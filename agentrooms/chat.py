from .agent import Agent

class Chat():
    def __init__(self, chat_name: str, agents: list[Agent]):
        self.chat_name = chat_name
        self.agents = agents
        self.history = []

        for agent in self.agents:
            agent.add_chat(self)

    def add_message(self, sender, content):
        self.history.append({
            'sender': sender,
            'content': content,
        })
    
    def get_agent_names(self):
        return [agent.agent_name for agent in self.agents]

    def get_log(self):
        output = ''

        for message in self.history:
            output += f'- {message['sender']}: {message['content']}\n'
        
        return output