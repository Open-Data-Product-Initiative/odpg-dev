<!-- Authorship: Zaher Abou Shakra -->
# Adoption and Evidence Profiles

ODPG is a storage-neutral portfolio and decision-context graph. It connects
enterprise assets, strategic objectives, evidence pointers, and accountable
decisions. It complements catalogs, lineage systems, observability platforms,
and access-control infrastructure. A relationship is a claim; it does not by
itself demonstrate business value, observed execution, compliance, or permission.

## Architecture boundary

| Responsibility | Authoritative system | ODPG responsibility |
| --- | --- | --- |
| Product metadata and discovery | ODPS, ODPC, DCAT-compatible catalogs | Reference products and catalog resources |
| Provenance and lineage | PROV and OpenLineage implementations | Link claims to source entities, activities, jobs and runs |
| Strategic and operating context | ODPG | Describe relationships, value hypotheses and review decisions |
| Agent execution | Agent runtime and tool infrastructure | Reference definitions, runs, evaluations and outcomes |
| Authentication and authorization | MCP/API infrastructure and policy enforcement | Document relevant policies and required approvals |
| Telemetry | OpenTelemetry-compatible systems | Reference trace IDs and evidence locations |

These are mappings of responsibility, not claims of implemented adapters.
OpenLineage distinguishes static jobs from observed runs; PROV distinguishes
entities, activities and agents. An ODPG `Agent` is not automatically equivalent
to every use of the term agent in PROV.

## Fifteen-minute quick start

Install the toolkit dependencies and create a YAML document:

Run from the repository root using Python 3.11, the version used by CI. Keep
`source/scripts/odpg_toolkit_core.py` and `source/scripts/odpg_profiles.py` beside
the CLI scripts, with `source/schema/` at its repository location. The shared
toolkit needs both PyYAML and `jsonschema[format]`; the manifest below also
installs pytest and pytest-cov for conformance tests. Required Dependencies &
Execution contains the full runtime layout and a runtime-only installation command.

```bash
python -m pip install -r requirements-dev.txt
```

```yaml
schema: https://opendataproducts.org/odpg-v1.0/schema/odpg.yaml
version: "1.0"
kind: Graph
graph:
  metadata:
    id: GRAPH-START
    name: {en: Maintenance portfolio}
    description: {en: Declared relationships to existing product resources.}
  nodes:
    - {id: UC-1, type: UseCase, $ref: ./usecases/maintenance.yaml}
    - {id: DP-1, type: DataProduct, $ref: ./products/maintenance.odps.yaml}
  edges:
    - {from: UC-1, to: DP-1, type: uses, confidence: high}
```

Replace the references with existing ODPS documents, ODPC resource locations,
or other authoritative resources. Save as `graph.yaml`, then run:

```bash
python source/scripts/odpg_validate.py -i graph.yaml
python source/scripts/odpg_traverse.py -i graph.yaml --start UC-1 --depth 1
```

Validation runs the bundled JSON Schema and graph integrity checks locally.
It does not fetch the `schema` URL, dereference resources, or authenticate evidence.
No graph database, RDF platform, or AI agent is required.

## Shared assertion contract 0.1 (draft)

Nodes and edges MAY carry `x-odpg-assertion`. The shared contract is published
at [assertion-0.1.json](/schema/profiles/assertion-0.1.json) and is validated
whenever that field is present, including on otherwise core-only graphs.

```yaml
x-odpg-assertion:
  id: CLAIM-MAINTENANCE-001
  origin: observed
  source: urn:example:maintenance-observer
  assertedAt: "2026-09-02T00:00:00Z"
  reviewStatus: accepted
  reviewer: Fleet review board
  reviewedAt: "2026-09-05T00:00:00Z"
  validFrom: "2026-09-05T00:00:00Z"
  validUntil: "2026-12-01T00:00:00Z"
  evidence:
    - uri: ./evidence/maintenance-report.json
```

| Field | Meaning |
| --- | --- |
| `id` | Stable claim identifier, unique across assertions in the graph |
| `origin` | `declared`, `observed`, or `inferred`; never overwritten by review |
| `source` | Absolute URI identifying the asserting source |
| `assertedAt` | Timestamp of the assertion |
| `reviewStatus` | `pending`, `accepted`, `rejected`, or `deferred` |
| `reviewer`, `reviewedAt` | Required for accepted, rejected and deferred claims |
| `validFrom`, `validUntil` | Optional validity window, inclusive start and exclusive end |
| `evidence` | URI references, optionally with `digest: sha256:<64 lowercase hex characters>` |

Observed and accepted claims require at least one evidence pointer. Times use
RFC 3339 with an explicit time zone. Digests identify content; validation does
not retrieve that content or establish its truth or the reviewer's authority.
Claims from different sources can coexist on separate edges with separate IDs.
The converter currently deduplicates equal edge triples and is a topology
importer, not an assertion-history importer.

Traversal preserves full assertion fields, including rejected claims, for
inspection. Analysis excludes explicitly unaccepted and out-of-window claims
from support counts. Legacy edges remain declared topology. The separate
`objectivesWithoutReviewedSupport` result requires accepted, current, evidenced
claims. Agent context includes `reviewedPaths` and a trust notice; review status
is self-reported metadata, not authenticated permission or production readiness.

`forwardPaths` and `reversePaths` preserve all traversed edge metadata, including
unaccepted claims. `reviewedPaths` filters edge assertions for acceptance,
evidence pointers and the current validity window. `governanceSignals` reports
policy links in the unfiltered forward paths; it is not a list of enforced or
approved controls. `analysisBasis` explains the topology/review distinction.

## Value Evidence profile 0.1 (draft)

