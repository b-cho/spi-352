import os
from anthropic import Anthropic
from negotiationarena.agents.agents import Agent
import time
from copy import copy, deepcopy
from negotiationarena.constants import AGENT_TWO, AGENT_ONE


class ClaudeAgent(Agent):
    def __init__(
        self,
        agent_name: str,
        model: str = "claude-sonnet-4-5-20250929",
        use_system_prompt=True,
    ):
        super().__init__(agent_name)
        self.run_epoch_time_ms = str(round(time.time() * 1000))

        self.conversation = []
        self.model = model
        self.use_system_prompt = use_system_prompt
        self.system_prompt = ""
        self.prompt_entity_initializer = "system"
        self.anthropic = Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

    def init_agent(self, system_prompt, role):
        if AGENT_ONE in self.agent_name:
            # Store system prompt separately for Messages API
            self.system_prompt = system_prompt
            # Add the role as the first user message
            self.update_conversation_tracking("user", role)

        elif AGENT_TWO in self.agent_name:
            # Combine system prompt and role for agent two
            self.system_prompt = system_prompt + role
        else:
            raise ValueError("No Player 1 or Player 2 in role")

    def __deepcopy__(self, memo):
        """
        Deepcopy is needed because we cannot pickle the anthropic object.
        :param memo:
        :return:
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if (type(v)) == Anthropic:
                v = "AnthropicObject"
            setattr(result, k, deepcopy(v, memo))
        return result

    def chat(self):
        """
        Use the Messages API to chat with Claude.
        The conversation should only contain user and assistant messages.
        System prompt is passed separately.
        """
        # Filter out any 'system' role messages from conversation
        messages = [msg for msg in self.conversation if msg["role"] != "system"]

        # Create the message using Messages API
        response = self.anthropic.messages.create(
            model=self.model,
            max_tokens=400,
            temperature=0.7,
            system=self.system_prompt,
            messages=messages,
        )
        time.sleep(0.2) 

        # Extract text content from the response
        return response.content[0].text

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})
