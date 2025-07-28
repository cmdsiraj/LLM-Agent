from MyAgent.Agent.BaseAgent import BaseAgent
from typing import Dict

class AgentManager:

    def __init__(self, exc_mode: str = "sequential", agents: list[BaseAgent]=None, out_dir:str=None):
        self.agents: Dict[str, BaseAgent] = {}
        self.exc_mode = exc_mode 
        self.out_dir = out_dir

        if agents:
            self.register(agents)
    
    def register(self, agent):
        if isinstance(agent, list):
            for gen in agent:
                self.agents[gen.name] = gen
        else:
            self.agents[agent.name] = agent
    
    def route_task(self, from_agent: str, to_agent: str, message: str):

        if to_agent not in self.agents:
            print(f"[Manager]Agent '{to_agent}' not found.")
            return
        
        print(f"[Manager] Routing message from '{from_agent}' to {to_agent}")
        recipient = self.agents[to_agent]
        return recipient.receive_message(message=message, sender=from_agent)
    
    def list_agent(self):
        return list(self.agents.keys())
    
    def execute(self, message: str):
        response = ""
        if self.exc_mode.lower() == "sequential":
            response = self.__execute_sequential(message=message)
        
        if self.out_dir:
            with open(self.out_dir, "w") as f:
                f.write(response)
                f.close()
            return f"Response Saved at {self.out_dir}"
        else:
            return response
    
    def __execute_sequential(self, message: str):
        current_message = message
        sender = "user"
        for agent_name, agent in self.agents.items():

                response = agent.receive_message(message=current_message, sender=sender)

                current_message = response
                sender = agent_name

        return current_message