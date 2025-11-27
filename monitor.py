import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from notify import notify

WATCHED_FOLDER = r"C:\Users\Veteran\OneDrive\Desktop\watched_folder"


# --------------------------------------------------
# GIT BACKUP FUNCTION (handles all cases properly)
# --------------------------------------------------
def run_git_backup():
    try:
        print("🌀 Change Detected → Running Backup...")

        # git add .
        add_res = subprocess.run(
            ["git", "add", "."],
            capture_output=True, text=True
        )
        if add_res.returncode != 0:
            print("[git add stderr]:", add_res.stderr)
            notify("Backup failed: git add error.")
            return

        # git commit
        commit_res = subprocess.run(
            ["git", "commit", "-m", "Auto backup update"],
            capture_output=True, text=True
        )

        combined_output = (commit_res.stdout or "") + (commit_res.stderr or "")
        lower = combined_output.lower()

        # If nothing new, treat as normal — NOT an error
        if "nothing to commit" in lower:
            print("ℹ Nothing to commit. Working tree clean.")
            notify("Backup skipped: nothing new to commit.")
            return

        # If commit failed (real error)
        if commit_res.returncode != 0:
            print("[git commit stderr]:", commit_res.stderr)
            notify("Backup failed: git commit error.")
            return

        # git push
        push_res = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True
        )
        if push_res.returncode != 0:
            print("[git push stderr]:", push_res.stderr)
            notify("Backup failed: git push error.")
            return

        print("✅ Git backup completed successfully.")
        notify("Backup completed successfully!")

    except Exception as e:
        print("🔥 Exception during git backup:", e)
        notify(f"Backup failed: {e}")


# --------------------------------------------------
# WATCHDOG EVENT HANDLER
# --------------------------------------------------
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            run_git_backup()

    def on_created(self, event):
        if not event.is_directory:
            run_git_backup()


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------
if __name__ == "__main__":
    print("📡 Monitoring started...")
    print(f"📂 Watching: {WATCHED_FOLDER}")

    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Monitoring stopped.")
        observer.stop()
    observer.join()
