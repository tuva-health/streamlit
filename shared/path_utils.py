import sys
from pathlib import Path

def add_repo_to_path(levels_up=3):
    """
    Adds the project root to sys.path so shared modules can be imported.
    levels_up: number of directories to go up from the current file.
    """
    caller_path = Path(__file__).resolve()
    repo_root = caller_path.parents[levels_up]
    if str(repo_root) not in sys.path:
        sys.path.append(str(repo_root))
