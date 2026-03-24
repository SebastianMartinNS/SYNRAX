import json, sys
f = r"C:\Users\adria\synrax\_reference\codedna\benchmark_agent\runs\or-deepseek-v3.2\session_traces\bench_or-deepseek-v3.2_14480_synrax_runtime_20260323_144611_r0.json"
d = json.load(open(f, encoding="utf-8"))
print("Ground truth:", d["ground_truth"])
print("note_missing:", d.get("note_missing"))
print()
for s in d["trace"]:
    if s["tool"] == "read_file":
        rp = str(s.get("result_preview", ""))
        path = s["args"].get("path", "")
        has_nav = "Synrax Navigation" in rp or "Synrax" in rp
        chars = s.get("result_chars", 0)
        print(f"  {'NAV' if has_nav else '---'}  {path}  ({chars} chars)")
print()
# Check trace structure keys
if d["trace"]:
    print("Trace step keys:", list(d["trace"][0].keys()))
