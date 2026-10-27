from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parents[1]
REQS_DIR = FRONTEND_DIR / "Reqs"


def req(name: str) -> str:
    """Absolute path to a file in frontend/Reqs."""
    return str(REQS_DIR / name)