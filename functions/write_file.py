import os
from google.genai import types


def write_file(working_directory, file_path, content):
    if not (
        target := os.path.abspath(os.path.join(working_directory, file_path))
    ).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    print(target)
    if not os.path.exists(os.path.dirname(target)):
        os.makedirs(os.path.dirname(target))

    try:
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error writing file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a given string to a provided filename, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to write or overwrite, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write.",
            ),
        },
    ),
)
