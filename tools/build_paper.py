"""Build the complete mathematical book; see tools/typesetting/README.md."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "typesetting/build.py"), run_name="__main__")
