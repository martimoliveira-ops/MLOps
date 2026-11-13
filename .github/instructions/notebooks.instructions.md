---
applyTo: 'notebooks/**/*.ipynb'
---

- When reviewing a notebook, read the `.ipynb` file on disk, including its saved outputs. If the outputs look stale, say so.
- Never print a whole DataFrame. Use `.head()`.
- Run notebooks top to bottom before committing, and keep the outputs. The charts are the deliverable.
- If a notebook is changed outside VS Code, the open tab won't reload it. Tell the owner to run **File: Revert File** before saving, or the saved changes will be overwritten.
- Keep notebooks to one analysis stage per PR.
