<!-- Authorship: Zaher Abou Shakra -->
# Graph Catalog

> Example of the catalog object usage:

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

  nodes:
    - id: UC-AVIATION-001
      type: UseCase
      $ref: ../usecases/predictive-maintenance-aircraft.yaml

    - id: OBJ-AVIATION-001
      type: BusinessObjective
      $ref: ../objectives/increase-fleet-availability.yaml

    - id: KPI-AVIATION-001
      type: KPI
      $ref: ../kpis/fleet-availability-rate.yaml

    - id: DP-AVIATION-001
      type: DataProduct
      $ref: ../products/aircraft-maintenance-history.yaml

    - id: DP-AVIATION-002
      type: DataProduct
      $ref: ../products/aircraft-sensor-events.yaml

    - id: API-AVIATION-001
      type: API
      $ref: ../apis/maintenance-risk-score-api.yaml

    - id: POL-AVIATION-001
      type: Policy
      $ref: ../policies/aviation-data-quality-policy.yaml

    - id: AGENT-AVIATION-001
      type: Agent
      $ref: ../agents/maintenance-recommendation-agent.yaml

    - id: OPP-AVIATION-001
      type: StrategicOpportunity
      $ref: ../opportunities/reduce-unscheduled-maintenance.yaml

  edges:
    - from: UC-AVIATION-001
      to: DP-AVIATION-001
      type: uses
      confidence: high

    - from: UC-AVIATION-001
      to: DP-AVIATION-002
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

    - from: DP-AVIATION-002
      to: OBJ-AVIATION-001
      type: contributesTo
      confidence: medium

    - from: KPI-AVIATION-001
      to: OBJ-AVIATION-001
      type: measures
      confidence: high

    - from: DP-AVIATION-001
      to: KPI-AVIATION-001
      type: tracks
      confidence: medium

    - from: DP-AVIATION-001
      to: API-AVIATION-001
      type: exposes
      confidence: high

    - from: DP-AVIATION-001
      to: POL-AVIATION-001
      type: governedBy
      confidence: high

    - from: AGENT-AVIATION-001
      to: DP-AVIATION-001
      type: uses
      confidence: high

    - from: AGENT-AVIATION-001
      to: API-AVIATION-001
      type: uses
      confidence: high

    - from: UC-AVIATION-001
      to: OPP-AVIATION-001
      type: identifies
      confidence: medium

    - from: OPP-AVIATION-001
      to: OBJ-AVIATION-001
      type: alignsWith
      confidence: medium
```
The following example demonstrates a complete ODPG document connecting use cases, business objectives, KPIs, data products, governance policies, APIs, AI agents, and strategic opportunities into a unified value graph.

![Aviation Data Product Value Graph](/images/aviation_example_relatiionship.png)

## Graph Explorer Example

The following YAML example can also be used as the input for a lightweight Graph Explorer generator capable of transforming an ODPG document into an interactive HTML-based visualization. This allows organizations to convert machine-readable graph specifications into human-readable graph catalogs that can be explored visually through a browser without requiring a dedicated graph database or enterprise catalog platform.

The Graph Explorer concept is intended to demonstrate how ODPG files can serve as portable relationship intelligence structures that support governance review, strategic planning, semantic exploration, AI-agent traversal, and operational dependency analysis through standard graph visualization techniques.

A Graph Explorer implementation typically performs the following sequence of operations:

Reads the ODPG YAML file.
Validates the graph with `odpg_validate.py` before generating the visualisation.
Extracts graph nodes and graph edges.
Converts the graph into a visualization-friendly structure.
Generates an interactive HTML page capable of displaying graph relationships.
Enables users to inspect node metadata, edge relationships, confidence levels, and referenced specifications.

The Graph Explorer may display:

* Data Products
* Use Cases
* Business Objectives
* KPIs
* Policies
* APIs
* Workflows
* Agents
* Strategic Opportunities

as graph nodes, while relationships such as:

* uses
* supports
* contributesTo
* governedBy
* tracks
* exposes
* identifies

can be rendered as directional graph edges.

## Purpose of the Graph Explorer

The purpose of the Graph Explorer is to provide a simple and portable way to inspect ODPG files visually. While ODPG is designed as a machine-readable specification, humans also need a practical way to understand how use cases, data products, objectives, policies, APIs, agents, and strategic opportunities are connected.

The Graph Explorer supports this need by converting the ODPG YAML structure into an interactive HTML page where users can inspect graph relationships, understand dependency paths, review contribution chains, and validate whether the graph communicates the intended business and governance context.


## Python Graph Explorer Generator

A lightweight Python utility can be used to transform an ODPG YAML document into a standalone HTML Graph Explorer.

The purpose of the script is not to redefine the ODPG structure, but rather to consume the existing specification and render it visually.

The script should:

* read the ODPG YAML file
* validate required graph properties
* validate node and edge integrity
* transform graph entities into visualization structures
* generate an HTML explorer
* render the graph interactively in a browser

The script should use the standard ODPG structure exactly as defined in this specification.


## Required Dependencies & Execution

Use Python 3.11, matching the version exercised by this repository's Python CI
job. Run the commands below from the repository root.

| Dependency | Required for |
| --- | --- |
| `PyYAML>=6.0` | Reading YAML in the toolkit, converter and explorer generator |
| `jsonschema[format]>=4.18,<5` | Bundled core JSON Schema and draft profile validation, including URI and timestamp formats |
| `pytest>=8.0` | Running the test suite; not required to execute the toolkit |
| `pytest-cov>=5.0` | Measuring test coverage and enforcing the CI coverage threshold |

Install the runtime and test dependencies from the repository's
`requirements-dev.txt`:

```bash
python -m pip install -r requirements-dev.txt
```

For runtime use without test tools, install only:

```bash
python -m pip install "PyYAML>=6.0" "jsonschema[format]>=4.18,<5"
```

The shared toolkit imports both modules below, even for core-only graphs.
They are supporting modules, not separate command-line entry points:

| Module | Responsibility |
| --- | --- |
| [`odpg_toolkit_core.py`](/scripts/odpg_toolkit_core.py) | Shared graph loading, core validation, summaries, traversal, analysis and context extraction |
| [`odpg_profiles.py`](/scripts/odpg_profiles.py) | Loads local schemas; validates the assertion contract and declared Value Evidence profile; checks claim validity and reviewed status |

Keep the repository layout when running the toolkit. Downloading a single CLI
script is insufficient: the shared modules and the schemas they load must be
available at their relative locations.

```text
source/
  scripts/
    odpg_validate.py
    odpg_toolkit_core.py
    odpg_profiles.py
    ... other toolkit scripts
  schema/
    odpg.json
    odpg.yaml
    profiles/
      assertion-0.1.json
      value-evidence-0.1.json
  examples/value-evidence/
    aviation.yaml
    resources.yaml
