from .utils import get_first_content_between_tags
from anthropic import Anthropic
from dotenv import load_dotenv
import random
import os
load_dotenv('../.env')

class Agent():
    def __init__(self, agent_name: str, model: str):
        self.agent_name = agent_name # set name of agent
        self.model = model
        self.chats = []
        self.system_prompt = None
        self.anthropic = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    
    def add_chat(self, chat):
        self.chats.append(chat)

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt # usually the rules

    def step(self):
        assert self.system_prompt is not None

        step_prompt = '''Task: Select a group chat to send a message in, and write what you would say next in that group chat. Select who you would like to speak next. Ensure the conversation flows naturally and avoids repetition. If no message has been sent yet, send a message related to your assigned role.
        
Please respond in the following format.

<group_chat> [name of group chat] </group_chat>
<message> [your message content] </message>
<next_speaker> [name of next speaker] </next_speaker>'''

        # we now construct a prompt containing all of the chat histories
        chat_history_prompt = '''Below are the list of conversations you have access to.'''

        for chat in random.sample(self.chats, len(self.chats)): # SHUFFLE THE ORDER OF THE CHATS TO PREVENT ORDER BIAS
            chat_history_prompt += f"\n\nChat name: {chat.chat_name}"
            chat_history_prompt += f"\nParticipating agents: {', '.join(chat.get_agent_names())}"
            chat_history_prompt += f"\nConversation so far:\n{chat.get_log()}"

        prompt = f'''{chat_history_prompt}\n\n==========\n\n{step_prompt}'''

        messages = [{'role': 'user', 'content': prompt}]

        response = self.anthropic.messages.create(
            model=self.model,
            max_tokens=400,
            temperature=0.7,
            system=self.system_prompt,
            messages=messages,
        )

        response_text = response.content[0].text

        chat_name = get_first_content_between_tags(response_text, 'group_chat').strip(' \n')
        content = get_first_content_between_tags(response_text, 'message').strip(' \n')
        next_speaker = get_first_content_between_tags(response_text, 'next_speaker').strip(' \n')

        response_dict = {
            'chat_name': chat_name,
            'content': content,
            'next_speaker': next_speaker,
            'raw_response': response_text
        }

        print('='*25)
        print('NAME:', self.agent_name)
        # print('SYSTEM PROMPT:', self.system_prompt)
        # print('PROMPT:', prompt)
        # print('\n\n')
        print(response_text)
        print({
            'chat_name': chat_name,
            'content': content,
            'next_speaker': next_speaker
        })
        print('='*25)

        for chat in self.chats:
            if chat.chat_name == chat_name:
                chat.add_message(self.agent_name, content)
        
        return next_speaker, response_dict

        




