import re
import json
from MyAgent.Knowledge.KnowledgeSource import FileKnowledge
from MyAgent.VectorDB.VectorDB import VectorDB
from MyAgent.Tools.Tool import Tool
from MyAgent.utils.load_system_prompt import get_system_prompt
from MyAgent.LLM.LLMBase import LLM
from MyAgent.LLM.OllamaLLM import OllamaLLM



class Agent:
    
    def __init__(self, role: str, goal: str, back_story: str, llm:LLM , chat_history=[], tools:list[Tool]=[], knowledge: list = None, top_k: int = 3, max_chat_history:int=20):
        self.llm = llm if llm else OllamaLLM(model_name="llama3")
            
        self.chat_history=chat_history
        self.system_prompt=get_system_prompt(role=role, goal=goal, back_story=back_story, tools=tools)
        self.tools={tool.name: tool for tool in tools}
        self.__vectorDb = None

        if knowledge:
            self.__add_to_db__(knowledgeFiles=knowledge)
        
        self.__top_k = top_k

        self.__max_chat_history = max_chat_history


    
    def __add_to_db__(self, knowledgeFiles: list[FileKnowledge]):
        if self.__vectorDb == None:
            self.__vectorDb = VectorDB()

        for knowledge in knowledgeFiles:
             for content in knowledge.get_content():
                self.__vectorDb.add(content)


    
    def __get_context__(self, query):
        if self.__vectorDb == None:
            return self.__vectorDb
        
        return self.__vectorDb.search(query, top_k=self.__top_k)
    
    

    def __run_tools__(self, tool_name: str, args: dict):
        tool = self.tools.get(tool_name)
        if tool:
            return tool.run(**args)
        else:
            return f"{tool_name} not found"
    

    
    def __extract_tools_needed__(self, agent_text):

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
    

    def __get_tool_execution_results(self, tools_needed: list[Tool]):
        tools_results = []
        for tool in tools_needed:
            tool_result = self.__run_tools__(**tool)
            tools_results.append(f'TOOL RESULT OF {tool["tool_name"]} : {tool_result}')
        
        return '\n'.join(tools_results)

    

    def __chat__(self, messages):
        prompt = [self.system_prompt] + messages
        # result = ollama.chat(model=self.model, messages=prompt)
        result = self.llm.chat(messages=prompt)
        return result
        
    def chat(self, user_input):

        # Retriving required knowledge (if knowledge is setup)
        if self.__vectorDb:
            context = self.__get_context__(user_input)
            user_input = (
                    "you can use the context to answer the question:\n"
                    f"{context}"
                    f"\nQuestion: {user_input}"
            )
        
        self.chat_history.append({"role": "user", "content":user_input})

        reply = self.__chat__(self.chat_history)

        tools_needed = self.__extract_tools_needed__(reply)

        if(tools_needed):
             while True:
                #Now, passing the prompt to model
                reply = self.__chat__(self.chat_history)

                tools_needed = self.__extract_tools_needed__(reply)
                # Checking if the model response has involved use of any tools
                if(tools_needed):
                    tools_content = self.__get_tool_execution_results(tools_needed)
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