Declare the optional profile inside metadata; document-level extensions are
not permitted by the unchanged core schema:

```yaml
graph:
  metadata:
    x-odpg-profiles:
      - odpg-value-evidence-0.1
```

This is a fragment, not a complete graph. The profile node overlay is published
at [value-evidence-0.1.json](/schema/profiles/value-evidence-0.1.json).
Profile nodes retain core `id`, `type`, and `$ref` fields and put their additional
attributes under `x-odpg-value`. These types are profile vocabulary, not additions
to the core type list.

| Node type | Required profile fields |
| --- | --- |
| `ValueHypothesis` | `statement`, `objective`, `useCase`, `product`, `outcome`, `metric`, `baseline`, `target`, `measurements`, `reviewDecision` |
| `Outcome` | `description` |
| `MetricDefinition` | `definition`, `unit`, `direction` (`increase` or `decrease`), `aggregation` |
| `Baseline`, `Target` | `metric`, `value`, `unit`, `periodStart`, `periodEnd` |
| `Measurement` | Baseline fields plus `hypothesis`, `observedAt`, `attributionMethod`, `evidence` |
| `Evidence` | `uri`, `recordedAt`; optional `digest` |
| `ReviewDecision` | `hypothesis`, `decision` (`continue`, `change`, `stop`, `defer`), `reviewer`, `reviewedAt`, `evidence`, `rationale` |

Reference fields contain node IDs; `measurements` and `evidence` contain arrays
of IDs. Each listed type must be present in a conformant profile graph.
Metric, unit, period ordering, hypothesis identity and typed-reference checks
are performed by [`odpg_profiles.py`](/scripts/odpg_profiles.py) in addition to
JSON Schema. Invoke it through `odpg_validate.py`; the module has no standalone CLI.
Measurement, baseline and target values must be finite numbers. Required chain
edges may be legacy declared links or current, accepted assertions; explicitly
pending, rejected, deferred or out-of-window claims do not satisfy those chains.

The following directed edges must accompany the reference fields:

| Source | Relationship | Target |
| --- | --- | --- |
| Use case | `tests` | Hypothesis |
| Hypothesis | `supports` | Objective |
| Hypothesis | `uses` | Data product or capability |
| Hypothesis | `expects` | Outcome |
| Hypothesis | `measuredBy` | Metric definition |
| Hypothesis | `hasBaseline`, `hasTarget` | Corresponding baseline or target |
| Baseline, target, measurement | `measures` | Metric definition |
| Measurement | `tests` | Hypothesis |
| Measurement, review decision | `supportedBy` | Evidence |
| Review decision | `reviews` | Hypothesis |

A measurement may support or weaken a hypothesis. It MUST NOT automatically
establish business value or production readiness. The named decision authority
records a conclusion and rationale. A `continue` decision may mean continuing
a controlled experiment rather than approving production deployment.

## Reference example and CI reports

The [aviation graph](/examples/value-evidence/aviation.yaml) and its
[referenced resources](/examples/value-evidence/resources.yaml) are entirely
synthetic fixtures. They show two hypotheses: one with a fictional decision to
continue evaluation, and one deferred because the target was missed and
attribution remains uncertain. They are not observed customer outcomes.

```bash
python source/scripts/odpg_validate.py -i source/examples/value-evidence/aviation.yaml
python source/scripts/odpg_analyze.py -i source/examples/value-evidence/aviation.yaml
python -m pytest tests
```

Run `python -m pytest tests/test_odpg_adoption.py` for the focused profile and
publication-consistency checks. It verifies that the published section and
resource inventories, dependencies, vocabularies, output fields and examples
agree with the current schemas and toolkit. Graph Toolkit provides the JSON
output field reference; Required Dependencies & Execution lists setup commands.

The validator returns JSON with `valid`, `errors`, and `warnings`; declared
profiles also receive a `profiles` map. Exit status is zero only for a valid
document and supported profiles. Unknown profiles fail explicitly. JSON Schema
conformance and graph checks do not certify referenced content or business results.

## Composable adoption and future proposals

Core conformance is independent of optional profile conformance. An organisation
can adopt value evidence without deploying agents or runtime lineage. Profiles
will be independently versioned; no four-level maturity ladder is required.

| Package | Status |
| --- | --- |
| Core graph and local structural validation | Implemented |
| Shared assertion contract 0.1 | Draft, schema and validator implemented |
| Value Evidence (`odpg-value-evidence-0.1`) | Draft, schema, semantic validator and fixture implemented |
| Governed Agent (`odpg-governed-agent-0.1`) | Proposal only; not accepted by the validator |
| Observed Lineage (`odpg-observed-lineage-0.1`) | Proposal only; not accepted by the validator |
| RDF/SHACL, DCAT, PROV, OpenLineage, MCP and OpenTelemetry adapters | Future work; not implemented here |

The Governed Agent proposal should distinguish `Agent` from `AgentRun`,
`ToolCapability`, `Approval`, `PolicyDecision`, `Evaluation`, and trace references.
`Agent → uses → API` MUST NOT grant access. Enforce identity, scopes, and policy
at the MCP/API boundary. The Observed Lineage proposal should link job/run IDs,
PROV entities and activities, source versions and telemetry evidence without
copying complete runtime payloads or unrestricted prompts into the graph.

Before promoting profile fields into a future core version, validate their
semantics with at least two independent implementations. This repository's
fixture and validator constitute one reference implementation.

Alignment references: [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/),
[PROV](https://www.w3.org/TR/prov-primer/),
[OpenLineage](https://openlineage.io/docs/spec/object-model/),
[MCP authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
[OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/gen-ai/).
