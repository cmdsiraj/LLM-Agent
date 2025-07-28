from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, input_texts: str):
        """
        Context Retrival from VectorDB (if needed)
        Prompt building
        LLM Call
        Tool Execution
        Store LLM and tool outputs in chat history
        """
        pass

    @abstractmethod
    def receive_message(self, message: str, sender: str):
        pass

    @abstractmethod
    def send_message(self, message: str, recipient_name: str, manager):
        pass