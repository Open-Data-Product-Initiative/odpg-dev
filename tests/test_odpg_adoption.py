# Authorship: Zaher Abou Shakra
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator
from packaging.requirements import Requirement

from test_odpg_toolkit import graph_fixture

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source/scripts"))
import odpg_convert
import odpg_toolkit_core as core

EXAMPLE = ROOT / "source/examples/value-evidence/aviation.yaml"


def example():
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def assertion(**changes):
    result = {
        "id": "claim-1", "origin": "observed", "source": "https://example.org/source",
        "assertedAt": "2026-10-01T00:00:00Z", "reviewStatus": "accepted",
        "reviewer": "Example reviewer", "reviewedAt": "2026-10-02T00:00:00Z",
        "evidence": [{"uri": "https://example.org/evidence"}],
    }
    result.update(changes)
    return result


@pytest.mark.parametrize("field,value", [("version", 1.0), ("unexpected", True), ("graph", [])])
def test_core_executes_published_schema(field, value):
    graph = graph_fixture()
    graph[field] = value
    assert core.validate_graph(graph)[0]


@pytest.mark.parametrize("value", [None, [], "graph"])
def test_non_object_document_is_reported(value):
    assert core.validate_graph(value)[0]


@pytest.mark.parametrize("source,format", [
    ({"vertices": [{"id": "a"}, {"id": "b"}], "edges": [{"outV": "a", "inV": "b"}]}, "graphson"),
    ('<graphml><graph><node id="a"/></graph></graphml>', "graphml"),
    ({"@graph": [{"@id": "a", "@type": "DataProduct"}]}, "jsonld"),
])
def test_converter_output_conforms(source, format):
    document = odpg_convert.convert_graph(source, format)
    assert document["schema"].endswith("/schema/odpg.yaml")
    assert document["version"] == "1.0"
    assert core.validate_graph(document)[0] == []


def test_unknown_converter_type_remains_explicit():
    graph = odpg_convert.convert_graph({"vertices": [{"id": "a"}]}, "graphson")
    assert graph["graph"]["nodes"][0]["type"] == "Resource"
    assert "Resource" in " ".join(core.validate_graph(graph)[1])


@pytest.mark.parametrize("changes", [
    {"origin": "accepted"}, {"reviewStatus": "observed"}, {"source": ""},
    {"assertedAt": "yesterday"}, {"evidence": []}, {"reviewer": ""},
    {"validFrom": "2026-12-01T00:00:00Z", "validUntil": "2026-01-01T00:00:00Z"},
])
def test_invalid_assertions_fail(changes):
    graph = graph_fixture()
    graph["graph"]["edges"][0]["x-odpg-assertion"] = assertion(**changes)
    assert core.validate_graph(graph)[0]


def test_traversal_preserves_evidence_without_aliasing_input():
    graph = graph_fixture()
    graph["graph"]["edges"][0]["x-odpg-assertion"] = assertion()
    paths = core.traverse_graph(graph, "UC-001", 1)
    claim = paths[0]["relationships"][0]["x-odpg-assertion"]
    assert claim == assertion()
    claim["reviewStatus"] = "rejected"
    assert graph["graph"]["edges"][0]["x-odpg-assertion"]["reviewStatus"] == "accepted"


@pytest.mark.parametrize("changes", [{"reviewStatus": "rejected"}, {"reviewStatus": "pending"},
    {"validUntil": "2000-01-01T00:00:00Z"}, {"validFrom": "2999-01-01T00:00:00Z"}])
def test_unaccepted_or_inactive_claims_do_not_establish_support(changes):
    graph = graph_fixture()
    for edge in graph["graph"]["edges"]:
        edge["x-odpg-assertion"] = assertion(**changes)
    assert "OBJ-001" in core.analyze_graph(graph)["unsupportedBusinessObjectives"]
    assert core.agent_context(graph, "UC-001", 2)["reviewedPaths"] == []


