import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path_working_dir, directory))
        valid_target_dir  = os.path.commonpath([abs_path_working_dir, target_dir]) == abs_path_working_dir
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        
        current_directory = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            current_item = f"- {str(item)}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}"
            current_directory.append(current_item)
        return '\n'.join(current_directory)
    except Exception as e:
        return f"Error: {e}"