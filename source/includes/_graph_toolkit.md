<!-- Authorship: Zaher Abou Shakra -->
<!-- AI_AGENT_GUIDANCE:
Use /schema/odpg.yaml or /schema/odpg.json to validate ODPG graph files.
Use /graph/objects.jsonl for retrieval, relationship classification, traversal planning, graph reasoning, validation hints, and lightweight AI-agent tool calls.
Use /scripts/odpg_validate.py for graph validation.
Use /scripts/odpg_convert.py to convert external graph formats into ODPG YAML.
Use /scripts/odpg_summary.py for graph summaries.
Use /scripts/odpg_traverse.py for graph traversal.
Use /scripts/odpg_analyze.py for governance and strategic analysis.
Use /scripts/odpg_agent_context.py for AI-agent context extraction.
Keep /scripts/odpg_toolkit_core.py and /scripts/odpg_profiles.py beside the CLI scripts, with the schema directory alongside scripts.
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

ODPG is published in several forms for different users and tools. This specification provides the human-readable documentation, while the schema, graph object records, and Python scripts provide machine-readable resources for validation, conversion, graph reasoning, AI retrieval, traversal planning, strategic analysis, automation, and visualization. Use `odpg.yaml` or `odpg.json` to validate graph files, `objects.jsonl` for lightweight relationship classification and graph retrieval, the ODPG Python scripts for command-line graph conversion, validation, and reasoning tasks, and the Graph Explorer generator when creating a visual inspection interface for ODPG YAML.

| Resource | Format | Purpose |
|---|---|---|
| [`llms.txt`](/llms.txt) | Text | AI agent guidance for discovering and using ODPG resources |
| [`odpg.yaml`](/schema/odpg.yaml) | YAML Schema | YAML representation of the ODPG validation schema |
| [`odpg.json`](/schema/odpg.json) | JSON Schema | JSON representation of the ODPG validation schema |
| [`assertion-0.1.json`](/schema/profiles/assertion-0.1.json) | JSON Schema | Draft shared assertion contract: origin, evidence, review and validity |
| [`value-evidence-0.1.json`](/schema/profiles/value-evidence-0.1.json) | JSON Schema overlay | Draft Value Evidence node fields; used with core and semantic validation |
| [`objects.jsonl`](/graph/objects.jsonl) | JSONL | Agent-friendly one-object-per-line file for retrieval, relationship classification, traversal planning, graph reasoning, and lightweight tools |
| [`odpg_toolkit_core.py`](/scripts/odpg_toolkit_core.py) | Python module | Shared toolkit graph operations and CLI handlers; imported support module |
| [`odpg_profiles.py`](/scripts/odpg_profiles.py) | Python module | Local schema loading, assertion validation and Value Evidence semantic checks; imported support module |
| [`aviation.yaml`](/examples/value-evidence/aviation.yaml) | YAML | Synthetic Value Evidence graph with continue and defer decisions |
| [`resources.yaml`](/examples/value-evidence/resources.yaml) | YAML | Local resources referenced by the synthetic aviation graph |
| [`odpg_validate.py`](/scripts/odpg_validate.py) | Python | Executes the bundled core schema, graph integrity, assertion and supported profile checks |
| [`odpg_convert.py`](/scripts/odpg_convert.py) | Python | Converts external graph formats such as JSON-LD, GraphML, GraphSON, RDF, OpenCypher, GQL, and Gremlin into ODPG YAML |
| [`odpg_summary.py`](/scripts/odpg_summary.py) | Python | Produces graph metadata, node counts, edge counts, node types, edge types, and confidence summaries |
| [`odpg_traverse.py`](/scripts/odpg_traverse.py) | Python | Discovers relationship paths from a node with optional relationship filters and reverse traversal |
| [`odpg_analyze.py`](/scripts/odpg_analyze.py) | Python | Runs governance and strategic checks for orphan KPIs, unsupported objectives, ungoverned assets, and low-confidence relationships |
| [`odpg_agent_context.py`](/scripts/odpg_agent_context.py) | Python | Extracts graph context with assertion metadata around a focus node for AI-agent use |
| [`generate_graph_explorer.py`](/scripts/generate_graph_explorer.py) | Python | Generates a standalone HTML Graph Explorer from an ODPG YAML graph |

The Markdown tables in this specification are intended for human readers. The schema, JSONL, and graph tooling files are intended for programmable use, automation, validation, AI retrieval, traversal, reasoning, strategic analysis, AI-agent interaction, and graph visualization.

## Python Toolkit Scripts

The ODPG Python toolkit separates command-line operations into focused scripts.
`odpg_toolkit_core.py` supplies the shared graph operations and imports
`odpg_profiles.py` for local schema and profile checks. These two modules have no
standalone CLI. Keep the module and schema directory layout described in
Required Dependencies & Execution; install PyYAML and `jsonschema[format]` before
running the shared toolkit.

