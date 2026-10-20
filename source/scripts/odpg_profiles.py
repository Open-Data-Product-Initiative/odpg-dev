# Authorship: Zaher Abou Shakra
"""Local-only draft profile validation. Evidence pointers never grant authority."""
import json
import math
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

PROFILE_ID = "odpg-value-evidence-0.1"
PROFILE_NODE_TYPES = {"ValueHypothesis", "Outcome", "MetricDefinition", "Baseline", "Target", "Measurement", "Evidence", "ReviewDecision"}
PROFILE_EDGE_TYPES = {"tests", "expects", "measuredBy", "hasBaseline", "hasTarget", "supportedBy", "reviews"}
SCHEMA_DIRECTORY = Path(__file__).resolve().parents[1] / "schema/profiles"


@lru_cache(maxsize=None)
def validator(filename):
    # Only filenames from the implementation are passed here, never graph URLs.
    schema = json.loads((SCHEMA_DIRECTORY / filename).read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_errors(value, filename, prefix=""):
    errors = sorted(validator(filename).iter_errors(value), key=lambda error: str(list(error.absolute_path)))
    return [f"{prefix}{'/'.join(map(str, error.absolute_path)) or '/'}: {error.message}" for error in errors]


def declared_profiles(document):
    if not isinstance(document, dict):
        return []
    graph = document.get("graph")
    metadata = graph.get("metadata") if isinstance(graph, dict) else None
    profiles = metadata.get("x-odpg-profiles", []) if isinstance(metadata, dict) else []
    return profiles if isinstance(profiles, list) and all(isinstance(p, str) for p in profiles) else []


def timestamp(value):
    return datetime.fromisoformat(value.upper().replace("Z", "+00:00"))


def assertion_is_active(edge, now=None):
    claim = edge.get("x-odpg-assertion")
    if claim is None:
        return True  # Legacy relationships remain declared topology only.
    if schema_errors(claim, "assertion-0.1.json"):
        return False
    if claim["reviewStatus"] != "accepted":
        return False
    now = now or datetime.now(timezone.utc)
    return (("validFrom" not in claim or timestamp(claim["validFrom"]) <= now)
            and ("validUntil" not in claim or now < timestamp(claim["validUntil"])))


def assertion_is_reviewed(edge):
    claim = edge.get("x-odpg-assertion")
    return bool(claim and assertion_is_active(edge) and claim.get("evidence"))


def validate_profiles(document):
    graph = document["graph"]
    errors = []
    profiles = declared_profiles(document)
    declaration = graph["metadata"].get("x-odpg-profiles", [])
    if declaration != profiles or len(profiles) != len(set(profiles)):
        errors.append("graph/metadata/x-odpg-profiles: expected unique profile identifiers")
    for profile in profiles:
        if profile != PROFILE_ID:
            errors.append(f"Unsupported profile: {profile}; conformance cannot be established")
    ids = set()
    for collection in ("nodes", "edges"):
        for index, item in enumerate(graph[collection]):
            if "x-odpg-assertion" not in item:
                continue
            claim = item["x-odpg-assertion"]
            location = f"graph/{collection}/{index}/x-odpg-assertion/"
            issues = schema_errors(claim, "assertion-0.1.json", location)
            errors.extend(issues)
            if issues:
                continue
            if claim["id"] in ids:
                errors.append(f"{location}id: duplicate assertion id {claim['id']}")
            ids.add(claim["id"])
            if "validFrom" in claim and "validUntil" in claim and timestamp(claim["validUntil"]) <= timestamp(claim["validFrom"]):
                errors.append(f"{location}validUntil: must follow validFrom")
    if PROFILE_ID in profiles:
        errors.extend(validate_value_graph(graph))
    elif any("x-odpg-value" in n for n in graph["nodes"]):
        errors.append(f"x-odpg-value requires declared profile {PROFILE_ID}")
    return errors


def validate_value_graph(graph):
    errors = []
    nodes = {n["id"]: n for n in graph["nodes"]}
    links = {(e["from"], e["type"], e["to"]) for e in graph["edges"] if assertion_is_active(e)}
    profile_nodes = [n for n in graph["nodes"] if n["type"] in PROFILE_NODE_TYPES]
    for kind in sorted(PROFILE_NODE_TYPES):
        if not any(n["type"] == kind for n in profile_nodes):
            errors.append(f"{PROFILE_ID}: missing node type {kind}")
    for node in profile_nodes:
        errors.extend(schema_errors(node, "value-evidence-0.1.json", f"nodes/{node['id']}/"))
    if errors:
        return errors

    def reference(node, field, expected, relationship=None, reverse=False):
        value = node["x-odpg-value"][field]
        values = value if isinstance(value, list) else [value]
        for target in values:
            linked = nodes.get(target)
            if not linked or linked["type"] not in expected:
                errors.append(f"nodes/{node['id']}/{field}: expected {sorted(expected)} reference, got {target}")
            if relationship:
                link = (target, relationship, node["id"]) if reverse else (node["id"], relationship, target)
                if link not in links:
                    errors.append(f"nodes/{node['id']}/{field}: missing active edge {link}")

    for node in profile_nodes:
        kind, data = node["type"], node["x-odpg-value"]
        if kind == "ValueHypothesis":
            for field, expected, rel, reverse in (
                ("objective", {"BusinessObjective"}, "supports", False),
                ("useCase", {"UseCase"}, "tests", True),
                ("product", {"DataProduct", "Capability"}, "uses", False),
                ("outcome", {"Outcome"}, "expects", False),
                ("metric", {"MetricDefinition"}, "measuredBy", False),
                ("baseline", {"Baseline"}, "hasBaseline", False),
                ("target", {"Target"}, "hasTarget", False),
                ("measurements", {"Measurement"}, "tests", True),
                ("reviewDecision", {"ReviewDecision"}, "reviews", True),
            ):
                reference(node, field, expected, rel, reverse)
            # The hypothesis, measurements, and decision must describe the same case.
            for field in ("baseline", "target", "measurements"):
                values = data[field] if isinstance(data[field], list) else [data[field]]
                for identifier in values:
                    other = nodes.get(identifier, {}).get("x-odpg-value", {})
                    if other.get("metric") != data["metric"]:
                        errors.append(f"nodes/{node['id']}/{field}: metric differs from hypothesis")
                    if field == "measurements" and other.get("hypothesis") != node["id"]:
                        errors.append(f"nodes/{node['id']}/{field}: hypothesis mismatch")
            decision = nodes.get(data["reviewDecision"], {}).get("x-odpg-value", {})
            if decision.get("hypothesis") != node["id"]:
                errors.append(f"nodes/{node['id']}/reviewDecision: hypothesis mismatch")
        elif kind in {"Baseline", "Target", "Measurement"}:
            if not math.isfinite(data["value"]):
                errors.append(f"nodes/{node['id']}/value: must be a finite number")
            reference(node, "metric", {"MetricDefinition"}, "measures")
            metric = nodes.get(data["metric"], {}).get("x-odpg-value", {})
            if data["unit"] != metric.get("unit"):
                errors.append(f"nodes/{node['id']}/unit: differs from metric")
            if timestamp(data["periodEnd"]) <= timestamp(data["periodStart"]):
                errors.append(f"nodes/{node['id']}/periodEnd: must follow periodStart")
            if kind == "Measurement":
                reference(node, "hypothesis", {"ValueHypothesis"}, "tests")
                reference(node, "evidence", {"Evidence"}, "supportedBy")
        elif kind == "ReviewDecision":
            reference(node, "hypothesis", {"ValueHypothesis"}, "reviews")
            reference(node, "evidence", {"Evidence"}, "supportedBy")
    return errors
