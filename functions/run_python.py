import os
import subprocess
import time


def run_python_file(working_directory, file_path):
    if not (
        target := os.path.abspath(os.path.join(working_directory, file_path))
    ).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    print(target)
    if not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        time.sleep(30)

        resp = subprocess.run(
            ["python3", target],
            capture_output=True,
        )

        if resp.stdout or resp.stderr:
            print(f"STDOUT: {resp.stdout}")
            print(f"STDERR: {resp.stderr}")
        else:
            print("No output produced.")
        if resp.returncode:
            print(f"Process exited with code {resp.returncode}")
    except Exception as e:
        print(f"Error: executing Python file: {e}")
