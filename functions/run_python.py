import os
import subprocess


def run_python_file(working_directory, file_path: str):
    abs_working_dir = os.path.abspath(working_directory)
    target = abs_working_dir
    if file_path:
        target = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        return f'Error: File "{file_path}" not found.'
    if not target.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python", target], timeout=30, capture_output=True, text=True, check=True
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if len(output) > 0:
            return "\n".join(output)
        else:
            return "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"
