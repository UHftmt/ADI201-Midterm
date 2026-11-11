#!/usr/bin/env python3
"""Known-answer runner. Run: python3 tests/known-answer/run.py  (Windows: python)

The loop, the step bookkeeping, and the checking are done for you. You write the three
hooks marked TODO so that they drive YOUR web app (for example with the Flask test client,
or HTTP calls to the running server). Translate your own state and outcome words to the
common words from the project contract inside the hooks.

Step vocabulary (contract section 3): create, move, list, restart.
"""
import json
import os
import re
import sys
import tempfile
import uuid
from pathlib import Path

HERE = Path(__file__).parent

# Run from the repository root no matter where you start the command, so that
# "import your_app" and relative paths such as "fixtures/..." work.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from database import init_db
from domain import create_appointment, move_appointment, list_appointments_summary


class AppHandle:
    """Encapsulates the running application state and database handle."""
    def __init__(self, db_path):
        self.db_path = db_path


def new_app():
    """Start app with a fresh, empty SQLite database and seeded services."""
    temp_dir = tempfile.gettempdir()
    db_file = os.path.join(temp_dir, f"midterm_test_{os.getpid()}_{uuid.uuid4().hex[:8]}.db")
    if os.path.exists(db_file):
        os.remove(db_file)
    init_db(db_file)
    return AppHandle(db_file)


def restart_app(app):
    """Simulate app restart pointing to the same existing database file."""
    # Data is persisted on disk in app.db_path
    return AppHandle(app.db_path)


SHIMING_ROLE_MAP = {
    "customer": "client",
    "frontdesk": "staff",
}

SHIMING_SERVICE_MAP = {
    "Consultation": "S4",       # 30 minutes
    "Cut and style": "S1",      # 45 minutes
    "Color consultation": "S2", # 90 minutes
}


def translate_step(step, step_index):
    """Translate non-contract step syntax (e.g., Shiming's action prose) into contract steps."""
    if "do" in step:
        return step

    as_role = step.get("as", "")
    actor = SHIMING_ROLE_MAP.get(as_role, as_role)
    action = step.get("action", "")

    if as_role == "customer":
        match = re.search(
            r"submit(?: second)? booking for (.+?) on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) for (.+)",
            action,
        )
        if not match:
            raise ValueError(f"Unrecognized customer action: {action!r}")
        provider, appointment_date, appointment_time, service = match.groups()
        client_name = "Second Customer" if "second" in action.lower() else "Sam Example"
        return {
            "do": "create",
            "as": actor,
            "data": {
                "request_id": f"SHIMING-{step_index}",
                "client": client_name,
                "service_id": SHIMING_SERVICE_MAP.get(service, service),
                "stylist": provider,
                "start": f"{appointment_date} {appointment_time}",
            },
        }

    if as_role == "frontdesk":
        if "view queue" in action.lower():
            return {"do": "list"}
        match = re.search(r"(?:confirm|mark) appointment #(\d+)(?: |$)(.*)", action)
        if not match:
            raise ValueError(f"Unrecognized frontdesk action: {action!r}")
        item_num = int(match.group(1))
        if "confirm appointment" in action:
            to_state = "confirmed"
        elif "arrived" in action:
            to_state = "arrived"
        elif "completed" in action:
            to_state = "completed"
        elif "no-show" in action:
            to_state = "no_show"
        else:
            raise ValueError(f"Unable to map target state for: {action!r}")
        return {"do": "move", "as": actor, "item": item_num, "to": to_state}

    if as_role == "system" and "restart" in action.lower():
        return {"do": "restart"}

    raise ValueError(f"Unrecognized step format: {step!r}")


def do_step(app, step, items):
    """Perform one create / move / list step and return result in common vocabulary."""
    action = step.get("do")
    actor = step.get("as")

    if action == "create":
        data = step.get("data", {})
        result = create_appointment(app.db_path, actor, data)
        if result["outcome"] == "accepted":
            items.append(result["item_id"])
            return {"outcome": "accepted", "state": result["state"]}
        return {"outcome": result["outcome"]}

    elif action == "move":
        item_idx = step.get("item", 1) - 1
        to_state = step.get("to")
        if 0 <= item_idx < len(items):
            appt_id = items[item_idx]
            return move_appointment(app.db_path, actor, appt_id, to_state)
        return {"outcome": "invalid_request"}

    elif action == "list":
        return list_appointments_summary(app.db_path)

    return {"outcome": "invalid_request"}


def run_case(case):
    """Run every step of one case on a fresh app and return the result of the LAST step."""
    app = new_app()
    items = []
    result = {}
    for idx, raw_step in enumerate(case["input"], start=1):
        step = translate_step(raw_step, idx)
        if step["do"] == "restart":
            app = restart_app(app)
            result = {"outcome": "accepted"}
        else:
            result = do_step(app, step, items)
    return result


def matches(got, expected):
    """expected may list only some keys; every key you list must match."""
    if isinstance(expected, dict) and isinstance(got, dict):
        return all(k in got and got[k] == v for k, v in expected.items())
    # Shiming's cases use string expectations mapped to common outcomes here.
    if isinstance(expected, str) and isinstance(got, dict):
        if expected == "accepted":
            return got.get("outcome") == "accepted"
        if expected == "not_permitted":
            return got.get("outcome") in {"not_permitted", "illegal_move", "conflict"}
        if expected == "state_persists":
            return got.get("outcome") == "accepted" and got.get("count", 0) >= 1
    return got == expected


def main():
    # Phase 1: one tests/known-answer/cases.json. Phase 2: one tests/known-answer/<member>/cases.json
    # per member, and every one of them is run (names get the member's folder as a prefix).
    files = sorted(HERE.glob("*/cases.json")) or [HERE / "cases.json"]
    cases = []
    try:
        for f in files:
            prefix = f"{f.parent.name}/" if f.parent != HERE else ""
            for c in json.loads(f.read_text())["cases"]:
                cases.append({**c, "name": prefix + c["name"]})
    except (OSError, ValueError, KeyError) as exc:
        sys.exit(f'cases.json must exist and look like {{"cases": [...]}} ({exc})')
    if not cases:
        sys.exit("cases.json has no cases yet: write them first (Step 1.3)")
    failed = 0
    for case in cases:
        try:
            got = run_case(case)
        except NotImplementedError as exc:
            sys.exit(f"{exc}: connect the hooks in run.py to your app")
        except Exception as exc:  # a crash is a FAIL, not a stop
            got = f"error: {exc}"
        if matches(got, case["expected"]):
            print(f"PASS {case['name']}")
        else:
            failed += 1
            print(f"FAIL {case['name']}: expected {case['expected']}, got {got}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
