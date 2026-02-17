import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run python code provided from file_path in the working directory with 30-second timeout",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path and name of the python file to Run",
            ),
            ####### yemat yemas c'est quoi cette syntaXX !? ###########
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of command arguments to pass to the function"
            )
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir,file_path))
        valide_path = os.path.commonpath([target_file,abs_working_dir]) == abs_working_dir
        file = os.path.isfile(target_file)
        python_file = file_path.endswith(".py")
        
        if not valide_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not python_file:
            return f'Error: "{file_path}" is not a Python file'
        
        #5----------------------------------------------------------------------
        command = ["python3", target_file]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )
        
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if result.stdout == "" and result.stderr == "":
            output_parts.append("No output produced")
        
        else:
            if result.stdout != "":
                output_parts.append(f"STDOUT: {result.stdout.strip()}")
            if result.stderr != "":
                output_parts.append(f"STDERR: {result.stderr.strip()}")
        
        return "\n".join(output_parts)
        #5----------------------------------------------------------------------
    except Exception as e:
        return f"Error: executing Python file: {e}"