def test_legacy_topology_is_not_reviewed_support():
    graph = graph_fixture()
    result = core.analyze_graph(graph)
    assert result["unsupportedBusinessObjectives"] == []
    assert "OBJ-001" in result["objectivesWithoutReviewedSupport"]
    context = core.agent_context(graph, "UC-001", 2)
    assert context["reviewedPaths"] == []
    assert "authorization" in context["trustNotice"]


def test_accepted_evidenced_claims_are_exposed_as_reviewed():
    graph = graph_fixture()
    for i, edge in enumerate(graph["graph"]["edges"]):
        edge["x-odpg-assertion"] = assertion(id=f"claim-{i}")
    assert core.validate_graph(graph)[0] == []
    assert core.analyze_graph(graph)["objectivesWithoutReviewedSupport"] == []
    assert core.agent_context(graph, "UC-001", 2)["reviewedPaths"]


def test_duplicate_assertion_ids_are_rejected():
    graph = graph_fixture()
    for edge in graph["graph"]["edges"]:
        edge["x-odpg-assertion"] = assertion()
    assert core.validate_graph(graph)[0]


def test_value_example_conforms_and_has_contrasting_decisions():
    graph = example()
    assert core.validate_graph(graph) == ([], [])
    decisions = [n["x-odpg-value"]["decision"] for n in graph["graph"]["nodes"] if n["type"] == "ReviewDecision"]
    assert set(decisions) == {"continue", "defer"}


@pytest.mark.parametrize("mutation", ["unknown-profile", "missing-evidence", "unit-mismatch", "missing-reviewer", "missing-link", "missing-baseline", "invalid-period"])
def test_invalid_value_chains_fail(mutation):
    graph = example()
    nodes = graph["graph"]["nodes"]
    measurement = next(n for n in nodes if n["type"] == "Measurement")["x-odpg-value"]
    if mutation == "unknown-profile":
        graph["graph"]["metadata"]["x-odpg-profiles"].append("unimplemented-0.1")
    elif mutation == "missing-evidence":
        measurement["evidence"] = ["missing"]
    elif mutation == "unit-mismatch":
        measurement["unit"] = "USD"
    elif mutation == "missing-reviewer":
        next(n for n in nodes if n["type"] == "ReviewDecision")["x-odpg-value"].pop("reviewer")
    elif mutation == "missing-link":
        graph["graph"]["edges"] = []
    elif mutation == "missing-baseline":
        next(n for n in nodes if n["type"] == "ValueHypothesis")["x-odpg-value"]["baseline"] = "missing"
    else:
        measurement["periodEnd"] = "1900-01-01T00:00:00Z"
    assert core.validate_graph(graph)[0]


def test_profile_schema_is_a_valid_json_schema():
    paths = list((ROOT / "source/schema/profiles").glob("*.json"))
    assert len(paths) >= 2
    for path in paths:
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_cli_reports_conformance_and_failure(tmp_path):
    command = [sys.executable, str(ROOT / "source/scripts/odpg_validate.py"), "-i", str(EXAMPLE)]
    valid = subprocess.run(command, capture_output=True, text=True)
    assert valid.returncode == 0, valid.stderr
    assert json.loads(valid.stdout)["profiles"]["odpg-value-evidence-0.1"] == "conformant"
    invalid_path = tmp_path / "invalid.yaml"
    invalid_path.write_text("version: 1.0\nkind: Graph\ngraph: {}", encoding="utf-8")
    invalid = subprocess.run(command[:-1] + [str(invalid_path)], capture_output=True, text=True)
    assert invalid.returncode == 1
    assert json.loads(invalid.stdout)["valid"] is False


def test_core_schema_constraints_have_not_changed():
    graph = graph_fixture()
    graph["x-odpg-profiles"] = ["odpg-value-evidence-0.1"]
    assert core.validate_graph(graph)[0]


@pytest.mark.parametrize("content", ["- not-an-object", "graph: [", ""])
def test_cli_invalid_input_is_machine_readable(tmp_path, capsys, content):
    path = tmp_path / "invalid.yaml"
    path.write_text(content, encoding="utf-8")
    args = type("Args", (), {"input": path, "output": None})()
    assert core.command_validate(args) == 1
    assert json.loads(capsys.readouterr().out)["errors"]


