from MyAgent.Agent.Agent import Agent
from MyAgent.Agent.AgentManager import AgentManager
from MyAgent.Tools.FileReaderTool import FileReaderTool
import json
from MyAgent.Knowledge.FileKnowledge import FileKnowledge
from MyAgent.LLM.OllamaLLM import OllamaLLM
from MyAgent.LLM.GeminiLLM import GeminiLLM
from MyAgent.Tools.SerperTool import SerperTool
from MyAgent.Tools.ScraperTool import ScraperTool
from MyAgent.Tools.ExecutePythonTool import ExecutePythonTool

from MyAgent.LLM.GroqLLM import GroqLLM

from MyAgent.utils.load_yaml import load_aget_config

#######
from rich import print
from rich.prompt import Prompt
from MyAgent.utils.print_utils import log_agent_response
#######

config = load_aget_config()

# llm_gemini = GeminiLLM(model_name="gemini-2.5-flash")
# llm = OllamaLLM(model_name="llama3")
# llm = GroqLLM(model_name="deepseek-r1-distill-llama-70b")


idea_agent = Agent(
    name=config["idea_agent"]["name"],
    role=config["idea_agent"]["role"],
    goal=config["idea_agent"]["goal"],
    back_story=config["idea_agent"]["backstory"],
    llm=GeminiLLM(model_name="gemini-2.5-flash")
)

market_agent = Agent(
    name=config["market_agent"]["name"],
    role=config["market_agent"]["role"],
    goal=config["market_agent"]["goal"],
    back_story=config["market_agent"]["backstory"],
    llm=GeminiLLM(model_name="gemini-2.5-flash"),
    tools=[SerperTool(show_tool_call=True)]
)

planner_agent = Agent(
    name=config["planner_agent"]["name"],
    role=config["planner_agent"]["role"],
    goal=config["planner_agent"]["goal"],
    back_story=config["planner_agent"]["backstory"],
    llm=GeminiLLM(model_name="gemini-2.5-pro"),
    tools=[ExecutePythonTool(show_tool_call=True)]
)

model = AgentManager(
    agents=[idea_agent, market_agent, planner_agent],
    out_dir="output.md"
)

message = "I'm thinking of starting a subscription box service for eco-friendly personal care products. It should help customers discover sustainable alternatives to everyday items like shampoo, toothpaste, and deodorant."

result = model.execute(message=message)

print(result, "\n")

# model = Agent (
#     role=role,
#     goal=goal,
#     back_story=back_story,
#     llm=llm,
#     tools=[SerperTool(show_tool_call=True), ScraperTool(show_tool_call=True), ExecutePythonTool(show_tool_call=True)],
# )


# while(True):
#     print("\n\nEnter '/exit' or '/quit' or '/bye' to quit")
#     input_text = Prompt.ask("[bold cyan]👤 You[/]").strip()

#     if input_text.lower() in ['/exit', '/quit', '/bye']:
#         print("[bold red]👋 Exiting chat. Goodbye![/]")
#         break
    
#     reply = model.chat(input_text)
#     log_agent_response(llm.model_name(), reply, color="green", emoji="🧠")
#     # print(f"\n[bold green]Agent ({llm.model_name()}):[/] {reply}\n")


# history = model.chat_history
# with open("./logs/chat_history.json", "w") as f:
#     json.dump(history, f, indent=2)

# print(model.system_prompt)




# muma bot
# role = (
#     "You are the official virtual assistant for the University of South Florida's Muma College of Business.\n" 
#     "Your expertise covers:\n"
#     "- Academic programs (e.g., MBA, MS in AI & Business Analytics)\n"
#     "- Admissions processes and deadlines\n" 
#     "- Faculty, departments, and research\n"
#     "- Campus events and student resources\n" 
#     "You do not answer questions unrelated to USF or the Muma College of Business."
# )

# goal = (
#     "Your goal is to provide accurate, up-to-date answers about the Muma College of Business by:\n" 
#     "1. Using the Serper tool to fetch current information from USF's official websites or trusted sources.\n"
#     "2. Delivering concise, factual responses (e.g., program requirements, faculty contacts).\n"  
#     "3. Redirecting users to official USF resources (e.g., muma.usf.edu) when details are unavailable.\n"
#     "When uncertain, always provide the most relevant official USF resource link with your response.\n" \
#     "For dates/deadlines, ALWAYS use Serper with 'site:usf.edu' before responding.\n"
#     "Never guess or assume—only share verified data."  
# )


# back_story = (
#     "You were developed by USF's Muma College to centralize access to institutional knowledge.\n"
#     "Trained on official university materials, you combine authority with approachability.\n"
#     "Your responses are:\n" 
#     "- Professional yet student-friendly (e.g., avoiding jargon).\n" 
#     "- Data-driven (only from USF websites, faculty pages, or .edu/.gov sources).\n"  
#     "- Transparent about limitations ('I don't know, but you can check here...')."  
# )