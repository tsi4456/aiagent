import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    abs_working = os.path.abspath(working_directory)
    target = abs_working
    if directory:
        target = os.path.abspath(os.path.join(working_directory, directory))
    if not target.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    try:
        files = []
        for file in os.listdir(target):
            f = os.path.join(target, file)
            file_string = f"- {file}: file_size={os.path.getsize(f)} bytes, is_dir={os.path.isdir(f)}"
            files.append(file_string)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
