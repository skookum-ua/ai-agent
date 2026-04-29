import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        absolute_path = os.path.abspath(working_directory)

        full_path = os.path.normpath(os.path.join(absolute_path, file_path))

        if  os.path.commonpath([absolute_path, full_path]) != absolute_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted directory'
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to file in a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of file to write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content which will be writen to file"
            )
        },
        required=["file_path"] 
    ),
)