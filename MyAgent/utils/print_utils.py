from rich import print
from rich.panel import Panel

def log_tool_action(label, detail, emoji="🔧", color="yellow"):
    print(f"[bold {color}]{emoji} {label}[/] [dim]{detail}[/]")


def log_agent_response(model_name, response, color="green", emoji="🤖"):
    print(f"\n[bold {color}]{emoji} Agent ({model_name}):[/] {response}\n")


def log_agent_execution(name, role):
        print(
        Panel.fit(
            f"[bold cyan]🔄 Executing Agent[/bold cyan]\n[green]{name}[/green]\n[dim]{role}[/dim]",
            title=f"[bold magenta]Step[/bold magenta]",
            border_style="blue",
        )
    )
