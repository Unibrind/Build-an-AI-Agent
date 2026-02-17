import functions.get_files_info
import functions.get_file_content
import functions.write_file
import functions.run_python_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[functions.get_files_info.schema_get_files_info,
                           functions.get_file_content.schema_get_file_content,
                           functions.write_file.schema_write_file,
                           functions.run_python_file.schema_run_python_file],
)