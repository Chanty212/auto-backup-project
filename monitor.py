import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backup import run_backup
from notify import notify
from config import MONITOR_FOLDER

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("Change Detected → Running Backup...")
        
        if run_backup():
            notify("Backup Completed Successfully!")
        else:
            notify("Backup Failed. Check the system.")

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_FOLDER, recursive=True)
    
    print("Monitoring started...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
