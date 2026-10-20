<!-- Authorship: Zaher Abou Shakra -->
<!-- AI_AGENT_GUIDANCE:
Use /schema/odpg.yaml or /schema/odpg.json to validate ODPG graph files.
Use ODPG for graph relationships, nodes, edges, traversal, governance propagation, strategic reasoning, and relationship semantics.
Use ODPC for catalog discovery; do not model discovery catalogs as ODPG graphs unless relationships or traversal are required.
Use ODPS for full data product metadata; in ODPG, reference data products as DataProduct nodes instead of copying full ODPS content.
Use ODPV when stable vocabulary terms, semantic mappings, or relationship names are needed.
Use confidence values high, medium, or low for edges.
Use x- prefixed extension fields for implementation-specific metadata or declared optional profiles; do not redefine core ODPG semantics.
-->
# ODPG Toolkit

The sections below describe optional architectural capabilities, not a claim
that all are implemented by the repository's scripts. The current Python
reference implementation provides local core/profile validation, topology
conversion, traversal, gap checks, context extraction and visualisation.
It does not provide a policy enforcement engine, agent runtime, authenticated
evidence service or federation service. See Adoption and Evidence Profiles for
the implemented draft contracts and the boundary between context and authority.

The ODPG Toolkit provides a collection of interoperable tooling capabilities that support graph creation, validation, traversal, governance reasoning, semantic interoperability, strategic intelligence analysis, and AI-agent interaction across Open Data Product ecosystems.

The toolkit may include:

* graph validators
* graph builders
* graph traversal engines
* graph visualization tools
* governance analyzers
* semantic enrichment engines
* strategic reasoning services
* AI-agent graph interfaces
* graph federation services
* interoperability adapters

## ODPG Agent Toolkit

The ODPG Agent Toolkit extends the graph ecosystem with agent-compatible interfaces that allow AI systems to navigate, reason over, and interact with interconnected enterprise data ecosystems using documented graph relationships and governance-aware traversal.

The Agent Toolkit may support:

* semantic graph traversal
* context retrieval
* objective discovery
* governance-aware execution
* relationship reasoning
* dependency analysis
* strategic opportunity detection
* graph-based memory
* explainable AI navigation
* context grounding with evidence pointers

This section is strategically important because ODPC focuses on discovery, while ODPG focuses on reasoning. That is the critical distinction.

## Toolkit Components

Toolkit components describe common tooling capabilities that may be implemented by platforms, governance systems, graph services, catalog systems, data product portals, AI-agent runtimes, or other interoperable software.

## Toolkit Conformance

The ODPG Toolkit describes interoperable capabilities rather than a single required software implementation. A tool MAY implement one or more toolkit components, provided that it preserves the ODPG graph model, validates against the official schema where applicable, and does not redefine core node, edge, confidence, or reference semantics.

Toolkit implementations SHOULD expose clear inputs and outputs so that graph validators, traversal engines, catalogs, governance systems, and AI-agent runtimes can interoperate consistently.

ODPG MAY provide an agent-friendly JSONL resource at `/graph/objects.jsonl`. This one-object-per-line file is intended for retrieval, relationship classification, traversal planning, graph reasoning, validation hints, and lightweight AI-agent tool calls. Unlike ODPC catalog JSONL resources, which focus on discovery and object selection, the ODPG JSONL resource focuses on graph reasoning and traversal semantics.

| Toolkit Component | Typical Input | Typical Output |
| --- | --- | --- |
| Graph Validation Toolkit | ODPG YAML or JSON | Validation report |
| Graph Traversal Toolkit | ODPG graph and traversal query | Paths, dependencies, impacted nodes |
| Strategic Intelligence Toolkit | ODPG graph and objectives | Gaps, overlaps, opportunities |
| AI Agent Toolkit | ODPG graph and agent task context | Graph context, assertion metadata and separately identified reviewed paths |
| Federation Toolkit | Multiple ODPG graphs | Federated graph view or cross-domain mappings |

