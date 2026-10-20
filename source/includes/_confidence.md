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
# Confidence

> Example of YAML formated:

```yml
confidence: high
```

The confidence property records the asserting party's qualitative certainty in
a relationship. It does not independently encode whether the relationship is
declared, observed, or inferred, and does not establish evidence, approval,
authorization, or measured business value. The separate draft assertion
contract records origin and review status; legacy documents remain valid
without it, but their claims have no explicit evidence or review status.

The schema allows only the following confidence values.

| Value  | Description                                                             |
| ------ | ----------------------------------------------------------------------- |
| high   | Asserting party reports high certainty; evidence and review remain separate |
| medium | Asserting party reports moderate certainty |
| low    | Asserting party reports low certainty |

Earlier guidance associated high confidence with declared or confirmed edges,
and lower confidence with inference. Existing values are preserved; consumers
MUST NOT infer origin or acceptance from confidence alone. This clarification
does not retroactively certify legacy claims.

