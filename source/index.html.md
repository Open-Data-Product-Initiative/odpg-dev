---
title: Open (source) Data Product Graphs DRAFT | Linux Foundation

language_tabs: # must be one of [https://git.io/vQNgJ](https://git.io/vQNgJ)

  - yaml

toc_footers:
  - License [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
  - <br/><a href="https://opendataproducts.org">Specification home</a>
  - <br/>Linux Foundation

includes:
  - schemas

search: true

code_clipboard: true

meta:
  - name: description
    content: The Data Product Graphs Specification is a vendor-neutral, machine-readable graph model for managing data products, use cases, business objectives, KPIs, and their relationships. It defines the nodes, edges, attributes, and structures needed to connect data product lifecycle management with measurable business value.

---

# OPEN DATA PRODUCT GRAPHS - The Linux Foundation


## Version DRAFT

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in BCP 14 ([RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and [RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174)) when, and only when, they appear in all capitals, as shown here.

The specification is shared under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license.
Development of the specification is under the umbrella of the Linux Foundation.


| Topic            | Link                                                                                                | Description                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Version source   | [Open Data Product Graphs 1.0 on GitHub](https://github.com/Open-Data-Product-Initiative/odpg-v1.0) | Official source repository for the ODPG 1.0 specification     |
| ODPG YAML schema | [YAML Schema](https://opendataproducts.org/odpg-v1.0/odpg.yaml)                                     | Machine-readable schema definition in YAML format             |
| ODPG JSON schema | [JSON Schema](https://opendataproducts.org/odpg-v1.0/odpg.json)                                     | Machine-readable schema definition in JSON format             |
| Contribute       | [Raise an issue in GitHub](https://github.com/Open-Data-Product-Initiative/odpg-v1.0/issues)        | Submit issues or suggestions to the specification maintainers |


## Introduction

Modern organizations increasingly operate across highly distributed ecosystems composed of data products, APIs, workflows, governance controls, AI systems, analytical capabilities, business domains, and operational processes that collectively contribute to strategic business execution. Despite significant investments in data platforms and governance programs, many organizations still struggle to understand how technical assets connect to business value because metadata, governance, strategy, and operational context are often managed independently from one another.

Traditional metadata catalogs primarily focus on technical discovery, indexing, and lineage management, which makes them valuable for inventory and governance use cases but insufficient for understanding the broader strategic relationships that exist between business objectives, operational capabilities, AI systems, data products, and measurable outcomes.

**Open Data Product Graphs ODPG-v1.0** addresses this challenge by introducing a machine-readable graph specification that enables organizations to describe and manage the relationships between interconnected entities across the enterprise ecosystem, thereby transforming isolated specifications into connected intelligence structures capable of supporting governance reasoning, strategic alignment, semantic interoperability, AI traversal, impact analysis, and reusable data ecosystems.

Through ODPG, organizations can represent questions such as:

- Which use cases depend on this data product?
- Which business objectives are supported by this use case?
- Which KPIs are measured through these data products?
- Which data products contribute to the same strategic objective?
- Which AI agents are consuming these APIs?
- Which policies govern this workflow or domain?
- Which business areas contain unsupported strategic objectives?
- Which strategic opportunities emerge from multiple related use cases?

By enabling organizations to describe these relationships using a standardized graph structure, ODPG provides the foundation for graph-native enterprise intelligence ecosystems.
