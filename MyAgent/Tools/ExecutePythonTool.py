from MyAgent.Tools.Tool import Tool
import os
import tempfile
import subprocess
from MyAgent.utils.print_utils import log_tool_action


class ExecutePythonTool(Tool):

    def __init__(self, show_tool_call=False):
        self.__name = "Python_code_execution_tool"
        self.__description = (
            "Executes Python code and returns the output. "
            "Use valid JSON in ARGS. "
            "Wrap the code in a JSON string using single quotes or escape double quotes. "
            )
        self.show_tool_call = show_tool_call
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self.__description
    
    def __run_code_in_docker(self, code_path):
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",              # no internet
            "--cpus", "0.5",                  # limit CPU
            "--memory", "512m",               # limit memory
            "-v", f"{code_path}:/code/script.py:ro",  # read-only mount
            "python:3.10",                    # official Python image
            "python", "/code/script.py"
        ]

        try:
            result = subprocess.run(docker_cmd, capture_output=True, text=True)
            return {
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "exit_code": result.returncode
            }
        except Exception as e:
            print(f"Got exception while executing python code: {e}")
            return e
    
    def _run_implementation(self, code_string: str):

        if self.show_tool_call:
            log_tool_action("Executing Python code", "...", "⚙️", "blue")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(code_string)
            file_path = temp_file.name

        return self.__run_code_in_docker(file_path)
    
