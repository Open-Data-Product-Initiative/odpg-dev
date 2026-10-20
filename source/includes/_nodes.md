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
# Nodes

> Example of nodes object format:

```yml 
nodes:
  - id: UC-AVIATION-001
    type: UseCase
    $ref: ../usecases/predictive-maintenance-aircraft.yaml

  - id: OBJ-AVIATION-001
    type: BusinessObjective
    $ref: ../objectives/increase-fleet-availability.yaml

  - id: DP-AVIATION-001
    type: DataProduct
    $ref: ../products/aircraft-maintenance-history.yaml
```


The nodes section defines the entities included within the graph, where each node represents a resource, capability, objective, policy, product, workflow, dataset, or system participating in the ecosystem being modeled.

A node may represent an internal resource defined directly within the organization or an external specification referenced through another machine-readable file.

Instead of embedding full resource definitions directly into the graph, ODPG encourages interoperability through references using the `$ref` property, thereby enabling organizations to connect graph structures with ODPS documents, ODPV vocabularies, governance artifacts, APIs, workflows, use cases, or external specifications.

## Node Properties

Each node within an ODPG document represents a distinct entity participating in the graph ecosystem, where the node itself serves as the graph reference point that enables relationships, dependencies, semantic mappings, governance propagation, strategic alignment, and interoperability across connected specifications and platforms.

The following properties are defined for graph nodes.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| id | String | Yes | Unique identifier of the node |
| type | String | Yes | Type of graph entity represented by the node |
| $ref | String | Yes | Path or URI to the referenced specification or resource |
| x-odpg-assertion | Object | No | Optional draft assertion contract for a node claim; source, origin, evidence, review and validity. |
| x-odpg-value | Object | No | Draft Value Evidence attributes; required on the profile's node types when that profile is declared. |

The **id** property uniquely identifies the node within the graph and allows edges to establish relationships between connected entities.

The **type** property identifies the category of entity represented by the node, thereby enabling graph consumers, validation systems, governance engines, AI agents, and traversal engines to interpret the role of the entity correctly.

The **$ref** property provides a path or URI reference to the underlying specification, thereby allowing ODPG to function as a lightweight relationship layer that interoperates with external specifications such as ODPS documents, governance definitions, API specifications, vocabulary definitions, use case files, or objective specifications.

## Supported Node Types

ODPG supports multiple node types capable of representing strategic, operational, governance, semantic, and AI-related entities across enterprise ecosystems.

| Node Type            | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| DataProduct          | A data product defined using ODPS or compatible structures  |
| UseCase              | A business, analytical, operational, or AI-related use case |
| BusinessObjective    | A strategic business objective or organizational goal       |
| KPI                  | A measurable business or operational indicator              |
| Domain               | A business, organizational, technical, or data domain       |
| Dataset              | A structured or unstructured dataset                        |
| API                  | A service interface exposed or consumed by a data product   |
| Policy               | A governance, compliance, security, or quality policy       |
| Workflow             | A business or technical workflow                            |
| Agent                | An AI agent or automation actor                             |
| Capability           | A business or technical capability                          |
| StrategicOpportunity | An inferred or declared strategic opportunity               |


The node model is intentionally extensible so that organizations can expand graph structures with additional node types while preserving interoperability with the core ODPG structure.

## Optional Value Evidence Node Types

The draft `odpg-value-evidence-0.1` profile defines `ValueHypothesis`, `Outcome`,
`MetricDefinition`, `Baseline`, `Target`, `Measurement`, `Evidence` and
`ReviewDecision`. These are optional profile types, not additions to the core
type list above. Declare the profile under `graph.metadata.x-odpg-profiles` and
place its node attributes under `x-odpg-value`, while retaining `id`, `type`
and `$ref`.

The [Value Evidence overlay](/schema/profiles/value-evidence-0.1.json) defines
their fields. The Adoption and Evidence Profiles section specifies the required
reference and relationship chains. `odpg_profiles.py`, invoked by the shared
toolkit, validates these semantics and recognises the profile types when the
profile is declared. A `ReviewDecision` records an accountable conclusion;
it does not itself grant access or establish production readiness.
