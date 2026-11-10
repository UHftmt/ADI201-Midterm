#!/usr/bin/env python3
"""Known-answer runner. Run: python3 tests/known-answer/run.py  (Windows: python)

The loop, the step bookkeeping, and the checking are done for you. You write the three
hooks marked TODO so that they drive YOUR web app (for example with the Flask test client,
or HTTP calls to the running server). Translate your own state and outcome words to the
common words from the project contract inside the hooks.

Step vocabulary (contract section 3): create, move, list, restart.
"""
import atexit
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent

# Run from the repository root no matter where you start the command, so that
# "import your_app" and relative paths such as "fixtures/..." work.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)


# ---- the three hooks: how run.py drives the salon app ----------------------
#
# MAPPING (my words -> contract common words). It is one-to-one: the app
# already uses the contract's words, so the hooks translate nothing.
#
#   states     booked, confirmed, arrived, completed, no_show, cancelled
#              -> the same six words
#   outcomes   accepted, bad_date_format, after_close, conflict,
#              duplicate_request, not_permitted, illegal_move
#              -> the same seven words
#   roles      client, staff -> the same two words
#
# Extra internal outcome words that are NOT contract words (no case should
# expect them; they only appear when the input itself is broken):
#   missing_field    a create with an empty request_id, client, service_id or stylist
#   unknown_service  a create whose service_id is not in services.csv
#   not_found        a move on an item number that does not exist
#
# Every step goes through the JSON API in app.py (/api/bookings...), which
# calls the same Store methods as the /book and /staff pages.

_TEMP_DIRS = []  # one temporary folder per case, all removed when run.py ends


def _cleanup():
    for d in _TEMP_DIRS:
        d.cleanup()


atexit.register(_cleanup)


def _start(db_path):
    """Build a brand-new Flask app on this database file and return a handle."""
    from app import create_app
    return {"client": create_app(db_path).test_client(), "db_path": db_path}


def new_app():
    """A fresh app with an EMPTY data store: a new database file in a new temporary folder."""
    folder = tempfile.TemporaryDirectory(prefix="salon-known-answer-")
    _TEMP_DIRS.append(folder)
    return _start(os.path.join(folder.name, "salon.db"))


def restart_app(app):
    """Throw the old app away and build a new one on the SAME database file."""
    db_path = app["db_path"]
    app.clear()  # the old Flask app and its test client are dropped here
    return _start(db_path)


def do_step(app, step, items):
    """Perform one create / move / list step through the JSON API and return
    the result in the contract's common words (see MAPPING above)."""
    client = app["client"]
    do = step["do"]

    if do == "create":
        reply = client.post("/api/bookings",
                            json={"role": step["as"], "data": step["data"]}).get_json()
        if reply["outcome"] != "accepted":
            return {"outcome": reply["outcome"]}  # a rejected create makes no item
        items.append(reply["id"])
        return {"outcome": reply["outcome"], "state": reply["state"]}

    if do == "move":
        number = step["item"]  # 1-based: item 1 is items[0]
        if not isinstance(number, int) or number < 1 or number > len(items):
            # The case points at an item that was never created
            # (for example its create was rejected).
            return {"outcome": "not_found"}
        reply = client.post(f"/api/bookings/{items[number - 1]}/move",
                            json={"role": step["as"], "to": step["to"]}).get_json()
        if "state" not in reply:
            return {"outcome": reply["outcome"]}
        return {"outcome": reply["outcome"], "state": reply["state"]}

    if do == "list":
        reply = client.get("/api/bookings").get_json()
        minutes = reply["minutes_by_stylist"]
        return {
            "outcome": reply["outcome"],
            "count": reply["count"],
            "ana_minutes": minutes.get("Ana", 0),
            "ben_minutes": minutes.get("Ben", 0),
        }

    raise ValueError(f"unknown step: {do!r}")


def run_case(case):
    """Run every step of one case on a fresh app and return the result of the LAST step."""
    app = new_app()
    items = []
    result = {}
    for step in case["input"]:
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
