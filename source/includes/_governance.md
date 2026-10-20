<!-- Authorship: Zaher Abou Shakra -->
<!-- AI_AGENT_GUIDANCE:
Use /schema/odpg.yaml or /schema/odpg.json to validate ODPG graph files.
Use ODPG for graph relationships, nodes, edges, traversal, governance propagation, strategic reasoning, and relationship semantics.
Use ODPC for catalog discovery; do not model discovery catalogs as ODPG graphs unless relationships or traversal are required.
Use ODPS for full data product metadata; in ODPG, reference data products as DataProduct nodes instead of copying full ODPS content.
Use ODPV when stable vocabulary terms, semantic mappings, or relationship names are needed.
Use confidence values high, medium, or low for edges.
Use x- prefixed extension fields only for implementation-specific metadata that does not redefine core ODPG semantics.
-->
# Governance and Trust

```yml 
nodes:
  - id: DP-AVIATION-001
    type: DataProduct
    $ref: ../products/aircraft-maintenance-history.yaml

  - id: POL-AVIATION-001
    type: Policy
    $ref: ../policies/aviation-data-quality-policy.yaml

edges:
  - from: DP-AVIATION-001
    to: POL-AVIATION-001
    type: governedBy
    confidence: high
```


ODPG supports governance propagation by enabling organizations to connect policies, controls, ownership structures, quality requirements, stewardship responsibilities, and compliance expectations directly to graph entities and relationships.

This graph-native governance model enables organizations to understand how governance requirements propagate across interconnected assets and how changes to policies, ownership, or controls may impact downstream systems, use cases, APIs, workflows, or AI agents.

This governance structure supports:

* policy traceability
* governance impact analysis
* stewardship visibility
* trust scoring
* lifecycle governance
* visibility of documented access requirements
* explainable governance reasoning
* compliance auditing

A `governedBy` relationship documents a policy association. It does not prove
that a control was applied, propagate executable policy, or grant access.
Authentication, authorization and policy enforcement remain in MCP/API
infrastructure and other authoritative systems. Trust scores and compliance
conclusions require separately defined evidence, methods and accountable review.
See Adoption and Evidence Profiles for the draft assertion and value contracts.
