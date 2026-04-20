import os
from config import max_read_chars


def get_file_content(working_directory, file_path):
    try:
        file_string = ""
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            file_string = f.read(max_read_chars)
            if f.read(1):
                file_string += f'[...File "{file_path}" truncated at {max_read_chars} characters]'
            return file_string
    except Exception as e:
        return f'Error: {e}'