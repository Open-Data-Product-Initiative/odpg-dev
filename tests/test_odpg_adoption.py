# Authorship: Zaher Abou Shakra
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

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
