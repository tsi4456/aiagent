import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
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
        commands = ["python", target]
        if args:
            commands.extend(args)
        resp = subprocess.run(
            commands,
            capture_output=True,
            timeout=30,
            text=True,
            cwd=os.path.abspath(working_directory),
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


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a named Python script, constrained to the working directory, and prints the response.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python script to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to pass to the script, if any.",
            ),
        },
    ),
)
