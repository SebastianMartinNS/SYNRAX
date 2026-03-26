"""demo/demo_value.py — Dimostra concretamente il valore aggiunto di Synrax vs CodeDNA grezzo.

Esegui con:  py demo/demo_value.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from synrax.extract.pipeline import extract_codebase
from synrax.namespaces import ARCH, RDF
from synrax.query.engine import run_query
from synrax.schema.reasoner import reason
from synrax.schema.validator import validate

DEMO_ROOT = Path(__file__).parent / "codebase"
DEMO_TTL = Path(__file__).parent / "output.ttl"


def section(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def main():
    # =========================================================================
    # FASE 1: Cosa vede CodeDNA grezzo (solo testo statico nei file)
    # =========================================================================
    section("FASE 1 — CodeDNA GREZZO: cosa sai leggendo i file?")

    print("Leggendo i docstring del codebase, un agente vede:")
    print()
    print("  views/checkout.py")
    print("    exports: checkout_view(request)")
    print("    used_by: urls.py -> urlpatterns")
    print("    dipende da: forms/ (dal manifest)")
    print()
    print("  forms/order_form.py")
    print("    exports: validate_order, build_line_items")
    print("    used_by: views/checkout.py [cascade], notifications/email.py")
    print("    dipende da: models/ (dal manifest)")
    print()
    print("  DOMANDA: Se modifico db/connection.py, cosa si rompe?")
    print("  CON CODEDNA GREZZO: Non lo sai! Devi seguire la catena manualmente:")
    print("    db -> models (manifest) -> forms (manifest) -> views (manifest)")
    print("    ...ma il file 'notifications/email.py' dipende anche da models!")
    print("    Un agente deve aprire OGNI file e ricostruire il grafo a mano.")
    print()
    print("  DOMANDA: L'agente che ha modificato order_form.py ha visitato")
    print("           tutti i target [cascade]?")
    print("  CON CODEDNA GREZZO: Non c'è modo di verificarlo automaticamente.")

    # =========================================================================
    # FASE 2: Synrax estrae → grafi RDF formale
    # =========================================================================
    section("FASE 2 — SYNRAX EXTRACT: da testo a knowledge graph")

    graph = extract_codebase(DEMO_ROOT)
    raw_count = len(graph)

    modules = list(graph.subjects(RDF.type, ARCH.Module))
    packages = list(graph.subjects(RDF.type, ARCH.Package))
    rules = list(graph.subjects(RDF.type, ARCH.Rule))
    exports = list(graph.subjects(RDF.type, ARCH.Export))
    sessions = list(graph.subjects(RDF.type, ARCH.AgentSession))
    functions = list(graph.subjects(RDF.type, ARCH.Function))

    print(f"  Triple estratti:    {raw_count}")
    print(f"  Moduli:             {len(modules)}")
    print(f"  Package:            {len(packages)}")
    print(f"  Regole:             {len(rules)}")
    print(f"  Export:             {len(exports)}")
    print(f"  Sessioni agente:    {len(sessions)}")
    print(f"  Funzioni (L2):      {len(functions)}")

    # Salva versione non-ragionata
    graph_noreason = extract_codebase(DEMO_ROOT)

    # =========================================================================
    # FASE 3: OWL Reasoning — scopre dipendenze nascoste
    # =========================================================================
    section("FASE 3 — OWL REASONING: scopre cosa CodeDNA non vede")

    graph = reason(graph)
    reasoned_count = len(graph)
    inferred = reasoned_count - raw_count

    print(f"  Triple prima del reasoning:  {raw_count}")
    print(f"  Triple dopo il reasoning:    {reasoned_count}")
    print(f"  Triple INFERITI:             {inferred} (+{inferred * 100 // raw_count}%)")
    print()

    # Mostra dipendenze transitive
    print("  DIPENDENZE TRANSITIVE scoperte dal reasoning:")
    for s, _p, o in sorted(graph.triples((None, ARCH.dependsOn, None))):
        s_name = str(s).split("/")[-1]
        o_name = str(o).split("/")[-1]
        # Check if this was in the original graph
        is_inferred = (s, ARCH.dependsOn, o) not in graph_noreason
        marker = " ← INFERITO!" if is_inferred else ""
        print(f"    {s_name} dependsOn {o_name}{marker}")

    print()
    print("  PROPRIETÀ INVERSE (usedBy) inferite:")
    used_by_count = 0
    for s, _p, o in sorted(graph.triples((None, ARCH.usedBy, None))):
        s_name = str(s).split("/")[-1]
        o_name = str(o).split("/")[-1]
        print(f"    {s_name} usedBy {o_name}")
        used_by_count += 1
    print(f"  → {used_by_count} relazioni usedBy inferite automaticamente")

    # Salva per le query
    graph.serialize(destination=str(DEMO_TTL), format="turtle")

    # =========================================================================
    # FASE 4: SHACL Validation — cattura problemi di qualità
    # =========================================================================
    section("FASE 4 — SHACL VALIDATION: qualità delle annotazioni")

    report = validate(graph)

    print(f"  Conforms:     {report['conforms']}")
    print(f"  Violations:   {report['statistics']['violations_count']}")
    print(f"  Warnings:     {report['statistics']['warnings_count']}")
    print(f"  Tempo:        {report['statistics']['validator_time_ms']}ms")

    if report["violations"]:
        print()
        print("  VIOLAZIONI trovate:")
        for v in report["violations"]:
            node = v.get("focusNode", "?").split("/")[-1]
            msg = v.get("resultMessage", "?")
            print(f"    ❌ {node}: {msg}")

    if report["warnings"]:
        print()
        print("  WARNING:")
        for w in report["warnings"]:
            node = w.get("focusNode", "?").split("/")[-1]
            msg = w.get("resultMessage", "?")
            print(f"    ⚠️  {node}: {msg}")

    print()
    print("  → Synrax cattura annotazioni incomplete AUTOMATICAMENTE.")
    print("    Il paper dice: 'wrong rules is worse than none'")
    print("    Con SHACL lo verifichi in CI, non a mano.")

    # =========================================================================
    # FASE 5: SPARQL Queries — risposte che CodeDNA non può dare
    # =========================================================================
    section("FASE 5 — SPARQL QUERIES: domande impossibili senza Synrax")

    # 5a. Impact analysis
    print("  Q1: 'Cosa si rompe se modifico db/connection.py?'")
    print("  (CodeDNA: devi leggere ogni file. Synrax: una query SPARQL)")
    print()

    # Find the db/connection module URI
    db_module = None
    for s, _p, o in graph.triples((None, ARCH.moduleName, None)):
        if "connection" in str(o):
            db_module = str(s).split("/")[-1]
            break

    if db_module:
        results = run_query("impact_analysis", DEMO_TTL, module=db_module)
        if results:
            print(f"  Moduli impattati da {db_module}:")
            for r in results:
                print(f"    → {r.get('name', '?')}")
        else:
            print(f"  Nessun modulo dipende direttamente da {db_module}")
            print("  (Le dipendenze transitive sono nei package-level dependsOn)")

    # 5b. Unused modules
    print()
    print("  Q2: 'Quali moduli sono orfani? (nessuno dipende da loro)'")
    results = run_query("unused_modules", DEMO_TTL)
    if results:
        for r in results:
            print(f"    🔍 {r.get('name', '?')}")
    else:
        print("    Nessun modulo orfano")

    # 5c. Circular deps
    print()
    print("  Q3: 'Ci sono dipendenze circolari?'")
    results = run_query("circular_deps", DEMO_TTL)
    if results:
        for r in results:
            print(f"    ⚠️  {r.get('cycle', '?')}")
    else:
        print("    ✅ Nessuna dipendenza circolare")

    # 5d. Cascade violations
    print()
    print("  Q4: 'Qualche agente ha dimenticato di visitare un target [cascade]?'")
    results = run_query("cascade_violations", DEMO_TTL)
    if results:
        for r in results:
            mod = r.get("module", "?").split("/")[-1]
            target = r.get("cascade_target", "?").split("/")[-1]
            session = r.get("session", "?").split("/")[-1]
            print(f"    ❌ Sessione {session} ha visitato {mod}")
            print(f"       ma NON ha visitato il target cascade: {target}")
    else:
        print("    ✅ Nessuna violazione cascade")

    # =========================================================================
    # RIEPILOGO
    # =========================================================================
    section("RIEPILOGO: Cosa aggiunge Synrax a CodeDNA?")

    print("  ┌──────────────────────────┬─────────────┬─────────────┐")
    print("  │ Capacità                 │ CodeDNA raw │ Synrax      │")
    print("  ├──────────────────────────┼─────────────┼─────────────┤")
    print("  │ Annotazioni in-source    │     ✅      │     ✅      │")
    print("  │ Dipendenze dirette       │     ✅      │     ✅      │")
    print("  │ Dipendenze TRANSITIVE    │     ❌      │     ✅ OWL  │")
    print("  │ inverse (usedBy) auto    │     ❌      │     ✅ OWL  │")
    print("  │ Validazione qualità      │     ❌      │     ✅ SHACL│")
    print("  │ Impact analysis query    │     ❌      │     ✅ SPARQL│")
    print("  │ Circular dep detection   │     ❌      │     ✅ SPARQL│")
    print("  │ Cascade enforcement      │     ❌      │     ✅ SPARQL│")
    print("  │ Orphan module detection  │     ❌      │     ✅ SPARQL│")
    print("  │ Agent provenance graph   │   parziale  │     ✅ RDF  │")
    print("  │ Integrabile in CI        │     ❌      │     ✅ CLI  │")
    print("  └──────────────────────────┴─────────────┴─────────────┘")
    print()
    print(f"  Triple estratti:  {raw_count}")
    print(f"  Triple inferiti:  {inferred} (dal reasoning OWL)")
    print(f"  Totale:           {reasoned_count} triple nel knowledge graph")
    print()
    print("  Il paper mostra +13pp F1 sugli agenti con CodeDNA.")
    print("  Synrax aggiunge verifica formale, reasoning automatico,")
    print("  e query strutturate sopra quelle annotazioni.")


if __name__ == "__main__":
    main()
