# Agent Framework with Ollama

A quick start guide for building AI agents using Microsoft's Agent Framework with Ollama as the local LLM provider.

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Ollama](https://ollama.ai/) installed and running locally

## Quick Start

### 1. Set up Ollama

First, make sure Ollama is running and pull a model:

```sh
# Pull a model (this example uses gpt-oss:20b, but you can use any model)
ollama pull gpt-oss:20b

# Verify it's available
ollama list
```

### 2. Create your project

```sh
# Clone this repository or create a new project
git clone https://github.com/pauldotyu/agent-framework-quickstart-with-ollama.git
cd agent-framework-quickstart-with-ollama

# Install dependencies
uv sync
```

### 3. Run your first agent

```sh
uv run main.py
```

That's it! Your agent will tell you a pirate joke using your local Ollama model.

## What's in the code

The `main.py` file contains a simple agent example:

```python
import asyncio
from agent_framework import ChatAgent
from agent_framework.observability import setup_observability
from agent_framework.openai import OpenAIChatClient

setup_observability()

async def main():
    async with (
        ChatAgent(
            chat_client=OpenAIChatClient(),
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a pirate.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

The agent automatically connects to your local Ollama instance thanks to the environment configuration in the `.env` file.

## Environment Configuration

The project includes a `.env` file that configures everything for you:

```properties
# Ollama Configuration
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_CHAT_MODEL_ID=gpt-oss:20b
OPENAI_API_KEY=none

# OpenTelemetry (for monitoring - optional)
ENABLE_OTEL=true
ENABLE_SENSITIVE_DATA=true
OTLP_ENDPOINT=http://localhost:4317
```

- **OPENAI_BASE_URL**: Points to Ollama's OpenAI-compatible API
- **OPENAI_CHAT_MODEL_ID**: The model you want to use (change this to match your pulled model)
- **OPENAI_API_KEY**: Set to "none" for Ollama (required by the OpenAI client)

## Optional: Observability with OpenTelemetry and chat history storage with Redis

Want to see what's happening under the hood? You can enable observability to monitor your agent's performance.

The docker compose setup also includes Redis for chat history storage if needed.

### Start the monitoring

```sh
# Start the OpenTelemetry collector and Redis
docker compose up -d

# Run your agent (observability is already enabled in .env)
uv run main.py

# View real-time telemetry data
docker logs otel-collector -f
```

### Stop monitoring

```sh
docker compose down
```

The telemetry shows you:

- **Traces**: How your agent processes requests
- **Metrics**: Token usage and performance data
- **Logs**: Debug information and agent activities

## Using Different Models

To use a different Ollama model:

1. Pull the model: `ollama pull model-name`
2. Update `OPENAI_CHAT_MODEL_ID` in your `.env` file
3. Run your agent: `uv run main.py`

## Next Steps

- Check out the [Agent Framework documentation](https://learn.microsoft.com/agent-framework/tutorials/quick-start?pivots=programming-language-python)
- Explore the [OpenAI chat client source](https://github.com/microsoft/agent-framework/blob/main/python/packages/core/agent_framework/openai/_chat_client.py)
- Modify `main.py` to create your own custom agents
