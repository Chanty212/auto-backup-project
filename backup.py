# backup.py
import subprocess

def has_changes():
    """Return True if there are unstaged or uncommitted changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True
    )
    return bool(result.stdout.strip())


def run_backup():
    try:
        # 1) Skip if there is nothing new to backup
        if not has_changes():
            print("No changes to commit; skipping backup.")
            return "no_changes"

        # 2) Stage, commit, and push
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto backup update"], check=True)
        subprocess.run(["git", "push"], check=True)

        print("Backup successful (committed and pushed).")
        return "success"

    except Exception as e:
        print(f"Backup failed: {e}")
        return "error"
