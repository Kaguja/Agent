import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output = True,
            text = True,
            timeout = 30,
        )
        return_string = []
        if result.returncode != 0:
            return_string.append(f'Process exited with code {result.returncode}')
        if not result.stdout and not result.stderr:
            return_string.append(f'No output produced')
        else:
            return_string.append(f'STDOUT: {result.stdout} STDERR: {result.stderr}')
        
        return  "\n".join(return_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python file, given the working directory relative file path(file_path) and optional argument (args)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Provides the path to the python file we want to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Provides optional arguments we might want to hand over to the python file we want to execute",
            ),
        },
        required = ["file_path"]
    ),
)