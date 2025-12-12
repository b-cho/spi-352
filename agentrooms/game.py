from .agent import Agent
from .chat import Chat

class Game():
    def __init__(self, agents: list[Agent], chats: list[Chat], log_dir='.logs'):
        self.agents = agents
        self.chats = chats
        self.log_dir = log_dir
        self.history = []
    
    def is_game_over(self, response):
        return False

    def run(self, max_iterations=20): 
        # begin with the first agent in the agents list
        next_index = 0

        for it in range(max_iterations):
            next_agent, response_dict = self.agents[next_index].step()

            response_dict['turn'] = it
            response_dict['sender'] = self.agents[next_index].agent_name

            self.history.append(response_dict)

            if self.is_game_over(response_dict['raw_response']):
                return self.history
            
            next_index = next((index for index, agent in enumerate(self.agents) if agent.agent_name == next_agent), None)
        
        print(self.history)
        return self.history
    