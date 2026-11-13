---
name: notebook-review
description: Review a Jupyter notebook from disk, including its saved outputs, and flag stale outputs, out-of-order cells and whole-DataFrame prints. Use when the owner asks to review, check or read a notebook.
---

Read the notebook from disk with the Read tool, not from pasted text. The tool shows each cell with its saved outputs.

Check the following:

1. **Order.** Execution counts should run 1, 2, 3 with no gaps or repeats. If they don't, the notebook wasn't run top to bottom. Say so.
2. **Stale outputs.** Compare each output with the code above it. If a chart or number doesn't match the code, mark it stale. If a cell changed but its output didn't, say so.
3. **Printing.** Flag any cell that prints a whole DataFrame. The rule is `.head()`.
4. **Leakage.** Apply the `data-and-ml-rules` skill to any feature, split or evaluation code in the notebook.
5. **Deliverables.** Charts need a title, axis labels and units. Each analysis stage ends with a conclusion cell.
6. **Size.** Flag any output that stores raw data or a large table in the notebook.

Report a short list, ranked by impact, with cell numbers. Then say what you checked and what you couldn't check, for example a result that needs a rerun.

If the owner edits the notebook outside VS Code, remind them to run **File: Revert File** before they save.
