from MyAgent.Tools.Tool import Tool
from MyAgent.Exceptions.CustomExceptions import ToolUseExtractionError

import inspect
import re
import json

def format_tools(tools: list[Tool]):
    
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

    return "\n".join(
        [
            f"- **tool_name**: {tool.name}\n"
            f"  **tool_description**: {tool.description}\n"
            f"  **tool_arguments**: {get_tool_arguments(tool)}"
            for tool in tools
        ]
    )


import re, json
import yaml

def extract_tools_needed(agent_text):
    # Match all <TOOLUSE>...</TOOLUSE> blocks
    block_pattern = r"<TOOLUSE>(.*?)</TOOLUSE>"
    tool_blocks = re.findall(block_pattern, agent_text, re.DOTALL | re.IGNORECASE)

    tools_needed = []

    for block in tool_blocks:
        try:
            # Clean block and parse YAML
            block = block.strip()
            parsed = yaml.safe_load(block)

            # Validate structure
            if not isinstance(parsed, dict) or 'tool' not in parsed or 'args' not in parsed:
                raise ToolUseExtractionError(f"Missing 'tool' or 'args' in block:\n{block}")

            tools_needed.append({
                "tool_name": parsed['tool'],
                "args": parsed['args']
            })

        except yaml.YAMLError as e:
            raise ToolUseExtractionError(f"YAML parsing error:\n{block}\nError: {e}")

    print(f"From extract_tools_needed func (tools_needed): {tools_needed}")
    return tools_needed if tools_needed else None


# def extract_tools_needed(agent_text):
#     # Match all <TOOLUSE>...</TOOLUSE> blocks
#     block_pattern = r"<TOOLUSE>(.*?)</TOOLUSE>"
#     result1 = re.findall(block_pattern, agent_text, re.DOTALL | re.IGNORECASE)

#     # Match TOOL name and ARGS JSON
#     in_block_pattern = r"TOOL:\s*(.*?)\s*ARGS:\s*({.*?})"
#     tools_needed = []

#     for block in result1:
#         found_tools = re.findall(in_block_pattern, block, re.DOTALL)

#         for tool_name_raw, raw_args in found_tools:
#             tool_name = tool_name_raw.replace("'", "").strip()
#             raw_args = re.sub(r"```(json)?", "", raw_args).strip("`\n ")

#             # Try parsing the args
#             try:
#                 args = json.loads(raw_args)
#             except json.JSONDecodeError:
#                 try:
#                     # Replace single quotes and retry
#                     raw_args_cleaned = raw_args.replace("'", '"')
#                     args = json.loads(raw_args_cleaned)
#                 except Exception as e:
#                     raise ToolUseExtractionError(f"Failed to parse JSON args for tool `{tool_name}`: {e}")
#             except Exception as e:
#                 raise ToolUseExtractionError(f"Unexpected error for tool `{tool_name}`: {e}")

#             tools_needed.append({"tool_name": tool_name, "args": args})

#     print(f"From extract_tools_needed func (tools_needed): {tools_needed}")
#     return tools_needed if tools_needed else None
