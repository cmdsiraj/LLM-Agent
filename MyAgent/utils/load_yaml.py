from MyAgent.Tools.Tool import Tool
from MyAgent.utils.tool_use import format_tools

import yaml
from pathlib import Path


def load_aget_config() -> dict:
    path = Path(__file__).parent.parent / "config" / "agents.yaml"

    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config.get('agents', {})


def get_system_prompt(role: str, goal: str, back_story: str, tools: list[Tool]):
    available_tools = format_tools(tools=tools)
   
    system_prompt_yaml_path = Path(__file__).parent.parent / "config" / "system.yaml"

    prompt_cfg = yaml.safe_load(system_prompt_yaml_path.read_text())

    filled_prompt = (
        prompt_cfg["role"]
        .replace("{{role}}", role)
        .replace("{{goal}}", goal)
        .replace("{{back_story}}", back_story)
        + "\n"
        + prompt_cfg["goal"]
        + "\n"
        + prompt_cfg["available_tools_block"]
        .replace("{{available_tools}}", available_tools)
    )

    system_message = {"role": "system", "content": filled_prompt}

    return system_message