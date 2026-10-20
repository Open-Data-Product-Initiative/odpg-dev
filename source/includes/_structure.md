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
# Specification Structure

> Example of details object usage:

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
      en: Graph describing how aviation data products, use cases, policies, agents, opportunities, and business objectives are connected.
  nodes: []
  edges: []
```

An ODPG document consists of a standardized graph structure composed of metadata, graph nodes, and graph edges, where the graph itself represents a connected ecosystem of business, operational, technical, governance, and AI-related entities.

The root structure of an ODPG document is defined as follows:

## Mandatory attributes

The following table uses full paths. `schema`, `version`, `kind` and `graph` are document-level properties; metadata, nodes and edges belong inside `graph`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `schema` | URL | Yes | URL of the ODPG schema used for validation |
| `version` | String | Yes | Version of the ODPG specification, for example `"1.0"` |
| `kind` | String | Yes | Type of graph specification document. Must be `Graph` |
| `graph` | Object | Yes | Container for graph metadata, nodes, and edges |
| `graph.metadata` | Object | Yes | Metadata describing the graph |
| `graph.metadata.id` | String | Yes | Unique identifier of the graph |
| `graph.metadata.name` | Object | Yes | Human-readable graph name using language-specific values |
| `graph.metadata.name.en` | String | No | English name; at least one supported language key is required. |
| `graph.metadata.description` | Object | Yes | Human-readable graph description using language-specific values |
| `graph.metadata.description.en` | String | No | English description; at least one supported language key is required. |
| `graph.nodes` | Array of node objects | Yes | Collection of graph node objects |
| `graph.edges` | Array of edge objects | Yes | Collection of graph edge objects |

## Optional attributes and options

> Example of catalog metadata usage:

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
      en: Graph describing how aviation data products, use cases, policies, agents, opportunities, and business objectives are connected.
    domain:
      en: Aviation
    purpose:
      en: Support portfolio analysis, value mapping, governance review, and AI-assisted reasoning.
    tags:
      - aviation
      - predictive-maintenance
      - fleet-availability
    status: draft
    visibility: public
    owner:
      name: Aviation Data Product Team
      email: aviation-data-products@example.com
  nodes: []
  edges: []
```

| Attribute                 | Type             | Description                                                                                                      |
| ------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------- |
| `graph.metadata.domain`         | Object           | Business, industry, or subject domain covered by the graph. Supports language-specific values.                   |
| `graph.metadata.domain.en`      | String           | English domain name.                                                                                             |
| `graph.metadata.purpose`        | Object           | Explanation of why the graph exists and how it should be used. Supports language-specific values.                |
| `graph.metadata.purpose.en`     | String           | English purpose statement.                                                                                       |
| `graph.metadata.tags`           | Array of strings | Keywords used for discovery, filtering, grouping, and search.                                                    |
| `graph.metadata.status`         | String           | Current status of the graph. Allowed values are `draft`, `active`, `deprecated`, and `archived`.         |
| `graph.metadata.visibility`     | String           | Intended visibility of the graph. Allowed values are `public`, `internal`, `restricted`, and `private`.  |
| `graph.metadata.owner`          | Object           | Party responsible for the graph.                                                                                 |
| `graph.metadata.owner.name`     | String           | Name of the owning person, team, or organization; required when owner is supplied.                                                                |
| `graph.metadata.owner.email`    | String           | Contact email for the owning party.                                                                              |

Graph lifecycle `graph.metadata.status` is distinct from an assertion's
`reviewStatus`. The schema enforces the listed lifecycle and visibility values;
neither property grants access.

Optional draft profiles add `graph.metadata.x-odpg-profiles` (an array of unique
profile identifiers). This is an extension, not a new required core field.
The shared validator supports `odpg-value-evidence-0.1` and rejects unknown
declared profiles. Node and edge extensions such as `x-odpg-assertion` and
`x-odpg-value` are described in the Nodes, Edges, Specification extensions, and
Adoption and Evidence Profiles sections. Document-level `x-` fields are forbidden.
