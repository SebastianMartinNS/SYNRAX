"""Quick perf test for EXP-2 boundary analysis on task 12508."""
from pathlib import Path
from synrax.runtime.session_graph import SessionGraph
import time

cdna = Path(r"c:\Users\adria\synrax\_reference\codedna\benchmark_agent\projects_swebench\django__django-12508\codedna")
sg = SessionGraph(cdna)

t0 = time.perf_counter()
n = sg.ingest_all()
t1 = time.perf_counter()
print(f"Ingested {sg.file_count} files, {sg.raw_triple_count} raw triples in {t1-t0:.2f}s")

# Test boundary status performance with 2 visited files (new threshold)
sg.mark_visited("django/core/management/commands/dbshell.py")
sg.mark_visited("django/db/backends/base/client.py")

t4 = time.perf_counter()
boundary = sg.get_boundary_status()
t5 = time.perf_counter()
print(f"Boundary status in {t5-t4:.2f}s")
pct = boundary.get("explored_pct", "?")
remaining = boundary.get("remaining_in_scope", [])
out = boundary.get("out_of_scope_sample", [])
print(f"  explored_pct: {pct}%")
print(f"  remaining_in_scope ({len(remaining)}): {remaining[:10]}")
print(f"  out_of_scope_sample ({len(out)}): {out[:10]}")

# Test classify_node_roles
t6 = time.perf_counter()
roles = sg.classify_node_roles()
t7 = time.perf_counter()
hubs = [n for n, r in roles.items() if r == "hub"]
leaves = [n for n, r in roles.items() if r == "leaf"]
connectors = [n for n, r in roles.items() if r == "connector"]
print(f"\nNode roles in {t7-t6:.2f}s: {len(hubs)} hubs, {len(connectors)} connectors, {len(leaves)} leaves")
print(f"  Hubs: {hubs[:5]}")

# Test edge_sources
print(f"\nEdge sources tracked: {len(sg._edge_sources)}")
structural = sum(1 for v in sg._edge_sources.values() if v == "structural")
annotated = sum(1 for v in sg._edge_sources.values() if v == "annotated")
print(f"  structural: {structural}, annotated: {annotated}")
