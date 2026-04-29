import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        absolute_path = os.path.abspath(working_directory)

        full_path = os.path.normpath(os.path.join(absolute_path, file_path))

        if  os.path.commonpath([absolute_path, full_path]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted directory'
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", full_path]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command,cwd=absolute_path, capture_output=True, text=True, timeout=30)
        
        return_string = ""
        if completed_process.returncode != 0:
            return_string += f"Process exited with code {completed_process.returncode}\n"
        if  not completed_process.stderr and not completed_process.stdout:
            return_string += "No output produced"
        else:
            if completed_process.stdout:
                return_string += f"STDOUT: {completed_process.stdout}\n"
            if completed_process.stderr:
                return_string += f"STDERR: {completed_process.stderr}"
        
        return return_string 

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="EXECUTE a python script and get its output. Use this when you need to run calculations, process data, or perform logic defined in a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of python script file to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Additional arguments if needed, default is None"
            )
        },
        required=["file_path"] 
    ),
)
