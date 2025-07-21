import requests
from MyAgent.Tools.Tool import Tool

class SerperTool(Tool):

    def __init__(self, show_tool_call: bool=False):
        self.__name = "Serper Search"
        self._description = (
            "Searches the web using Serper and returns the top results. "
            "Use this tool when the user's question requires recent, external, or otherwise unknown information from the internet. "
        )
        self.show_tool_call = show_tool_call
    
    @property
    def name(self):
        return self.__name
    
    @property
    def description(self):
        return self._description
    
    def run(self, search_query: str):
        serper_url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": "b013f073d4b72a84754b47fe3879307fc8852445",
            "Content-Type": "application/json"
        }
        data = {
            "q": search_query
        }

        if self.show_tool_call:
            print(f"Conducting web search for {search_query}")

        response = requests.post(url=serper_url, headers=headers, json=data)

        return response.json()['organic']