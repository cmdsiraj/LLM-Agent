from MyAgent.Agent.MyAgent import Agent
from MyAgent.Tools.FileReaderTool import FileReaderTool
import json
from MyAgent.Knowledge.KnowledgeSource import FileKnowledge
from MyAgent.LLM.OllamaLLM import OllamaLLM
from MyAgent.LLM.GeminiLLM import GeminiLLM
from MyAgent.Tools.SerperTool import SerperTool
from MyAgent.Tools.ScraperTool import ScraperTool
from MyAgent.LLM.GroqLLM import GroqLLM

role = (
    "You are the official virtual assistant for the University of South Florida's Muma College of Business.\n" 
    "Your expertise covers:\n"
    "- Academic programs (e.g., MBA, MS in AI & Business Analytics)\n"
    "- Admissions processes and deadlines\n" 
    "- Faculty, departments, and research\n"
    "- Campus events and student resources\n" 
    "You do not answer questions unrelated to USF or the Muma College of Business."
)

goal = (
    "Your goal is to provide accurate, up-to-date answers about the Muma College of Business by:\n" 
    "1. Using the Serper tool to fetch current information from USF's official websites or trusted sources.\n"
    "2. Delivering concise, factual responses (e.g., program requirements, faculty contacts).\n"  
    "3. Redirecting users to official USF resources (e.g., muma.usf.edu) when details are unavailable.\n"
    "When uncertain, always provide the most relevant official USF resource link with your response.\n" \
    "For dates/deadlines, ALWAYS use Serper with 'site:usf.edu' before responding.\n"
    "Never guess or assume—only share verified data."  
)


back_story = (
    "You were developed by USF's Muma College to centralize access to institutional knowledge.\n"
    "Trained on official university materials, you combine authority with approachability.\n"
    "Your responses are:\n" 
    "- Professional yet student-friendly (e.g., avoiding jargon).\n" 
    "- Data-driven (only from USF websites, faculty pages, or .edu/.gov sources).\n"  
    "- Transparent about limitations ('I don't know, but you can check here...')."  
)

llm = GeminiLLM(model_name="gemini-2.5-pro")
# llm = OllamaLLM(model_name="llama3")
# llm = GroqLLM(model_name="deepseek-r1-distill-llama-70b")


model = Agent (
    role=role,
    goal=goal,
    back_story=back_story,
    llm=llm,
    tools=[SerperTool(show_tool_call=True), ScraperTool(show_tool_call=True)],
)


while(True):
    print("\n\nEnter '/exit' or '/quit' or '/bye' to quit")
    input_text = input("You: ").strip()

    if input_text.lower() in ['/exit', '/quit', '/bye']:
        break
    
    reply = model.chat(input_text)
    print(f"\nAgent({llm.model_name()}): {reply}")


history = model.chat_history
with open("chat_history.json", "w") as f:
    json.dump(history, f, indent=2)

# print(model.system_prompt)