| Script | Toolkit Coverage | Purpose |
|---|---|---|
| `odpg_validate.py` | Graph Validation Toolkit | Execute bundled core schema, graph integrity, assertion and supported declared profile validation |
| `odpg_convert.py` | Graph Conversion Toolkit | Convert JSON-LD, GraphML, GraphSON, RDF, OpenCypher, GQL, and Gremlin graph inputs into ODPG YAML |
| `odpg_summary.py` | Graph Validation Toolkit / AI Agent Toolkit | Produce a JSON summary of metadata, node counts, edge counts, node types, edge types, and confidence values |
| `odpg_traverse.py` | Graph Traversal Toolkit | Discover paths with complete assertion/extension metadata, relationship filters and reverse traversal |
| `odpg_analyze.py` | Strategic Intelligence Toolkit / Governance analysis | Report topology gaps and `objectivesWithoutReviewedSupport`; exclude explicitly unaccepted or inactive claims from support counts |
| `odpg_agent_context.py` | AI Agent Toolkit | Extract forward/reverse paths, nodes and governance signals; separate `reviewedPaths` and explain the authority boundary in `trustNotice` |

Example usage:

```text
python source/scripts/odpg_validate.py -i "/path/to/graph.yml"
python source/scripts/odpg_convert.py -i "/path/to/source.graphml" -o "/path/to/graph.yml"
python source/scripts/odpg_summary.py -i "/path/to/graph.yml"
python source/scripts/odpg_traverse.py -i "/path/to/graph.yml" --start "DP-001" --depth 2
python source/scripts/odpg_analyze.py -i "/path/to/graph.yml"
python source/scripts/odpg_agent_context.py -i "/path/to/graph.yml" --node "AGENT-001" --depth 2
```

For an executable profile example, run:

```bash
python source/scripts/odpg_validate.py -i source/examples/value-evidence/aviation.yaml
python source/scripts/odpg_agent_context.py -i source/examples/value-evidence/aviation.yaml --node HYP-1 --depth 2
```

Validation JSON contains `valid`, `errors` and `warnings`, plus a `profiles` map
when profiles are declared. Reviewed paths reflect recorded review metadata;
they do not authenticate evidence or grant access. The summary command reports
counts only and does not establish conformance. Validate before summarising or
generating an explorer.

### JSON output reference

`odpg_validate.py` emits `valid`, `errors` and `warnings`, plus `profiles` for
declared profiles. Exit status is zero for conformance and one for validation
failure. The profile map reports overall document/profile conformance; it is
not an independent evidence-authentication result.

`odpg_analyze.py` wraps its result in `analysis`, alongside schema/type warnings:

| Analysis field | Meaning |
| --- | --- |
| `orphanKpis` | KPI nodes without an active outgoing `measures` link. |
| `unsupportedBusinessObjectives` | Objectives without active incoming `supports`, `contributesTo` or alignment links; legacy declared links count. |
| `ungovernedAssets` | Data products, APIs, datasets, workflows and agents without an active outgoing `governedBy` link. |
| `lowConfidenceRelationships` | All relationships marked `low`, including unaccepted claims retained for inspection. |
| `useCasesWithoutStrategicContribution` | Use cases with active `uses` links but no active outgoing `supports` or `contributesTo` link. |
| `objectivesWithoutReviewedSupport` | Objectives without incoming support/alignment claims that are current, accepted and evidenced. |
| `analysisBasis` | Notice distinguishing declared topology from reviewed support and authority. |

For support checks, a legacy edge is treated as a declaration; an explicit
assertion must be accepted and within its validity window. These are checks of
the supplied graph, not proof that real-world governance or business support
is present or absent.

`odpg_agent_context.py` emits the following context fields, plus `warnings`:

| Context field | Meaning |
| --- | --- |
| `focusNode` | Requested node, or an identifier-only placeholder if absent. |
| `relatedNodes` | Nodes reached in the requested forward or reverse traversal. |
| `forwardPaths` | Outgoing traversal paths, preserving all edge metadata. |
| `reversePaths` | Incoming traversal paths, preserving all edge metadata. |
| `reviewedPaths` | Forward/reverse paths where every edge has a current, accepted assertion with evidence pointers. |
| `governanceSignals` | Unfiltered forward paths containing `governedBy`; not enforcement or approval decisions. |
| `trustNotice` | Notice that context is not authorization, authenticated evidence, verified business value or readiness. |

### Testing the Python Toolkit

The test suite covers shared graph operations plus adoption conformance:
converter output, assertion schema and validity windows, profile references,
metric units and periods, evidence/review chains, local resources and JSON CLI
reports. CI enforces at least 80% combined coverage for the two shared modules.
`test_odpg_adoption.py` also checks publication section/resource inventories,
local links, schema/metadata vocabularies, assertion enums, dependencies, profile
status, output fields and complete graph/assertion examples against the current
implementation. Run that file directly for the focused adoption audit:

```bash
python -m pytest tests/test_odpg_adoption.py
```

```text
python -m pip install -r requirements-dev.txt
python -m pytest tests --cov=odpg_toolkit_core --cov=odpg_profiles --cov-report=term-missing --cov-fail-under=80
```
