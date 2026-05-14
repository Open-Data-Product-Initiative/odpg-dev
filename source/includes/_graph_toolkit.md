<!-- AI_AGENT_GUIDANCE:
Use /schema/odpg.yaml or /schema/odpg.json to validate ODPG graph files.
Use /graph/objects.jsonl for retrieval, relationship classification, traversal planning, graph reasoning, validation hints, and lightweight AI-agent tool calls.
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

ODPG is published in several forms for different users and tools. This specification provides the human-readable documentation, while the schema, graph object records, and generator script provide machine-readable resources for validation, graph reasoning, AI retrieval, traversal planning, and automation. Use `odpg.yaml` or `odpg.json` to validate graph files, `objects.jsonl` for lightweight relationship classification and graph retrieval, and the Graph Explorer generator when creating a visual inspection interface for ODPG YAML.

| Resource | Format | Purpose |
|---|---|---|
| [`llms.txt`](/llms.txt) | Text | AI agent guidance for discovering and using ODPG resources |
| [`odpg.yaml`](/schema/odpg.yaml) | YAML Schema | YAML representation of the ODPG validation schema |
| [`odpg.json`](/schema/odpg.json) | JSON Schema | JSON representation of the ODPG validation schema |
| [`objects.jsonl`](/graph/objects.jsonl) | JSONL | Agent-friendly one-object-per-line file for retrieval, relationship classification, traversal planning, graph reasoning, and lightweight tools |

The Markdown tables in this specification are intended for human readers. The schema, JSONL, and graph tooling files are intended for programmable use, automation, validation, AI retrieval, traversal, reasoning, and graph visualization.
