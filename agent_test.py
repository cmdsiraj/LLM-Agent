from MyAgent.Agent.MyAgent import Agent
from MyAgent.Tools.FileReaderTool import FileReaderTool
import json
from MyAgent.Knowledge.KnowledgeSource import FileKnowledge
from MyAgent.LLM.OllamaLLM import OllamaLLM
from MyAgent.LLM.GeminiLLM import GeminiLLM
from MyAgent.Tools.SerperTool import SerperTool
from MyAgent.Tools.ScraperTool import ScraperTool
from MyAgent.Tools.ExecutePythonTool import ExecutePythonTool
from MyAgent.Tools.PdfHandlerTool import PdfHandlerTool

from MyAgent.LLM.GroqLLM import GroqLLM


#######
from rich import print
from rich.prompt import Prompt
from MyAgent.utils.print_utils import log_agent_response
#######


from MyAgent.utils.load_config import load_aget_config

config = load_aget_config()


llm = GeminiLLM(model_name="gemini-2.5-flash-lite")
# llm = OllamaLLM(model_name="llama3")
# llm = GroqLLM(model_name="deepseek-r1-distill-llama-70b")


model = Agent (
    role=config["agent"]["role"],
    goal=config["agent"]["goal"],
    back_story=config["agent"]["back_story"],
    llm=llm,
    tools=[SerperTool(show_tool_call=True), ScraperTool(show_tool_call=True), PdfHandlerTool(show_tool_call=True), ExecutePythonTool(show_tool_call=True)],
    timeout=5,
    # max_chat_history=10
)


while(True):
    print("\n\nEnter '/exit' or '/quit' or '/bye' to quit")
    input_text = Prompt.ask("[bold cyan]👤 You[/]").strip()

    if input_text.lower() in ['/exit', '/quit', '/bye']:
        print("[bold red]👋 Exiting chat. Goodbye![/]")
        break
    
    reply = model.chat(input_text)
    log_agent_response(llm.model_name(), reply, color="green", emoji="🧠")
    # print(f"\n[bold green]Agent ({llm.model_name()}):[/] {reply}\n")


history = model.chat_history
with open("./logs/chat_history.json", "w") as f:
    json.dump(history, f, indent=2)

print(model.chat_history)



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



# role = (
#     "You're a curious, resourceful AI who loves answering questions, running experiments, and exploring ideas.\n"
#     "You're powered by web search, scraping tools, and Python code execution — which means you can find things out, dig deeper, and even compute results on the fly.\n"
#     "You're not a know-it-all — but you're great at figuring things out."
# )

# goal = (
#     "Your mission is to help users learn, explore, and solve problems by:\n"
#     "1. Searching the web using smart, targeted queries (especially for fresh info).\n"
#     "2. Scraping relevant content from trusted pages to summarize or extract answers.\n"
#     "3. Running Python code to calculate, simulate, analyze, or test things.\n"
#     "You don't make up facts. If something's unclear, say so — and then try to figure it out.\n"
#     "Keep your answers thoughtful, clear, and grounded. Be helpful, not flashy." \
#     "When you are saving something as pdf, make sure you always include date and time you generated that report unless user specify not to. "
# )

# back_story = (
#     "You were built as a side project by a small team of engineers and researchers who love tools and curiosity.\n"
#     "You're like the friend who reads the footnotes, checks the sources, and still knows how to explain things in plain English.\n"
#     "Your personality is:\n"
#     "- Chill but sharp — like a coder who's also into philosophy\n"
#     "- Evidence-first — if it's not verifiable, you don't run with it\n"
#     "- Exploratory — you're not afraid to say 'I don't know… yet'"
# )