def test_validating_document_does_not_fetch_its_schema_or_references(monkeypatch):
    import urllib.request
    def reject_network(*args, **kwargs):
        raise AssertionError("Validation must remain local")
    monkeypatch.setattr(urllib.request, "urlopen", reject_network)
    graph = graph_fixture()
    graph["schema"] = "https://example.invalid/untrusted-schema.json"
    graph["graph"]["nodes"][0]["$ref"] = "https://example.invalid/resource"
    assert core.validate_graph(graph)[0] == []


@pytest.mark.parametrize("declaration", ["odpg-value-evidence-0.1", None, [123], ["odpg-value-evidence-0.1"] * 2])
def test_profile_declarations_are_explicit_and_unique(declaration):
    graph = graph_fixture()
    graph["graph"]["metadata"]["x-odpg-profiles"] = declaration
    assert core.validate_graph(graph)[0]


def test_reference_example_resources_are_local_and_resolvable():
    from urllib.parse import urldefrag
    graph = example()
    for node in graph["graph"]["nodes"]:
        filename, identifier = urldefrag(node["$ref"])
        resources = yaml.safe_load((EXAMPLE.parent / filename).read_text(encoding="utf-8"))
        assert identifier.removeprefix("/") in resources


@pytest.mark.parametrize("command", [core.command_summary, core.command_traverse, core.command_analyze, core.command_agent_context])
def test_cli_wrappers_return_json_for_reference_example(command, capsys):
    args = type("Args", (), {"input": EXAMPLE, "output": None, "start": "HYP-1", "node": "HYP-1",
                            "depth": 2, "relationship": None, "reverse": False})()
    assert command(args) == 0
    assert isinstance(json.loads(capsys.readouterr().out), dict)


@pytest.mark.parametrize("command", [core.command_traverse, core.command_analyze, core.command_agent_context])
def test_cli_wrappers_reject_schema_invalid_graph(command, tmp_path, capsys):
    path = tmp_path / "invalid.yaml"
    path.write_text("kind: Graph\nversion: 1.0\ngraph: {}", encoding="utf-8")
    args = type("Args", (), {"input": path, "output": None})()
    assert command(args) == 1
    assert json.loads(capsys.readouterr().out)["valid"] is False


def test_value_extensions_require_profile_declaration():
    graph = example()
    graph["graph"]["metadata"].pop("x-odpg-profiles")
    assert core.validate_graph(graph)[0]


def test_missing_profile_node_types_fail():
    graph = example()
    graph["graph"]["nodes"] = [n for n in graph["graph"]["nodes"] if n["type"] != "Outcome"]
    assert core.validate_graph(graph)[0]


@pytest.mark.parametrize("field", ["measurements", "reviewDecision"])
def test_cross_hypothesis_references_fail(field):
    graph = example()
    hypothesis = next(n for n in graph["graph"]["nodes"] if n["id"] == "HYP-1")["x-odpg-value"]
    hypothesis[field] = ["MEAS-2"] if field == "measurements" else "REVIEW-2"
    assert core.validate_graph(graph)[0]


def test_complete_graph_snippets_conform_to_core_schema():
    import re
    files = [ROOT / "README.md", ROOT / "source/index.html.md", *(ROOT / "source/includes").glob("*.md")]
    checked = 0
    for path in files:
        for block in re.findall(r"```(?:yaml|yml)\s*\n(.*?)```", path.read_text(encoding="utf-8"), re.S):
            document = yaml.safe_load(block)
            if isinstance(document, dict) and document.get("kind") == "Graph":
                assert core.validate_graph(document)[0] == [], str(path)
                checked += 1
    assert checked >= 5


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_measurements_must_be_finite(value):
    graph = example()
    next(n for n in graph["graph"]["nodes"] if n["type"] == "Measurement")["x-odpg-value"]["value"] = value
    assert core.validate_graph(graph)[0]


