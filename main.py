import asyncio

from agent_framework import ChatAgent
from agent_framework.observability import setup_observability
from agent_framework.openai import OpenAIChatClient

# setup_observability(enable_sensitive_data=True)


async def main():
    async with (
        ChatAgent(
            chat_client=OpenAIChatClient(),
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
