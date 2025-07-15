import subprocess
import os

def run_sync_script():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "sync_to_git.sh")
    subprocess.run(["chmod", "+x", script_path], check=True)
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"Script exited with code {result.returncode}")

if __name__ == "__main__":
    run_sync_script()
