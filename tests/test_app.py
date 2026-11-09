import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from app import create_app


class AppointmentAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "test.sqlite3")
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "DATABASE": self.database,
            }
        )
        self.client = self.app.test_client()
        self.slot_date = (date.today() + timedelta(days=10)).isoformat()

    def tearDown(self):
        self.temp_dir.cleanup()

    def book(self, *, name="Sam Example", provider="Avery", time="10:00"):
        return self.client.post(
            "/customer",
            data={
                "customer_name": name,
                "service": "Consultation",
                "provider": provider,
                "appointment_date": self.slot_date,
                "appointment_time": time,
            },
            follow_redirects=True,
        )

    def test_customer_booking_appears_in_staff_queue_and_logs_reminder(self):
        response = self.book()
        self.assertIn(b"Request #1 submitted", response.data)

        queue = self.client.get("/frontdesk")
        self.assertIn(b"Sam Example", queue.data)
        self.assertIn(b"Reminder log", queue.data)
        self.assertIn(b"(not sent)", queue.data)

        with self.app.app_context():
            from app import get_db

            reminder = get_db().execute(
                "SELECT * FROM reminder_log WHERE appointment_id = 1"
            ).fetchone()
            self.assertIsNotNone(reminder)

    def test_engineered_failure_rejects_overlapping_booking(self):
        self.book()
        response = self.book(name="Taylor Example", time="10:00")
        self.assertIn(b"already has an appointment", response.data)
        with self.app.app_context():
            from app import get_db

            count = get_db().execute(
                "SELECT COUNT(*) FROM appointments"
            ).fetchone()[0]
            self.assertEqual(count, 1)

    def test_adjacent_appointments_do_not_conflict(self):
        first = self.book(time="10:00")
        second = self.book(name="Taylor Example", time="10:30")
        self.assertIn(b"Request #1 submitted", first.data)
        self.assertIn(b"Request #2 submitted", second.data)

    def test_front_desk_confirms_then_records_arrival_and_completion(self):
        self.book()
        confirmed = self.client.post(
            "/frontdesk/1/status", data={"status": "confirmed"}
        )
        self.assertEqual(confirmed.status_code, 302)
        arrived = self.client.post("/frontdesk/1/status", data={"status": "arrived"})
        self.assertEqual(arrived.status_code, 302)
        completed = self.client.post(
            "/frontdesk/1/status", data={"status": "completed"}
        )
        self.assertEqual(completed.status_code, 302)
        with self.app.app_context():
            from app import get_db

            status = get_db().execute(
                "SELECT status FROM appointments WHERE id = 1"
            ).fetchone()["status"]
            self.assertEqual(status, "completed")

    def test_invalid_status_transition_is_rejected(self):
        self.book()
        response = self.client.post(
            "/frontdesk/1/status", data={"status": "completed"}
        )
        self.assertEqual(response.status_code, 400)

    def test_front_desk_move_checks_new_slot_conflicts(self):
        self.book()
        self.book(name="Taylor Example", time="11:00")
        response = self.client.post(
            "/frontdesk/1/move",
            data={
                "provider": "Avery",
                "appointment_date": self.slot_date,
                "appointment_time": "11:00",
            },
            follow_redirects=True,
        )
        self.assertIn(b"already has an appointment", response.data)
        with self.app.app_context():
            from app import get_db

            start_at = get_db().execute(
                "SELECT start_at FROM appointments WHERE id = 1"
            ).fetchone()["start_at"]
            self.assertTrue(start_at.endswith("10:00"))

    def test_no_show_appointments_still_block_rebooking(self):
        self.book()
        self.client.post("/frontdesk/1/status", data={"status": "no-show"})
        response = self.client.post(
            "/customer",
            data={
                "customer_name": "Taylor Example",
                "service": "Consultation",
                "provider": "Avery",
                "appointment_date": self.slot_date,
                "appointment_time": "10:00",
            },
            follow_redirects=True,
        )
        self.assertIn(b"already has an appointment", response.data)

    def test_provider_has_a_distinct_schedule_view(self):
        self.book()
        response = self.client.get("/provider?provider=Avery")
        self.assertIn(b"Avery's appointments", response.data)
        self.assertIn(b"Sam Example", response.data)
        jordan = self.client.get("/provider?provider=Jordan")
        self.assertIn(b"No appointments are scheduled for Jordan", jordan.data)

    def test_booking_persists_after_app_is_recreated(self):
        self.book()
        second_app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-key",
                "DATABASE": self.database,
            }
        )
        response = second_app.test_client().get("/frontdesk")
        self.assertIn(b"Sam Example", response.data)


if __name__ == "__main__":
    unittest.main()
