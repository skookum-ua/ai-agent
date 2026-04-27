import os
def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)

        full_path = os.path.normpath(os.path.join(absolute_path, directory))

        if  os.path.commonpath([absolute_path, full_path]) != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        dir_scan_output = {}

        for i in os.listdir(full_path):

            i_path = os.path.normpath(os.path.join(full_path, i))
            if os.path.isdir(i_path):
                dir_scan_output[i] = os.path.getsize(i_path), True

            if os.path.isfile(i_path):
                dir_scan_output[i] = os.path.getsize(i_path), False

        
        out_string = ""
        for i in dir_scan_output:
            out_string = out_string + f"- {i}: file_size={dir_scan_output[i][0]} bytes, is_dir={dir_scan_output[i][1]}\n"
        return out_string
    except Exception as e:
        return f"Error: {e}"