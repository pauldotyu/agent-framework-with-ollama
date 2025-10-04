# Agent Framework with Ollama

Start by creating a new project and adding the appropriate dependencies.

```sh
mkdir agent-framework-with-ollama
cd agent-framework-with-ollama
uv init
uv add agent-framework --prerelease=allow
```

Open the pyproject.toml file and make sure this is included at the bottom of the file

```toml
[tool.uv]
prerelease = "allow"
```

Remove the uv.lock file if you have one

```sh
rm -f uv.lock
```

Sync the dependencies

```sh
uv sync
```

Run the project

```sh
uv run main.py
```

## Running a basic agent sample

Reference: https://learn.microsoft.com/agent-framework/tutorials/quick-start?pivots=programming-language-python

Add this to main.py

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

async def main():
    async with (
        ChatAgent(
            chat_client=OpenAIChatClient(base_url="http://localhost:11434/v1", model_id="gpt-oss:20b", api_key="none"),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

Reference: https://github.com/microsoft/agent-framework/blob/main/python/packages/core/agent_framework/openai/_chat_client.py

Run the project

```sh
uv run main.py
```
