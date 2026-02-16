import os
import subprocess

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