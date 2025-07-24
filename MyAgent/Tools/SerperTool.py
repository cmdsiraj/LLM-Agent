import requests
from MyAgent.Tools.Tool import Tool
from MyAgent.utils.print_utils import log_tool_action
import os
from dotenv import load_dotenv

class SerperTool(Tool):

    def __init__(self, api_key=None, show_tool_call: bool=False):
        self.__name = "Serper Search"
        self._description = (
            "Searches the web using Serper and returns the top results. "
            "Use this tool when the user's question requires recent, external, or otherwise unknown information from the internet. "
        )
        self.show_tool_call = show_tool_call

        try:
            load_dotenv()
            self.serper_url = os.getenv("SERPER_URL")
            if api_key is None:
                
                api_key = os.getenv("SERPER_API_KEY")

            self.__api_key = api_key
        except Exception as e:
            print()


    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self._description
    
    def _run_implementation(self, search_query: str):
        serper_url = self.serper_url
        headers = {
            "X-API-KEY": self.__api_key,
            "Content-Type": "application/json"
        }
        data = {
            "q": search_query
        }

        if self.show_tool_call:
            log_tool_action("Conducting web search for", search_query, "🔍", "yellow")

        response = requests.post(url=serper_url, headers=headers, json=data)

        return response.json()['organic']