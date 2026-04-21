import os
from google.genai import types

def remove_file(working_directory,file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot interact with "{file_path}" as it is a directory'
        os.remove(file_path)
        return f'Successfully removed "{file_path}"'

    except Exception as e:
        return f'Error: {e}'

schema_remove_file = types.FunctionDeclaration(
    name="remove_file",
    description="removes a file with the given path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Provides the path to the file we want to delete",
            ),
        },
        required = ["file_path"]
    ),
)