ODPG provides focused Python command-line scripts for validation, conversion,
summaries, traversal, analysis and context extraction. The shared operations in
[`odpg_toolkit_core.py`](/scripts/odpg_toolkit_core.py) import
[`odpg_profiles.py`](/scripts/odpg_profiles.py) for bundled schema validation,
assertion validity and draft Value Evidence semantic checks. Both are supporting
modules, not CLI entry points. The converter and explorer have independent
implementations; run `odpg_validate.py` on their graph inputs or outputs to
establish conformance. Required Dependencies & Execution lists the packages,
module/schema layout and commands.

### Graph Validation Toolkit

The Graph Validation Toolkit validates ODPG documents against the official schema and verifies structural consistency, node integrity, edge validity, confidence values, and interoperability requirements.

The current implementation also checks the draft shared assertion contract and
the declared `odpg-value-evidence-0.1` profile, using the published profile
schemas plus typed-reference, unit, period and evidence-chain checks. Its JSON
report identifies declared profile conformance; unsupported profiles fail
explicitly. This does not certify referenced evidence or external interoperability
adapters. Governed Agent and Observed Lineage remain proposals.

Capabilities may include:

* schema validation
* node validation
* edge validation
* reference validation
* semantic consistency checks
* confidence validation

### Graph Traversal Toolkit

The reference scripts implement depth-limited forward/reverse traversal,
relationship filtering and full edge-metadata preservation. The broader
capabilities below are architectural possibilities; there is no executable
policy-propagation engine in this repository.

The Graph Traversal Toolkit enables traversal across interconnected graph entities using semantic, strategic, operational, and governance relationships.

Capabilities may include:

* path discovery
* dependency traversal
* governance propagation
* impact analysis
* semantic navigation
* strategic alignment analysis

### Strategic Intelligence Toolkit

The reference analyzer implements topology-gap checks and separate reviewed
support reporting. Thematic clustering, opportunity inference, duplicate use-case
detection and capability-alignment engines remain architectural possibilities.

The Strategic Intelligence Toolkit analyzes graph relationships to identify organizational gaps, overlapping initiatives, unsupported objectives, and emerging strategic opportunities.

Capabilities may include:

* orphan KPI detection
* strategic gap analysis
* thematic clustering
* opportunity inference
* duplicate use case detection
* capability alignment analysis

### AI Agent Toolkit

The reference script extracts graph context and recorded review metadata.
The broader capabilities below require external implementations; this repository
does not provide an agent runtime, tool execution or policy enforcement.

> Example of AI agent graph interaction:

```yml
nodes:
  - id: AGENT-001
    type: Agent
    $ref: ../agents/enterprise-analytics-agent.yaml

  - id: DP-001
    type: DataProduct
    $ref: ../products/customer-360.yaml

  - id: API-001
    type: API
    $ref: ../apis/customer-insights-api.yaml

edges:
  - from: AGENT-001
    to: DP-001
    type: uses
    confidence: high

  - from: AGENT-001
    to: API-001
    type: uses
    confidence: high
```

The AI Agent Toolkit enables AI agents and automation systems to interact with ODPG ecosystems through graph-native semantic interfaces and governance-aware traversal mechanisms.

The toolkit may support:

* graph retrieval APIs
* semantic context injection
* governance-aware graph traversal
* relationship discovery with evidence metadata
* explainable reasoning paths
* graph-based memory systems
* objective-aware planning
* policy-aware execution
* dependency reasoning
* graph-native orchestration

### Federation Toolkit

This is an architectural proposal. No federation service, synchronisation
runtime or cross-organisation authorization adapter is implemented here.

The Federation Toolkit enables organizations to connect multiple ODPG ecosystems into federated graph environments capable of supporting cross-domain interoperability, distributed governance, and enterprise-scale graph reasoning.

Capabilities may include:

* federated graph discovery
* cross-domain traversal
* graph synchronization
* semantic mapping
* distributed governance
* multi-organization graph interoperability
