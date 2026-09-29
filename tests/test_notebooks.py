"""Each numbered topic is available as a script and a valid notebook."""

from pathlib import Path

import nbformat

from tools.generate_notebooks import cells_from_script

ROOT = Path(__file__).resolve().parents[1]


def test_every_topic_has_matching_notebook() -> None:
    scripts = sorted((ROOT / "workshop").glob("[0-9][0-9]-*/*.py"))
    assert len(scripts) == 23
    for script in scripts:
        notebook_path = script.with_suffix(".ipynb")
        notebook = nbformat.read(notebook_path, as_version=4)
        nbformat.validate(notebook)
        expected_code = [cell for cell in cells_from_script(script.read_text(encoding="utf-8")) if cell["cell_type"] == "code"]
        actual_code = [cell for cell in notebook.cells if cell.cell_type == "code"]
        assert [cell.source for cell in actual_code] == ["".join(cell["source"]) for cell in expected_code]
        markdown = "\n".join(cell.source for cell in notebook.cells if cell.cell_type == "markdown")
        for section in (
            "## Problem", "## Concept", "## Where this fits in the whole workshop",
            "## Architecture of this lesson", "## Step 1", "## Failure mode to know about",
            "## Production implication", "## Your turn",
        ):
            assert section in markdown, (notebook_path, section)
        assert "```text\n" in markdown, notebook_path
