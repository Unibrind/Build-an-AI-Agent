import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a single file and returns it as a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)

def get_file_content(working_directory, file_path):
    
    try:
        
        abs_path_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_path_working_dir, target_file]) == abs_path_working_dir

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        

        with open(target_file, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'
                return content
            return file_content_string
    
    except Exception as e:
        return f"Error: {e}"