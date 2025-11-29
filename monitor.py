# monitor.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backup import run_backup
from notify import notify
from config import MONITOR_FOLDER

DEBOUNCE_SECONDS = 2  # wait time between runs

class ChangeHandler(FileSystemEventHandler):
    last_run = 0

    def on_modified(self, event):
        now = time.time()

        # Ignore changes in directories themselves
        if event.is_directory:
            return

        # Debounce: avoid firing multiple times per quick burst of events
        if now - self.last_run < DEBOUNCE_SECONDS:
            return

        self.last_run = now

        print(f"Change detected in: {event.src_path}")
        result = run_backup()

        if result == "success":
            notify("Backup Completed Successfully!")
        elif result == "error":
            # Optional: you can comment this out if you don't want failure messages
            notify("Backup Failed. Check the system logs.")
        elif result == "no_changes":
            # Silent case – don't spam WebEx
            print("No new changes; not sending WebEx notification.")


if __name__ == "__main__":
    observer = Observer()
    event_handler = ChangeHandler()
    observer.schedule(event_handler, MONITOR_FOLDER, recursive=True)

    print(f"Monitoring started on: {MONITOR_FOLDER}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
