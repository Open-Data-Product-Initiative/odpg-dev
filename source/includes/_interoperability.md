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
# AI Agent Interoperability

```yml 
nodes:
  - id: AGENT-AVIATION-001
    type: Agent
    $ref: ../agents/maintenance-recommendation-agent.yaml

  - id: DP-AVIATION-001
    type: DataProduct
    $ref: ../products/aircraft-maintenance-history.yaml

  - id: API-AVIATION-001
    type: API
    $ref: ../apis/maintenance-risk-score-api.yaml

edges:
  - from: AGENT-AVIATION-001
    to: DP-AVIATION-001
    type: uses
    confidence: high

  - from: AGENT-AVIATION-001
    to: API-AVIATION-001
    type: uses
    confidence: high
```

ODPG provides structured graph context that can be consumed by AI agents, automation systems, semantic search engines, orchestration platforms, and reasoning systems operating across enterprise ecosystems.

Through graph traversal, AI agents can identify:

* which data products are relevant to a task
* which APIs are available
* which objectives are being supported
* which policies are associated with graph entities
* which governance boundaries exist
* which dependencies affect execution
* which relationships carry explicit origin, evidence and review metadata

An `Agent` node describes an actor or definition, not a particular execution.
`Agent → uses → API` describes a relationship and MUST NOT authorize a call.
Agent runs, approval events, policy decisions and evaluations belong to the
proposed Governed Agent profile, which is not implemented in this release.
Context extraction preserves assertion metadata and reports reviewed paths
separately; it does not authenticate evidence or enforce policies.

## Interoperability

ODPG is designed to operate as an interoperable relationship layer across the broader Open Data Products ecosystem, where graph nodes may reference ODPS data products, ODPV vocabulary definitions, ODPC catalog entries, governance specifications, APIs, workflows, use cases, KPI definitions, or external organizational assets.

The `$ref` property enables ODPG to link graph entities to external specifications while maintaining lightweight graph portability and reusable interoperability structures.

```yml
$ref: ../products/aircraft-maintenance-history.yaml
```

References provide a basis for linking graphs across teams and domains; the
reference toolkit does not implement a federation service. The proposed
`odpg-observed-lineage-0.1` profile would link PROV and OpenLineage records, while
`odpg-governed-agent-0.1` would distinguish definitions from observed runs and
approval/evaluation evidence. Both remain unimplemented proposals. The current
implemented draft is `odpg-value-evidence-0.1`, with a shared assertion contract;
see Adoption and Evidence Profiles for schemas, mappings and conformance scope.
