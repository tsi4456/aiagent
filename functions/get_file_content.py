import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    if not (
        target := os.path.abspath(os.path.join(working_directory, file_path))
    ).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target, encoding="utf-8") as f:
            file_contents = f.read(MAX_CHARS)
        if os.path.getsize(target) > MAX_CHARS:
            file_contents += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_contents
    except Exception as e:
        return f"Error listing files: {e}"
