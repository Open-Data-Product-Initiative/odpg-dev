<!-- AI_AGENT_GUIDANCE:
Use /schema/odpg.yaml or /schema/odpg.json to validate ODPG graph files.
Use /graph/objects.jsonl for retrieval, relationship classification, traversal planning, graph reasoning, validation hints, and lightweight AI-agent tool calls.
Use /scripts/odpg_validate.py for graph validation.
Use /scripts/odpg_summary.py for graph summaries.
Use /scripts/odpg_traverse.py for graph traversal.
Use /scripts/odpg_analyze.py for governance and strategic analysis.
Use /scripts/odpg_agent_context.py for AI-agent context extraction.
Use /scripts/generate_graph_explorer.py to generate a standalone HTML graph explorer from ODPG YAML.
Use ODPG for graph relationships, nodes, edges, traversal, governance propagation, strategic reasoning, and relationship semantics.
Use ODPC for catalog discovery; do not model discovery catalogs as ODPG graphs unless relationships or traversal are required.
Use ODPS for full data product metadata; in ODPG, reference data products as DataProduct nodes instead of copying full ODPS content.
Use ODPV when stable vocabulary terms, semantic mappings, or relationship names are needed.
-->
# Graph Toolkit

> Snippet of YAML version:

```yml
schema: https://opendataproducts.org/odpg-v1.0/schema/odpg.yaml
version: "1.0"
kind: Graph
graph:
  metadata:
    id: GRAPH-AVIATION-001
    name:
      en: Aviation Data Product Value Graph
    description:
      en: Graph describing how aviation data products, use cases, policies,
          agents, opportunities, and business objectives are connected.
    domain:
      en: Aviation
    purpose:
      en: Support portfolio analysis, value mapping, governance review,
          and AI-assisted reasoning.
    status: draft
    visibility: public
  nodes: []
  edges: []
```

ODPG is published in several forms for different users and tools. This specification provides the human-readable documentation, while the schema, graph object records, and Python scripts provide machine-readable resources for validation, graph reasoning, AI retrieval, traversal planning, strategic analysis, automation, and visualization. Use `odpg.yaml` or `odpg.json` to validate graph files, `objects.jsonl` for lightweight relationship classification and graph retrieval, the ODPG Python scripts for command-line graph validation and reasoning tasks, and the Graph Explorer generator when creating a visual inspection interface for ODPG YAML.

| Resource | Format | Purpose |
|---|---|---|
| [`llms.txt`](/llms.txt) | Text | AI agent guidance for discovering and using ODPG resources |
| [`odpg.yaml`](/schema/odpg.yaml) | YAML Schema | YAML representation of the ODPG validation schema |
| [`odpg.json`](/schema/odpg.json) | JSON Schema | JSON representation of the ODPG validation schema |
| [`objects.jsonl`](/graph/objects.jsonl) | JSONL | Agent-friendly one-object-per-line file for retrieval, relationship classification, traversal planning, graph reasoning, and lightweight tools |
| [`odpg_validate.py`](/scripts/odpg_validate.py) | Python | Validates graph structure, node integrity, edge integrity, confidence values, and core ODPG semantics |
| [`odpg_summary.py`](/scripts/odpg_summary.py) | Python | Produces graph metadata, node counts, edge counts, node types, edge types, and confidence summaries |
| [`odpg_traverse.py`](/scripts/odpg_traverse.py) | Python | Discovers relationship paths from a node with optional relationship filters and reverse traversal |
| [`odpg_analyze.py`](/scripts/odpg_analyze.py) | Python | Runs governance and strategic checks for orphan KPIs, unsupported objectives, ungoverned assets, and low-confidence relationships |
| [`odpg_agent_context.py`](/scripts/odpg_agent_context.py) | Python | Extracts trusted graph context around a focus node for AI-agent use |
| [`generate_graph_explorer.py`](/scripts/generate_graph_explorer.py) | Python | Generates a standalone HTML Graph Explorer from an ODPG YAML graph |

The Markdown tables in this specification are intended for human readers. The schema, JSONL, and graph tooling files are intended for programmable use, automation, validation, AI retrieval, traversal, reasoning, strategic analysis, AI-agent interaction, and graph visualization.

## Python Toolkit Scripts

The ODPG Python toolkit separates the most important command-line operations into focused scripts while sharing the same internal graph rules through `odpg_toolkit_core.py`:

| Script | Toolkit Coverage | Purpose |
|---|---|---|
| `odpg_validate.py` | Graph Validation Toolkit | Validate graph structure, required fields, node integrity, edge integrity, confidence values, and core ODPG semantics |
| `odpg_summary.py` | Graph Validation Toolkit / AI Agent Toolkit | Produce a JSON summary of metadata, node counts, edge counts, node types, edge types, and confidence values |
| `odpg_traverse.py` | Graph Traversal Toolkit | Discover relationship paths from a node, optionally filtering by relationship type or traversing incoming relationships |
| `odpg_analyze.py` | Strategic Intelligence Toolkit / Governance analysis | Detect orphan KPIs, unsupported objectives, ungoverned assets, low-confidence relationships, and use cases without strategic contribution |
| `odpg_agent_context.py` | AI Agent Toolkit | Extract trusted graph context around a focus node, including forward paths, reverse paths, related nodes, and governance signals |

Example usage:

```text
python source/scripts/odpg_validate.py -i "/path/to/graph.yml"
python source/scripts/odpg_summary.py -i "/path/to/graph.yml"
python source/scripts/odpg_traverse.py -i "/path/to/graph.yml" --start "DP-001" --depth 2
python source/scripts/odpg_analyze.py -i "/path/to/graph.yml"
python source/scripts/odpg_agent_context.py -i "/path/to/graph.yml" --node "AGENT-001" --depth 2
```

### Testing the Python Toolkit

The repository includes pytest coverage for the shared toolkit logic used by all five scripts. The tests verify graph validation, invalid edge handling, graph summaries, traversal paths, strategic and governance analysis, agent-context extraction, and JSON output writing.

```text
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_odpg_toolkit.py
```
