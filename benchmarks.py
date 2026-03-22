"""benchmarks.py — Collect real benchmark metrics: CodeDNA vs Synrax."""

import time
from pathlib import Path

from rdflib import Graph, Literal
from rdflib.namespace import XSD

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF, bind_namespaces
from synrax.query.engine import run_query
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate

DEMO = Path("demo/codebase")
TTL = Path("demo/output.ttl")


def main():
    # === BENCHMARK 1: Triple Amplification ===
    raw = extract_codebase(DEMO)
    raw_count = len(raw)
    reasoned = extract_codebase(DEMO)
    t0 = time.monotonic()
    reason(reasoned)
    reason_ms = round((time.monotonic() - t0) * 1000)
    reasoned_count = len(reasoned)
    inferred = reasoned_count - raw_count

    print("=" * 60)
    print("  BENCHMARK 1: Knowledge Amplification")
    print("=" * 60)
    print(f"  Raw triples (CodeDNA extract):  {raw_count}")
    print(f"  Reasoned triples (Synrax OWL):  {reasoned_count}")
    print(f"  Inferred triples:               +{inferred}")
    print(f"  Amplification ratio:            {reasoned_count / raw_count:.1f}x")
    print(f"  Reasoning time:                 {reason_ms}ms")

    # === BENCHMARK 2: Entity Counts ===
    print()
    print("=" * 60)
    print("  BENCHMARK 2: Extracted Entities")
    print("=" * 60)
    for cls_name in ["Module", "Package", "Rule", "Export", "AgentSession", "Function"]:
        cls = ARCH[cls_name]
        raw_n = len(list(raw.subjects(RDF.type, cls)))
        rsn_n = len(list(reasoned.subjects(RDF.type, cls)))
        print(f"  {cls_name:16s}  raw={raw_n:3d}  reasoned={rsn_n:3d}")

    # === BENCHMARK 3: Inverse Relations ===
    print()
    print("=" * 60)
    print("  BENCHMARK 3: Inverse Relations (usedBy)")
    print("=" * 60)
    raw_ub = len(list(raw.triples((None, ARCH.usedBy, None))))
    rsn_ub = len(list(reasoned.triples((None, ARCH.usedBy, None))))
    print(f"  usedBy triples (raw):       {raw_ub}")
    print(f"  usedBy triples (reasoned):  {rsn_ub}")
    print(f"  NEW inverse relations:      +{rsn_ub - raw_ub}")

    # === BENCHMARK 4: Transitive Dependencies ===
    print()
    print("=" * 60)
    print("  BENCHMARK 4: Transitive Dependencies")
    print("=" * 60)
    raw_deps = list(raw.triples((None, ARCH.dependsOn, None)))
    rsn_deps = list(reasoned.triples((None, ARCH.dependsOn, None)))
    print(f"  dependsOn triples (raw):       {len(raw_deps)}")
    print(f"  dependsOn triples (reasoned):  {len(rsn_deps)}")
    print(f"  NEW transitive edges:          +{len(rsn_deps) - len(raw_deps)}")

    # === BENCHMARK 5: SHACL Validation ===
    print()
    print("=" * 60)
    print("  BENCHMARK 5: SHACL Validation")
    print("=" * 60)
    t0 = time.monotonic()
    report = validate(reasoned)
    val_ms = round((time.monotonic() - t0) * 1000)
    print(f"  Conforms:      {report['conforms']}")
    print(f"  Violations:    {report['statistics']['violations_count']}")
    print(f"  Warnings:      {report['statistics']['warnings_count']}")
    print(f"  Validation ms: {val_ms}ms")

    # === BENCHMARK 6: SPARQL Query Capabilities ===
    print()
    print("=" * 60)
    print("  BENCHMARK 6: SPARQL Query Capabilities")
    print("=" * 60)
    reasoned.serialize(destination=str(TTL), format="turtle")

    # Find module URIs
    for s, p, o in reasoned.triples((None, ARCH.moduleName, None)):
        uri_frag = str(s).split("/")[-1]
        results = run_query("impact_analysis", TTL, module=uri_frag)
        if results:
            print(f"  Impact of {str(o):30s}: {len(results)} modules affected")

    results = run_query("unused_modules", TTL)
    print(f"  Orphan modules: {len(results)}")
    for r in results:
        print(f"    - {r.get('name', '?')}")

    results = run_query("circular_deps", TTL)
    print(f"  Circular dependencies: {len(results)}")

    results = run_query("cascade_violations", TTL)
    print(f"  Cascade violations: {len(results)}")

    # === BENCHMARK 7: Transitive Reach (synthetic) ===
    print()
    print("=" * 60)
    print("  BENCHMARK 7: Transitive Reach (5-node chain)")
    print("=" * 60)
    g = Graph()
    bind_namespaces(g)
    for n in ["A", "B", "C", "D", "E"]:
        g.add((ARCH[n], RDF.type, ARCH.Module))
        g.add((ARCH[n], ARCH.moduleName, Literal(n, datatype=XSD.string)))
        g.add((ARCH[n], ARCH.purpose, Literal(f"Mod {n}", datatype=XSD.string)))
    for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]:
        g.add((ARCH[a], ARCH.dependsOn, ARCH[b]))
    before = len(set(o for _, _, o in g.triples((ARCH.A, ARCH.dependsOn, None))))
    reason(g)
    after = len(set(o for _, _, o in g.triples((ARCH.A, ARCH.dependsOn, None))))
    print(f"  A reach before reasoning: {before} node(s)")
    print(f"  A reach after reasoning:  {after} node(s)")
    print(f"  Reach amplification:      {after / before:.0f}x")

    # === BENCHMARK 8: Full Pipeline Timing ===
    print()
    print("=" * 60)
    print("  BENCHMARK 8: Full Pipeline Timing (E2E)")
    print("=" * 60)
    t0 = time.monotonic()
    g2 = extract_codebase(DEMO)
    t_extract = time.monotonic() - t0

    t1 = time.monotonic()
    reason(g2)
    t_reason = time.monotonic() - t1

    t2 = time.monotonic()
    rep = validate(g2)
    t_validate = time.monotonic() - t2

    g2.serialize(destination=str(TTL), format="turtle")
    t3 = time.monotonic()
    run_query("impact_analysis", TTL, module="db_connection")
    t_query = time.monotonic() - t3

    total = time.monotonic() - t0
    print(f"  Extract:    {t_extract * 1000:.0f}ms")
    print(f"  Reason:     {t_reason * 1000:.0f}ms")
    print(f"  Validate:   {t_validate * 1000:.0f}ms")
    print(f"  Query:      {t_query * 1000:.0f}ms")
    print(f"  TOTAL:      {total * 1000:.0f}ms")

    # === SUMMARY TABLE ===
    print()
    print("=" * 60)
    print("  SUMMARY: CodeDNA raw vs Synrax")
    print("=" * 60)
    rows = [
        ("Knowledge triples", str(raw_count), str(reasoned_count)),
        ("Transitive dep edges", str(len(raw_deps)), str(len(rsn_deps))),
        ("Inverse (usedBy) relations", str(raw_ub), str(rsn_ub)),
        ("Quality violations detected", "0", str(report["statistics"]["violations_count"])),
        ("Quality warnings detected", "0", str(report["statistics"]["warnings_count"])),
        ("SPARQL query types available", "0", "5"),
        ("Cycle detection", "none", "automatic"),
        ("Cascade enforcement", "none", "automatic"),
        ("Node reach (5-chain, A)", str(before), str(after)),
    ]
    print(f"  {'Metric':<35s} {'CodeDNA':>10s} {'Synrax':>10s}")
    print(f"  {'-' * 35} {'-' * 10} {'-' * 10}")
    for label, cd, sx in rows:
        print(f"  {label:<35s} {cd:>10s} {sx:>10s}")


if __name__ == "__main__":
    main()
