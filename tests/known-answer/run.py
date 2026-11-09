import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app

CASES_PATH = ROOT / "tests" / "known-answer" / "cases.json"


def new_app():
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "known-answer.sqlite3"
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "known-answer-key",
        "DATABASE": str(db_path),
    })
    app._known_answer_temp_dir = temp_dir
    return app


def restart_app(app):
    db_path = app.config["DATABASE"]
    restarted = create_app({
        "TESTING": True,
        "SECRET_KEY": "known-answer-key",
        "DATABASE": db_path,
    })
    restarted._known_answer_temp_dir = getattr(app, "_known_answer_temp_dir", None)
    return restarted


def do_step(app, step):
    client = app.test_client()
    as_role = step.get("as")
    action = step.get("action", "")

    if as_role == "customer":
        match = re.search(r"submit(?: second)? booking for (.+?) on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2}) for (.+)", action)
        if not match:
            raise ValueError(f"Unrecognized customer action: {action!r}")
        provider, appointment_date, appointment_time, service = match.groups()
        customer_name = "Second Customer" if "second" in action.lower() else "Sam Example"
        client.post(
            "/customer",
            data={
                "customer_name": customer_name,
                "service": service,
                "provider": provider,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
            },
            follow_redirects=True,
        )
        return app

    if as_role == "frontdesk":
        if "view queue after restart" in action:
            client.get("/frontdesk")
            return app

        match = re.search(r"(?:confirm|mark) appointment #(\d+)(?: |$)(.*)", action)
        if not match:
            raise ValueError(f"Unrecognized front desk action: {action!r}")
        appointment_id, suffix = match.groups()
        status_map = {
            "confirm": "confirmed",
            "confirm ": "confirmed",
            "arrived": "arrived",
            "completed": "completed",
            "no-show": "no-show",
            "no-show ": "no-show",
        }
        status = None
        for status_name, value in status_map.items():
            if suffix.strip() == status_name:
                status = value
                break
        if status is None:
            if "confirm" in action:
                status = "confirmed"
            elif "arrived" in action:
                status = "arrived"
            elif "completed" in action:
                status = "completed"
            elif "no-show" in action:
                status = "no-show"
        if status is None:
            raise ValueError(f"Unable to determine front-desk status for: {action!r}")
        client.post(
            f"/frontdesk/{appointment_id}/status",
            data={"status": status},
            follow_redirects=True,
        )
        return app

    if as_role == "system":
        if "restart" in action.lower():
            return restart_app(app)
        raise ValueError(f"Unrecognized system action: {action!r}")

    raise ValueError(f"Unrecognized role: {as_role!r}")


def main():
    data = json.loads(CASES_PATH.read_text())
    cases = data.get("cases", [])
    if not cases:
        print("Not written yet")
        return 0

    for case in cases:
        app = new_app()
        for step in case.get("input", []):
            app = do_step(app, step)
        print(f"PASS {case.get('name', 'unnamed')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
