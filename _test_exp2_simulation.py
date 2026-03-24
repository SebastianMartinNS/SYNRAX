"""Simulate realistic agent session on task 12508 to verify EXP-2 flow.

Ground truth files for 12508 (Add dbshell -c SQL argument):
  django/core/management/base.py
  django/core/management/commands/dbshell.py
  django/db/backends/base/client.py
  django/db/backends/mysql/client.py
  django/db/backends/mysql/creation.py
  django/db/backends/oracle/client.py
  django/db/backends/postgresql/client.py
  django/db/backends/sqlite3/client.py
"""
import sys
sys.path.insert(0, r"c:\Users\adria\synrax\_reference\codedna\benchmark_agent\swebench")
sys.path.insert(0, r"c:\Users\adria\synrax")

from pathlib import Path
from synrax.runtime.session_graph import SessionGraph

cdna = Path(r"c:\Users\adria\synrax\_reference\codedna\benchmark_agent\projects_swebench\django__django-12508\codedna")
sg = SessionGraph(cdna)
sg.ingest_all()

# Import the benchmark functions we need to test
import importlib.util
spec = importlib.util.spec_from_file_location(
    "run_agent_multi",
    r"c:\Users\adria\synrax\_reference\codedna\benchmark_agent\swebench\run_agent_multi.py"
)
mod = importlib.util.module_from_spec(spec)
# We can't exec the module because it has heavy deps, so let's replicate _build_nav_hint logic

# Simulate agent reads in order (natural exploration path)
read_order = [
    "django/core/management/commands/dbshell.py",   # 1st: start from the command
    "django/db/backends/base/client.py",             # 2nd: follow the base client
    "django/db/backends/mysql/client.py",            # 3rd: follow mysql backend
    "django/db/backends/postgresql/client.py",       # 4th: postgresql backend
    "django/db/backends/oracle/client.py",           # 5th: oracle backend
    "django/db/backends/sqlite3/client.py",          # 6th: sqlite3 backend
    "django/core/management/base.py",                # 7th: management base
    "django/db/backends/mysql/creation.py",          # 8th: mysql creation (tricky)
]

from synrax.runtime.tools import _module_uri_fragment

print("=" * 80)
print("SIMULATED AGENT SESSION — Task 12508 (dbshell -c)")
print("=" * 80)

for i, path in enumerate(read_order, 1):
    sg.ingest_file(path)
    sg.mark_visited(path)
    
    # What the agent would see
    uri = _module_uri_fragment(path)
    
    # Get impacted files
    try:
        impact = sg.query_template("impact_analysis", module=uri)
        impact_names = [r.get("name", "?") for r in impact]
    except Exception:
        impact_names = []
    
    # Get dependencies
    try:
        deps = sg.query_template("deps_of", module=uri)
        dep_names = [r.get("name", "?") for r in deps]
    except Exception:
        dep_names = []
    
    # Get edge labels
    tagged_impact = []
    for n in impact_names[:3]:
        key = (n, path)
        label = sg._edge_sources.get(key, "")
        tagged_impact.append(f"{n} ({label})" if label else n)
    
    tagged_deps = []
    for n in dep_names[:5]:
        key = (path, n)
        label = sg._edge_sources.get(key, "")
        tagged_deps.append(f"{n} ({label})" if label else n)
    
    print(f"\n--- Read #{i}: {path} ---")
    print(f"  Used by ({len(impact_names)}): {', '.join(tagged_impact)}")
    if len(impact_names) > 3:
        print(f"    (+{len(impact_names) - 3} more)")
    print(f"  Depends on ({len(dep_names)}): {', '.join(tagged_deps)}")
    
    # Boundary check (activates after 2 files with new threshold)
    if len(sg._visited_files) >= 2:
        boundary = sg.get_boundary_status()
        pct = boundary.get("explored_pct", 0)
        remaining = boundary.get("remaining_in_scope", [])
        out = boundary.get("out_of_scope_sample", [])
        print(f"  [Boundary] {pct}% explored | {len(remaining)} remaining in scope | {len(out)} out of scope")
        if remaining:
            print(f"    Remaining: {', '.join(remaining[:5])}")
        if out:
            print(f"    Out of scope (skip): {', '.join(out[:3])}")

gt_files = set(read_order)
visited = sg._visited_files
print(f"\n{'=' * 80}")
print(f"FINAL: Visited {len(visited)} files")
print(f"  Ground truth covered: {len(gt_files & visited)}/{len(gt_files)}")
boundary_final = sg.get_boundary_status()
print(f"  Final explored_pct: {boundary_final.get('explored_pct', 0)}%")
print(f"  Remaining in scope: {boundary_final.get('remaining_in_scope', [])[:5]}")
