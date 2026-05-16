import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "source" / "scripts"))

import odpg_toolkit_core  # noqa: E402


def graph_fixture():
    return {
        "schema": "https://opendataproducts.org/odpg-v1.0/schema/odpg.yaml",
        "version": "1.0",
        "kind": "Graph",
        "graph": {
            "metadata": {
                "id": "GRAPH-TEST-001",
                "name": {"en": "Test Graph"},
                "description": {"en": "A graph used by toolkit tests."},
            },
            "nodes": [
                {"id": "UC-001", "type": "UseCase", "$ref": "../usecases/test.yaml"},
                {"id": "DP-001", "type": "DataProduct", "$ref": "../products/test.yaml"},
                {"id": "API-001", "type": "API", "$ref": "../apis/test.yaml"},
                {"id": "OBJ-001", "type": "BusinessObjective", "$ref": "../objectives/test.yaml"},
                {"id": "KPI-001", "type": "KPI", "$ref": "../kpis/test.yaml"},
                {"id": "POL-001", "type": "Policy", "$ref": "../policies/test.yaml"},
                {"id": "AGENT-001", "type": "Agent", "$ref": "../agents/test.yaml"},
            ],
            "edges": [
                {"from": "UC-001", "to": "DP-001", "type": "uses", "confidence": "high"},
                {"from": "UC-001", "to": "OBJ-001", "type": "supports", "confidence": "high"},
                {"from": "DP-001", "to": "API-001", "type": "exposes", "confidence": "high"},
                {"from": "DP-001", "to": "KPI-001", "type": "tracks", "confidence": "medium"},
                {"from": "KPI-001", "to": "OBJ-001", "type": "measures", "confidence": "high"},
                {"from": "DP-001", "to": "POL-001", "type": "governedBy", "confidence": "high"},
                {"from": "AGENT-001", "to": "DP-001", "type": "uses", "confidence": "high"},
            ],
        },
    }


def test_validate_graph_accepts_valid_graph():
    errors, warnings = odpg_toolkit_core.validate_graph(graph_fixture())

    assert errors == []
    assert warnings == []


def test_validate_graph_rejects_edge_with_unknown_node():
    graph = graph_fixture()
    graph["graph"]["edges"].append(
        {"from": "UC-001", "to": "MISSING-001", "type": "uses", "confidence": "high"}
    )

    errors, warnings = odpg_toolkit_core.validate_graph(graph)

    assert warnings == []
    assert "Edge target does not match any node id: MISSING-001" in errors


def test_summarize_graph_counts_nodes_edges_and_types():
    summary = odpg_toolkit_core.summarize_graph(graph_fixture())

    assert summary["id"] == "GRAPH-TEST-001"
    assert summary["nodeCount"] == 7
    assert summary["edgeCount"] == 7
    assert summary["nodeTypes"]["DataProduct"] == 1
    assert summary["edgeTypes"]["uses"] == 2
    assert summary["confidenceValues"] == {"high": 6, "medium": 1}


def test_traverse_graph_returns_paths_from_start_node():
    paths = odpg_toolkit_core.traverse_graph(graph_fixture(), "UC-001", depth=2)

    assert {
        "start": "UC-001",
        "end": "DP-001",
        "depth": 1,
        "relationships": [{"from": "UC-001", "to": "DP-001", "type": "uses", "confidence": "high"}],
    } in paths
    assert any(path["end"] == "API-001" and path["depth"] == 2 for path in paths)


def test_analyze_graph_reports_governance_and_strategy_gaps():
    graph = graph_fixture()
    graph["graph"]["nodes"].append(
        {"id": "OBJ-002", "type": "BusinessObjective", "$ref": "../objectives/unsupported.yaml"}
    )
    graph["graph"]["nodes"].append(
        {"id": "API-002", "type": "API", "$ref": "../apis/ungoverned.yaml"}
    )
    graph["graph"]["edges"].append(
        {"from": "API-002", "to": "DP-001", "type": "dependsOn", "confidence": "low"}
    )

    analysis = odpg_toolkit_core.analyze_graph(graph)

    assert "OBJ-002" in analysis["unsupportedBusinessObjectives"]
    assert "API-002" in analysis["ungovernedAssets"]
    assert analysis["lowConfidenceRelationships"] == [
        {"from": "API-002", "to": "DP-001", "type": "dependsOn", "confidence": "low"}
    ]


def test_agent_context_includes_forward_reverse_paths_and_related_nodes():
    context = odpg_toolkit_core.agent_context(graph_fixture(), "DP-001", depth=1)

    related_ids = {node["id"] for node in context["relatedNodes"]}
    assert context["focusNode"]["id"] == "DP-001"
    assert {"UC-001", "AGENT-001", "API-001", "KPI-001", "POL-001"}.issubset(related_ids)
    assert any(path["end"] == "POL-001" for path in context["governanceSignals"])


def test_command_validate_writes_json_output(tmp_path):
    graph_path = tmp_path / "graph.yml"
    output_path = tmp_path / "validation.json"
    graph_path.write_text(
        """
schema: https://opendataproducts.org/odpg-v1.0/schema/odpg.yaml
version: "1.0"
kind: Graph
graph:
  metadata:
    id: GRAPH-CLI-001
    name:
      en: CLI Test Graph
    description:
      en: CLI validation fixture.
  nodes:
    - id: DP-001
      type: DataProduct
      $ref: ../products/test.yaml
  edges: []
""".lstrip(),
        encoding="utf-8",
    )

    result = odpg_toolkit_core.command_validate(
        type("Args", (), {"input": graph_path, "output": output_path})()
    )

    assert result == 0
    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "valid": True,
        "errors": [],
        "warnings": [],
    }
