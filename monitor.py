import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backup import run_backup
from notify import notify
from config import MONITOR_FOLDER

DEBOUNCE_SECONDS = 2  # to avoid multiple triggers

class ChangeHandler(FileSystemEventHandler):
    last_run = 0

    def _maybe_run_backup(self, reason: str):
        now = time.time()
        if now - self.last_run < DEBOUNCE_SECONDS:
            return

        self.last_run = now
        print(f"{reason} → running backup...")
        result = run_backup()

        if result == "success":
            notify("Backup Completed Successfully!")
        elif result == "error":
            notify("Backup Failed. Check the system logs.")
        elif result == "no_changes":
            print("No changes detected by git; skipping WebEx notification.")

    def on_created(self, event):
        if event.is_directory:
            self._maybe_run_backup(f"Folder created: {event.src_path}")
        else:
            self._maybe_run_backup(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if event.is_directory:
            self._maybe_run_backup(f"Folder deleted: {event.src_path}")
        else:
       	    self._maybe_run_backup(f"File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            self._maybe_run_backup(f"File modified: {event.src_path}")


if __name__ == "__main__":
    observer = Observer()
    handler = ChangeHandler()
    observer.schedule(handler, MONITOR_FOLDER, recursive=True)
    print(f"Monitoring started on: {MONITOR_FOLDER}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
