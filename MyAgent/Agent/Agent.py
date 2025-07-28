from MyAgent.Agent.BaseAgent import BaseAgent
from MyAgent.Knowledge.Knowledge import Knowledge
from MyAgent.VectorDB.VectorDB import VectorDB
from MyAgent.Tools.Tool import Tool
from MyAgent.utils.load_yaml import get_system_prompt
from MyAgent.LLM.LLMBase import LLM
from MyAgent.LLM.OllamaLLM import OllamaLLM
from MyAgent.Agent.AgentManager import AgentManager

from MyAgent.utils.tool_use import extract_tools_needed

import json

from MyAgent.utils.print_utils import log_agent_execution



class Agent(BaseAgent):
    
    def __init__(self, name:str, role: str, goal: str, back_story: str, llm:LLM , chat_history: list[dict] = None, tools:list[Tool]=None, knowledge: list[Knowledge] = None, top_k: int = 3, max_chat_history:int=20, log_exe=True):
        super().__init__(name=name)
        self.role = role
            
        if chat_history:
            self.chat_history=chat_history
        else:
            self.chat_history = list()

        if tools:
            self.tools={tool.name: tool for tool in tools}
        else:
            self.tools = list()

        if knowledge:
            self._db = VectorDB(knowledgeFiles=knowledge)
        else:
            self._db = None
        
        self.top_k = top_k

        self.__max_chat_history = max_chat_history

        self.logs = list()

        self.system_prompt=get_system_prompt(role=role, goal=goal, back_story=back_story, tools=tools)

        self.llm = llm if llm else OllamaLLM(model_name="llama3")

    
    

    def __execute_tool(self, tool_name: str, args: dict):
        tool = self.tools.get(tool_name)
        if tool:
            return tool.run(**args)
        else:
            return f"{tool_name} not found"
    

    def __execute_tools(self, tools_needed: list[Tool]):
        tools_results = []
        for tool in tools_needed:
            tool_result = self.__execute_tool(**tool)
            tools_results.append(f'TOOL RESULT OF {tool["tool_name"]} : {tool_result}')
        
        return '\n'.join(tools_results)

    

    def __chat(self, messages):
        prompt = [self.system_prompt] + messages
        # result = ollama.chat(model=self.model, messages=prompt)
        result = self.llm.chat(messages=prompt)
        return result
        
    def run(self, user_input):

        # Retriving required knowledge (if knowledge is setup)
        if self._db:
            context = self._db.get_context(user_input, self.top_k)
            user_input = (
                    "you can use the context to answer the question:\n"
                    f"{context}"
                    f"\nQuestion: {user_input}"
            )
        
        self.chat_history.append({"role": "user", "content":user_input})

        reply = self.__chat(self.chat_history)

        tools_needed = extract_tools_needed(reply)

        if(tools_needed):
             while True:
                #Now, passing the prompt to model
                reply = self.__chat(self.chat_history)

                tools_needed = extract_tools_needed(reply)
                # Checking if the model response has involved use of any tools
                if(tools_needed):
                    tools_content = self.__execute_tools(tools_needed)
                    self.chat_history.append({
                        "role": 
                            "tool assistant", 
                        "content": 
                            "Use the following content from tools to answer the users questions:\n"
                            f"{tools_content}"
                            f"user question: {user_input}"
                        })
                else:
                    break

            # We include the agents final response in our chat history
        self.chat_history.append({"role": "assistant", "content": reply})
        self.chat_history = self.chat_history[-self.__max_chat_history:]

        return reply
    
    def receive_message(self, message: str, sender: str):
        self.chat_history.append({
            "role": "user",
            "content": f"Message from {sender}: {message}"
        })

        log_agent_execution(self.name, self.role)

        response  = self.run(message)

        self.logs.append({
        "agent": self.name,
        "sender": sender,
        "input": message,
        "output": response,
        })

        return response
    
    def send_message(self, message: str, recipient_name: str, manager: AgentManager):

        if manager:
            return manager.route_task(from_agent=self.name, to_agent=recipient_name, message=message)
        else:
            return f"No manager provided to route the message from {self.name} to {recipient_name}"
    

    def save_logs(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.logs, f, indent=2)

