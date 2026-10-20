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
# Edges

> Example of edges object usage:

```yml
edges:
  - from: UC-AVIATION-001
    to: DP-AVIATION-001
    type: uses
    confidence: high

  - from: UC-AVIATION-001
    to: OBJ-AVIATION-001
    type: supports
    confidence: high

  - from: DP-AVIATION-001
    to: OBJ-AVIATION-001
    type: contributesTo
    confidence: medium
```

The edges section defines the relationships between nodes, where each edge establishes a directional connection that represents strategic alignment, operational dependency, semantic association, governance propagation, usage patterns, contribution paths, ownership relationships, or interoperability mappings between entities.

An edge always connects a source node to a target node using the from and to properties.


Through edges, ODPG enables organizations to construct connected value graphs capable of supporting strategic analysis, governance reasoning, graph traversal, semantic interoperability, dependency analysis, and AI-driven contextual reasoning.

## Edge Properties

Each edge within an ODPG graph contains properties that describe the relationship connecting two nodes.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| from | String | Yes | Source node identifier |
| to | String | Yes | Target node identifier |
| type | String | Yes | Relationship type |
| confidence | String | Yes | Confidence level of the relationship |
| x-odpg-assertion | Object | No | Optional draft claim contract; separate origin, evidence, review status and validity from confidence. |

The **from** property identifies the source node from which the relationship originates.

The **to** property identifies the destination node receiving the relationship.

The **type** property defines the semantic meaning of the relationship.

The **confidence** property records qualitative certainty reported by the
asserting party. Origin, evidence and review status are separate concepts,
represented by the optional draft `x-odpg-assertion` contract. Confidence alone
does not distinguish observed facts from declarations or inference.

## Supported Edge Types

ODPG supports multiple relationship types capable of representing operational, strategic, governance, semantic, and AI-related connections between graph entities.

| Edge Type      | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| uses           | A node uses another node as part of execution or operation    |
| supports       | A node supports a business objective                          |
| contributesTo  | A node contributes toward an outcome or objective             |
| measures       | A KPI measures an objective or outcome                        |
| tracks         | A node tracks or provides KPI-related information             |
| dependsOn      | A node depends on another node                                |
| produces       | A node produces data, outputs, or services                    |
| consumes       | A node consumes data, APIs, or outputs                        |
| governedBy     | A node is governed by a policy or control                     |
| ownedBy        | A node is owned by a person, team, or domain                  |
| alignsWith     | A node aligns strategically or semantically with another node |
| relatedTo      | A generic semantic relationship                               |
| impacts        | A node impacts another node                                   |
| derivedFrom    | A node originates from another node                           |
| exposes        | A node exposes an API or interface                            |
| monitors       | A node monitors another node                                  |
| identifies     | A node identifies an opportunity or condition                 |

The relationship model is designed to remain extensible so that organizations can introduce domain-specific relationship types while maintaining compatibility with the core ODPG graph structure.

## Optional Value Evidence Relationships

The draft Value Evidence profile adds `tests`, `expects`, `measuredBy`,
`hasBaseline`, `hasTarget`, `supportedBy` and `reviews`, and reuses core
relationships such as `uses`, `supports` and `measures`. The Adoption and
Evidence Profiles section defines their source/target types and required
chains; they are not new core relationship types. The shared validator
recognises the profile vocabulary when `odpg-value-evidence-0.1` is declared.

Nodes and edges may also carry `x-odpg-assertion`, validated against the
[shared assertion contract](/schema/profiles/assertion-0.1.json), independently
of Value Evidence profile adoption. Traversal preserves these fields. Analysis
distinguishes legacy declared links from current, accepted claims with evidence
pointers; `confidence` alone does not establish reviewed support.
