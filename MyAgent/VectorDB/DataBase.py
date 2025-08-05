from abc import ABC, abstractmethod
from MyAgent.Knowledge.Knowledge import Knowledge

class DataBase(ABC):
    @abstractmethod
    def get_context(self, query: str):
        pass

    @abstractmethod
    def add_to_db(self, knowledge: list[Knowledge]):
        pass
