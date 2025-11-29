import os
import subprocess

def run_backup():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto backup update"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except Exception as e:
        print(e)
        return False
