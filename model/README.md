# Model files (not committed by default)

The API expects trained weights here:

- `best_model.keras` **or** `final_model.keras`
- `class_indices.json`

`.gitignore` excludes `*.keras` so large files stay out of Git. For **Render** (or GitHub):

1. **Option A — Git LFS:** Track `*.keras` with [Git LFS](https://git-lfs.github.com/) and push.
2. **Option B — Commit if small:** If under ~100MB per file, temporarily allow the file in `.gitignore` and commit.
3. **Option C — Upload after deploy:** Use Render Shell or a release step to copy models into `/opt/render/project/src/model` (path may vary).

Without these files, `/health` will show `model_loaded: false` and `/predict` will fail.
