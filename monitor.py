import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backup import run_backup
from notify import notify
from config import MONITOR_FOLDER

class ChangeHandler(FileSystemEventHandler):
    last_run = 0

    def on_any_event(self, event):
        now = time.time()

        # debounce: ignore events within 2 seconds of the last run
        if now - self.last_run < 2:
            return

        self.last_run = now
        print("Change detected → Running backup...")

        if run_backup():
            notify("Backup Completed Successfully!")
        else:
            notify("Backup Failed. Check the system.")
            

if __name__ == "__main__":
    observer = Observer()
    event_handler = ChangeHandler()
    observer.schedule(event_handler, MONITOR_FOLDER, recursive=True)
    print("Monitoring started...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
