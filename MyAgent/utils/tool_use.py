from MyAgent.Tools.Tool import Tool

import re
import inspect
import json

def get_tool_arguments(tool: Tool):
    signature = inspect.signature(tool._run_implementation)
    args = list(signature.parameters.keys())
    args_list = []
    for arg in args:
        if signature.parameters[arg].annotation is inspect._empty:
            annotat = "any"
        else:
            annotat = signature.parameters[arg].annotation
        
        args_list.append(f"{arg}:{annotat}")
    
    return ";".join(args_list)

def format_tools(tools: list[Tool]):
    if not tools:
        return "None"
    
    return "\n".join(
        [
            f"- **tool_name**: {tool.name}\n"
            f"  **tool_description**: {tool.description}\n"
            f"  **tool_arguments**: {get_tool_arguments(tool)}"
            for tool in tools
        ]
    )


def extract_tools_needed(agent_text):
    block_pattern = r"(<?/?TOOLUSE>?.*?<?/?TOOLUSE>?)"
    result1 = re.findall(block_pattern, agent_text, re.DOTALL | re.IGNORECASE)

    in_block_pattern = r"TOOL:\s*(.*?)\s*ARGS:\s*({.*?})"
    tools_needed = []

    for block in result1:
        found_tool = re.findall(in_block_pattern, block, re.DOTALL)
        if not found_tool:
            continue

        name = found_tool[0][0]
        args_str = found_tool[0][1].strip()

        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            try:
                # Attempt to repair just the content of the code string
                repaired = (
                    args_str.replace('\\', '\\\\')
                            .replace('"', '\\"')
                            .replace('\n', '\\n')
                            .replace('\t', '\\t')
                )

                # Extract value for 'code_string' using regex or fallback
                match = re.search(r'"code_string"\s*:\s*"(.*)', repaired, re.DOTALL)
                if match:
                    code_val = match.group(1)
                    if code_val.endswith('"}'):
                        code_val = code_val[:-2]  # remove trailing "}
                    args = {"code_string": code_val}
                else:
                    args = {"code_string": repaired}
            except Exception as e:
                print(f"[Tool Extraction Error] Failed to fix ARGS: {e}")
                continue

        tools_needed.append({"tool_name": name, "args": args})

    return tools_needed if tools_needed else []
