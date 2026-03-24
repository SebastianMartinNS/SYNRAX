"""Debug script to check agent session extraction."""
import tempfile
from pathlib import Path
from benchmark_openrouter import MODULES, _build_synthetic_codebase, _clean_uri
from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF
from synrax.schema.reasoner import reason

tmp = tempfile.mkdtemp(prefix="synrax_dbg_")
root = _build_synthetic_codebase(Path(tmp))
graph = extract_codebase(root)
reason(graph)

# Check agent sessions
sessions = list(graph.subjects(RDF.type, ARCH.AgentSession))
print(f"Total AgentSessions: {len(sessions)}")

module_agents = {}
for s in sorted(sessions):
    name = str(s).split("/")[-1]
    belongs = list(graph.objects(s, ARCH.belongs))
    visited = list(graph.objects(s, ARCH.visited))
    print(f"\n  Session: {name}")
    print(f"    belongs: {[str(b).split('/')[-1] for b in belongs]}")
    print(f"    visited: {[str(v).split('/')[-1] for v in visited]}")
    if belongs:
        a = belongs[0]
        m = list(graph.objects(a, ARCH.agentModel))
        p = list(graph.objects(a, ARCH.agentProvider))
        print(f"    model: {[str(x) for x in m]}, provider: {[str(x) for x in p]}")

    if belongs and visited:
        mod = _clean_uri(visited[0])
        agent_uri = belongs[0]
        model_list = list(graph.objects(agent_uri, ARCH.agentModel))
        agent_model = str(model_list[0]) if model_list else "?"
        module_agents.setdefault(mod, []).append(agent_model)

print("\n\n=== Module -> Agents mapping ===")
for mod, agents in sorted(module_agents.items()):
    if len(agents) > 1:
        print(f"  MULTI: {mod} -> {agents}")
    else:
        print(f"  single: {mod} -> {agents}")
