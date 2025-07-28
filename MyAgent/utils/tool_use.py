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
        return "No tools assigned."
    
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
        name = found_tool[0][0]
        args_str=found_tool[0][1].strip()

        try:
            args = json.loads(args_str)
        except json.JSONDecodeError as e:
            args = json.loads(args_str.replace("'", '"'))
        except Exception as e:
            print(f"Error occured while decoidng args: {e}")
            return
        tools_needed.append({"tool_name": name, "args": args})

    if len(tools_needed)>0:
        return tools_needed
    else:
        None