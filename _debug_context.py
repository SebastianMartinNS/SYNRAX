"""Show the Synrax enrichment section only."""
import tempfile
from pathlib import Path
from benchmark_openrouter import _build_synthetic_codebase, build_synrax_context

tmp = tempfile.mkdtemp(prefix="synrax_ctx_")
root = _build_synthetic_codebase(Path(tmp))
ctx = build_synrax_context(root)

# Print ONLY the enrichment section (after the --- separator)
parts = ctx.split("---")
if len(parts) > 1:
    print(parts[1])
