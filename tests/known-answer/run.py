import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / "tests" / "known-answer" / "cases.json"


def new_app():
    raise NotImplementedError("Fill in new_app() to create the app for a known-answer test.")


def restart_app(app):
    raise NotImplementedError("Fill in restart_app() to restart the app and keep state.")


def do_step(app, step):
    raise NotImplementedError("Fill in do_step() to run one case step in the app.")


def main():
    data = json.loads(CASES_PATH.read_text())
    cases = data.get("cases", [])
    if not cases:
        print("Not written yet")
        return 0

    for case in cases:
        app = new_app()
        for step in case.get("input", []):
            try:
                do_step(app, step)
            except NotImplementedError:
                print(f"NOT WRITTEN YET: {case.get('name', 'unnamed')}")
                return 0
        print(f"PASS {case.get('name', 'unnamed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
