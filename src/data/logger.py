import csv
import time
import os


class DataLogger:
    def __init__(self, session_id=None):
        if session_id is None:
            session_id = int(time.time())
        self.session_dir = f"data/sessions/{session_id}"
        os.makedirs(self.session_dir, exist_ok=True)

        self.log_file = os.path.join(self.session_dir, "events.csv")
        self.init_log()

    def init_log(self):
        with open(self.log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event_type", "x", "y", "details"])

    def log_event(self, event_type, x, y, details=""):
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time.time(), event_type, x, y, details])
