"""Tests for the Textual diff application."""

import asyncio
from pathlib import Path

from dunk.dunk import DunkApp


def test_app_renders_a_unified_diff(tmp_path: Path) -> None:
    """Show the parsed file path and its changed lines in the diff widget."""
    target = tmp_path / "example.py"
    target.write_text('print("after")\n')
    diff = """\
diff --git a/example.py b/example.py
index 0000000..1111111 100644
--- a/example.py
+++ b/example.py
@@ -1 +1 @@
-print("before")
+print("after")
"""

    async def run_app() -> str:
        """Mount the app and return the rendered diff text."""
        app = DunkApp(diff=diff, project_root=tmp_path)
        async with app.run_test(size=(120, 40)) as pilot:
            await pilot.pause()
            return app.query_one("#diff").render().plain

    rendered = asyncio.run(run_app())

    assert "example.py" in rendered
    assert 'print("after")' in rendered
