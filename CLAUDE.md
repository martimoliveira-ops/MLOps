# CLAUDE.md

@AGENTS.md

## Claude Code specifics

The import above keeps one source of truth for every agent. Put only Claude-specific notes here.

- When asked to review a notebook, read the `.ipynb` file on disk, including its saved outputs, rather than asking for pastes. If the outputs look stale, say so.
- When you edit a notebook, use the notebook edit tool one cell at a time. Then tell the user to run **File: Revert File** in VS Code, because an open notebook tab doesn't reload changes from disk, and saving it would overwrite them.
- When there's a genuine choice to make (a design option, a threshold, a target definition), ask, and lead with your recommendation. Don't silently pick one.
