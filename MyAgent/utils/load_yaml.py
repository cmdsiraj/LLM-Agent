import yaml

import os

default_path = os.path.join(os.path.dirname(__file__), "../config/system_prompt.yaml")


def load_system_prompt(role, goal, back_story, available_tools, path=default_path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    print("---"*10)
    print(available_tools)
    
    content = " ".join(line.format(
        role=role,
        goal=goal,
        back_story=back_story,
        available_tools=available_tools
    ) for line in data["content"])

    return {
        "role": data["role"],
        "content": content
    }


