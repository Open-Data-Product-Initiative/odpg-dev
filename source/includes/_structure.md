# Specification Structure

An ODPG document consists of a standardized graph structure composed of metadata, graph nodes, and graph edges, where the graph itself represents a connected ecosystem of business, operational, technical, governance, and AI-related entities.

The root structure of an ODPG document is defined as follows:

> Example of details object usage:

```yml
schema: https://opendataproducts.org/odpg-v1.0/schema/graph.yaml
version: 1.0
kind: DataProductGraph
id: GRAPH-AVIATION-001
name:
  en: Aviation Data Product Value Graph
nodes: []
edges: []
```


## Mandatory attributes

The following root properties are defined within an ODPG document.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| **schema** | URL | Yes | URL of the ODPG schema used for validation |
| **version** | String or number | Yes | Version of the ODPG specification |
| **kind** | String | Yes | Type of graph specification document. Must be `DataProductGraph` |
| **id** | String | Yes | Unique identifier of the graph |
| **name** | Object | Yes | Human-readable graph name using language-specific values |
| **nodes** | Array | Yes | Collection of graph nodes |
| **edges** | Array | Yes | Collection of graph edges |
