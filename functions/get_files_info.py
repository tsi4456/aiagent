import os
from google.genai import types


def get_files_info(working_directory, directory=None):
    if not (
        target := os.path.abspath(os.path.join(working_directory, directory))
    ).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not directory:
        target = os.path.abspath(working_directory)
    if not os.path.isdir(target):
        return f'Error: "{directory}" is not a directory'

    files = []
    for file in os.listdir(target):
        f = os.path.join(target, file)
        file_string = (
            f"- {file}: file_size={os.path.getsize(f)} bytes, is_dir={os.path.isdir(f)}"
        )
        files.append(file_string)
    return "\n".join(files)


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