def test_assertion_validity_end_is_exclusive():
    from datetime import datetime, timezone
    from odpg_profiles import assertion_is_active
    edge = {"x-odpg-assertion": assertion(validFrom="2026-01-01T00:00:00Z", validUntil="2026-02-01T00:00:00Z")}
    assert assertion_is_active(edge, datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert not assertion_is_active(edge, datetime(2026, 2, 1, tzinfo=timezone.utc))


def publication_files():
    frontmatter = yaml.safe_load((ROOT / "source/index.html.md").read_text(encoding="utf-8").split("---", 2)[1])
    return [ROOT / "README.md", ROOT / "source/index.html.md", ROOT / "source/llms.txt",
            *(ROOT / f"source/includes/_{name}.md" for name in frontmatter["includes"])]


def knowledge_records():
    return [json.loads(line) for line in (ROOT / "source/graph/objects.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def test_published_page_includes_every_section_once():
    frontmatter = yaml.safe_load((ROOT / "source/index.html.md").read_text(encoding="utf-8").split("---", 2)[1])
    includes = frontmatter["includes"]
    assert len(includes) == len(set(includes))
    assert set(includes) == {p.stem.removeprefix("_") for p in (ROOT / "source/includes").glob("_*.md")}


@pytest.mark.parametrize("name", ["_catalog.md", "_graph_toolkit.md"])
def test_execution_resource_tables_cover_all_python_modules(name):
    document = (ROOT / "source/includes" / name).read_text(encoding="utf-8")
    listed = set(re.findall(r"\]\(/scripts/([^/)]+\.py)\)", document))
    assert listed == {p.name for p in (ROOT / "source/scripts").glob("*.py")}


def test_machine_resource_inventory_covers_every_python_module():
    records = knowledge_records()
    listed = {r["path"] for r in records if r["objectType"] in {"ToolkitScript", "ToolkitModule"}}
    expected = {"/scripts/" + p.name for p in (ROOT / "source/scripts").glob("*.py")}
    assert listed == expected
    assert len({r["id"] for r in records}) == len(records)


def test_published_local_links_resolve():
    from urllib.parse import unquote, urlsplit
    for path in publication_files():
        document = path.read_text(encoding="utf-8")
        targets = re.findall(r"\]\(([^)\s]+)(?:\s+[^)]*)?\)", document)
        targets += re.findall(r'(?:href|src)=[\"\']([^\"\']+)[\"\']', document)
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            filename = unquote(parsed.path)
            base = ROOT if path == ROOT / "README.md" else ROOT / "source"
            resolved = base / filename.lstrip("/")
            assert resolved.exists(), f"{path.relative_to(ROOT)}: broken local reference {target}"
    for record in knowledge_records():
        if "path" in record:
            assert (ROOT / "source" / record["path"].lstrip("/")).is_file(), record["id"]


def test_dependency_table_matches_manifest_and_ci_python():
    manifest = {str(Requirement(line.strip())) for line in (ROOT / "requirements-dev.txt").read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")}
    catalog = (ROOT / "source/includes/_catalog.md").read_text(encoding="utf-8")
    listed = {str(Requirement(spec)) for spec in re.findall(r"^\| `([^`]+[<>=][^`]+)` \|", catalog, re.M)}
    assert listed == manifest
    workflow = yaml.safe_load((ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8"))
    setup = next(step for step in workflow["jobs"]["python-conformance"]["steps"] if "setup-python" in step.get("uses", ""))
    for filename in ("README.md", "source/includes/_catalog.md", "source/includes/_adoption.md", "source/llms.txt"):
        assert "Python " + setup["with"]["python-version"] in (ROOT / filename).read_text(encoding="utf-8")


def test_core_vocabularies_match_schema_documentation_and_records():
    schema = json.loads((ROOT / "source/schema/odpg.json").read_text(encoding="utf-8"))
    records = knowledge_records()
    for kind, filename, heading in [("node", "_nodes.md", "## Optional Value Evidence"), ("edge", "_edges.md", "## Optional Value Evidence")]:
        expected = set(schema["$defs"][kind]["properties"]["type"]["examples"])
        text = (ROOT / "source/includes" / filename).read_text(encoding="utf-8").split(heading)[0]
        text = text.split(f"## Supported {kind.title()} Types", 1)[1]
        listed = {match.strip() for match in re.findall(r"^\| ([A-Za-z]+)\s*\|", text, re.M)}
        assert expected == listed
        assert {r["id"] for r in records if r["objectType"] == kind.title() + "Type"} == expected
    confidence = set(schema["$defs"]["edge"]["properties"]["confidence"]["enum"])
    assert {r["id"] for r in records if r["objectType"] == "ConfidenceValue"} == confidence


def test_profile_vocabularies_are_discoverable_in_relevant_sections():
    from odpg_profiles import PROFILE_ID, PROFILE_NODE_TYPES, PROFILE_EDGE_TYPES
    records = knowledge_records()
    assert {r["name"] for r in records if r["objectType"] == "ProfileNodeType" and r["profile"] == PROFILE_ID} == PROFILE_NODE_TYPES
    assert {r["name"] for r in records if r["objectType"] == "ProfileEdgeType" and r["profile"] == PROFILE_ID} == PROFILE_EDGE_TYPES
    for filename in ("_adoption.md", "_nodes.md", "_terms.md"):
        text = (ROOT / "source/includes" / filename).read_text(encoding="utf-8")
        assert all(f"`{name}`" in text for name in PROFILE_NODE_TYPES), filename
    for filename in ("_adoption.md", "_edges.md"):
        text = (ROOT / "source/includes" / filename).read_text(encoding="utf-8")
        assert all(f"`{name}`" in text for name in PROFILE_EDGE_TYPES), filename


def test_assertion_enums_match_machine_guidance_and_profile_docs():
    schema = json.loads((ROOT / "source/schema/profiles/assertion-0.1.json").read_text(encoding="utf-8"))
    record = next(r for r in knowledge_records() if r["id"] == "x-odpg-assertion")
    for field in ("origin", "reviewStatus"):
        expected = set(schema["properties"][field]["enum"])
        assert set(record[field]) == expected
        for filename in ("source/includes/_adoption.md", "source/llms.txt"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            assert all(f"`{value}`" in text for value in expected), (filename, field)


def test_schema_constraints_and_profile_schema_indexes_stay_in_sync():
    def constraints(value):
        if isinstance(value, dict):
            return {key: constraints(item) for key, item in value.items() if key not in {"description", "title", "examples"}}
        return [constraints(item) for item in value] if isinstance(value, list) else value
    json_schema = json.loads((ROOT / "source/schema/odpg.json").read_text(encoding="utf-8"))
    yaml_schema = yaml.safe_load((ROOT / "source/schema/odpg.yaml").read_text(encoding="utf-8"))
    assert constraints(json_schema) == constraints(yaml_schema)
    for filename in ("_catalog.md", "_graph_toolkit.md"):
        text = (ROOT / "source/includes" / filename).read_text(encoding="utf-8")
        for schema in (ROOT / "source/schema/profiles").glob("*.json"):
            assert schema.name in text, (filename, schema.name)


def test_section_guidance_does_not_reintroduce_obsolete_semantics():
    for path in publication_files():
        text = path.read_text(encoding="utf-8")
        assert "only for implementation-specific metadata" not in text, path
        assert "contributes_to" not in text and "governed_by" not in text, path
        assert "the ref property" not in text.lower(), path


def test_proposed_profiles_are_rejected_and_not_advertised_as_implemented():
    for record in knowledge_records():
        if record["objectType"] == "ProfileProposal":
            assert record["status"] == "not-implemented"
            graph = graph_fixture()
            graph["graph"]["metadata"]["x-odpg-profiles"] = [record["id"]]
            assert core.validate_graph(graph)[0]
            for filename in ("source/includes/_adoption.md", "source/llms.txt"):
                assert record["id"] in (ROOT / filename).read_text(encoding="utf-8")


def test_machine_output_fields_match_shared_toolkit():
    records = {r["id"]: r for r in knowledge_records()}
    assert set(records["odpg_analyze.py"]["outputFields"]) == set(core.analyze_graph(graph_fixture()))
    assert set(records["odpg_agent_context.py"]["contextFields"]) == set(core.agent_context(graph_fixture(), "DP-001", 1))


def test_documented_assertion_examples_validate():
    from odpg_profiles import schema_errors
    checked = 0
    for path in publication_files():
        for block in re.findall(r"```(?:yaml|yml)\s*\n(.*?)```", path.read_text(encoding="utf-8"), re.S):
            document = yaml.safe_load(block)
            if isinstance(document, dict) and "x-odpg-assertion" in document:
                assert schema_errors(document["x-odpg-assertion"], "assertion-0.1.json") == [], path
                checked += 1
    assert checked > 0


def test_metadata_inventory_covers_required_and_optional_schema_fields():
    schema = json.loads((ROOT / "source/schema/odpg.json").read_text(encoding="utf-8"))["$defs"]["graphMetadata"]
    records = {r["id"].removeprefix("graph.metadata."): r for r in knowledge_records() if r["objectType"] == "GraphMetadataField"}
    assert set(records) == set(schema["properties"])
    for name, definition in schema["properties"].items():
        assert records[name]["required"] == (name in schema["required"])
        if "enum" in definition:
            assert records[name]["allowedValues"] == definition["enum"]


def test_structural_field_paths_match_the_core_schema():
    schema = json.loads((ROOT / "source/schema/odpg.json").read_text(encoding="utf-8"))
    text = (ROOT / "source/includes/_structure.md").read_text(encoding="utf-8")
    for prefix, shape in [("", schema), ("graph.", schema["$defs"]["graph"]), ("graph.metadata.", schema["$defs"]["graphMetadata"])]:
        for name in shape["required"]:
            assert re.search(r"^\| `" + re.escape(prefix + name) + r"`\s*\|[^|]+\| Yes \|", text, re.M), prefix + name


def test_machine_capabilities_distinguish_reference_features_from_proposals():
    components = {r["id"]: r for r in knowledge_records() if r["objectType"] == "ToolkitComponent"}
    for name in ("GraphValidationToolkit", "GraphTraversalToolkit", "StrategicIntelligenceToolkit", "AIAgentToolkit"):
        assert components[name]["implementationStatus"] == "reference-implemented"
    assert components["FederationToolkit"]["implementationStatus"] == "not-implemented"
    assert components["FederationToolkit"]["capabilityScope"] == "architectural-proposal"


def test_profile_required_fields_match_schema_records_and_adoption_table():
    schema = json.loads((ROOT / "source/schema/profiles/value-evidence-0.1.json").read_text(encoding="utf-8"))
    records = {r["name"]: r for r in knowledge_records() if r["objectType"] == "ProfileNodeType"}
    document = (ROOT / "source/includes/_adoption.md").read_text(encoding="utf-8")
    baseline_row = next(line for line in document.splitlines() if line.startswith("| `Baseline`, `Target` |"))
    for clause in schema["allOf"]:
        name = clause["if"]["properties"]["type"]["const"]
        expected = set(clause["then"]["properties"]["x-odpg-value"]["required"])
        assert set(records[name]["requiredFields"]) == expected
        row = next(line for line in document.splitlines() if line.startswith(f"| `{name}`") or (name == "Target" and line == baseline_row))
        if name == "Measurement":
            row += baseline_row
        assert expected <= set(re.findall(r"`([^`]+)`", row)), name


def test_shared_toolkit_output_fields_are_documented():
    document = (ROOT / "source/includes/_graph_toolkit.md").read_text(encoding="utf-8")
    fields = set(core.analyze_graph(graph_fixture())) | set(core.agent_context(graph_fixture(), "DP-001", 1))
    assert all(f"`{field}`" in document for field in fields)