```

`odpg.json` is the core schema executed by the Python validator; `odpg.yaml`
publishes the equivalent core constraints in YAML. The assertion schema is
checked whenever `x-odpg-assertion` is present. The Value Evidence node overlay
and semantic checks apply when `odpg-value-evidence-0.1` is declared under
`graph.metadata.x-odpg-profiles`. The aviation graph and its referenced resources
are synthetic examples, not runtime dependencies.

Validate a graph before generating an explorer:

```bash
python source/scripts/odpg_validate.py -i source/examples/value-evidence/aviation.yaml
python source/scripts/generate_graph_explorer.py --help
python source/scripts/generate_graph_explorer.py -i source/examples/value-evidence/aviation.yaml -o graph-explorer.html
```

The validator returns JSON and exits with status 1 on failed conformance. The
explorer generator performs its own basic graph checks; it does not execute the
shared core/profile validator or authenticate evidence. A rendered graph is not
a conformance report. Its generated HTML loads vis-network from jsDelivr, so
that external resource must be reachable to view the graph.

| Script | Purpose |
|---|---|
| [`odpg_validate.py`](/scripts/odpg_validate.py) | Validate the bundled core schema, graph integrity, assertions and supported declared profiles; emit JSON conformance results |
| [`odpg_convert.py`](/scripts/odpg_convert.py) | Convert JSON-LD, GraphML, GraphSON, RDF, OpenCypher, GQL and Gremlin topology into ODPG YAML |
| [`odpg_summary.py`](/scripts/odpg_summary.py) | Summarize graph metadata and node, edge, type and confidence counts |
| [`odpg_traverse.py`](/scripts/odpg_traverse.py) | Discover relationship paths while preserving assertion and extension fields |
| [`odpg_analyze.py`](/scripts/odpg_analyze.py) | Report topology gaps and objectives without reviewed support separately |
| [`odpg_agent_context.py`](/scripts/odpg_agent_context.py) | Extract graph context with assertion metadata, `reviewedPaths` and a `trustNotice` |
| [`generate_graph_explorer.py`](/scripts/generate_graph_explorer.py) | Generate an HTML explorer after basic graph checks |

The resulting HTML file can be opened in a browser.

### Conformance tests and coverage

`tests/test_odpg_toolkit.py` covers the shared toolkit operations.
`tests/test_odpg_adoption.py` adds converter conformance, assertion validity,
profile chains, local resource references, CLI reports and complete documentation
graph snippets. Python CI runs both and requires at least 80% combined coverage
for `odpg_toolkit_core` and `odpg_profiles`:

```bash
python -m pytest tests --cov=odpg_toolkit_core --cov=odpg_profiles --cov-report=term-missing --cov-fail-under=80
```

For the focused adoption and publication-consistency audit, run
`python -m pytest tests/test_odpg_adoption.py`. This checks the published
inventories, dependency table, vocabulary, profile status, output field reference
and example conformance. See Graph Toolkit for the JSON output field reference.

### Quick reference

These flags refer to `generate_graph_explorer.py`; other CLI scripts expose
their own `--help`.

| Flag | Meaning |
|------|--------|
| `-i PATH` or `--input PATH` | ODPG graph YAML file to read |
| `-o PATH` or `--output PATH` | HTML file to write |
| `-h` or `--help` | Show help and defaults |

**Defaults:** if you omit `-i`, the script uses `graph.yaml` **in the same directory as** `generate_graph_explorer.py`. If you omit `-o`, it writes **`graph-explorer.html`** in the **current working directory**.

## Graph Explorer Capabilities

A generated Graph Explorer implementation may support:

* node visualization
* edge visualization
* relationship labels
* confidence display
* node grouping by type
* graph zooming and panning
* graph traversal
* dependency inspection
* governance inspection
* AI-agent relationship visualization
* clickable specification references

The Graph Explorer demonstrates how ODPG specifications can become both machine-readable and human-navigable while preserving interoperability with the broader Open Data Products ecosystem.

<a href="graph/examples/graph-explorer.html" target="_blank" rel="noopener noreferrer">
  <img src="images/graph_example_1.png" alt="Aviation Data Product Graph Explorer">
</a>

<a href="graph/examples/graph-explorer.html" target="_blank" rel="noopener noreferrer">Open the Graph Explorer example</a>
