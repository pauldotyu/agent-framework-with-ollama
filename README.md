# Agent Framework with local LLMs

A quick start guide for building AI agents using Microsoft's Agent Framework with local LLMs (e.g., Ollama or vLLM).

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) for Python package management
- [Ollama](https://ollama.ai/) installed and running locally
- [vLLM](https://docs.vllm.ai/) (optional, if you want to use vLLM)
- [Docker](https://www.docker.com/) (optional, for observability and Redis)
- [GitHub CLI](https://cli.github.com/) (optional, for cloning the repo)

## Quick Start

This quick start guide will help you set up a simple agent that tells jokes using a local Ollama model. If you prefer to use vLLM, you can skip the Ollama setup and configure the environment variables accordingly.

### 1. Set up Ollama

Pull a model (this example uses gpt-oss:20b, but you can use any model)

```sh
ollama pull gpt-oss:20b
```

Verify the model is available

```sh
ollama list
```

### 2. Create your project

Clone this repository or create a new project

```sh
gh repo create demo --template pauldotyu/agent-framework-quickstart-with-local-llms --clone --private
cd demo
```

Install dependencies

```sh
uv sync
```

Create a `.env` file by copying the provided example

```sh
cp .env.example .env
```

### 3. Run your first agent

```sh
uv run main.py
```

That's it! Your agent will tell you a corny joke using your local model.

## What's in the code

The `main.py` file contains a simple agent example:

```python
import asyncio

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

async def main():
    async with (
        ChatAgent(
            chat_client=OpenAIChatClient(),
            name="Joker",
            instructions="You are good at telling jokes.",
        ) as agent,
    ):
        result = await agent.run("Tell me a dad joke about programming.")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
```

## Environment Configuration

The project includes a `.env.sample` file that helps you configures the connection to your local LLM.

```properties
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_CHAT_MODEL_ID=gpt-oss:20b
OPENAI_API_KEY=none
```

- **OPENAI_BASE_URL**: Points to OpenAI API compatible inference server
- **OPENAI_CHAT_MODEL_ID**: The model you want to use
- **OPENAI_API_KEY**: Set to "none" for local servers that don't require authentication

Optional observability settings:

- **ENABLE_OTEL**: Set to `true` to enable OpenTelemetry observability
- **OTLP_ENDPOINT**: The endpoint for the OpenTelemetry collector

See next section for observability setup.

## Optional: Observability with OpenTelemetry and Grafana's LGTM stack

Want to see what's happening under the hood? You can enable observability to monitor your agent's performance.

The docker compose setup also includes Redis for chat history storage if needed.

### Start the monitoring

Start the observability stack

```sh
docker compose up -d
```

This will start:

- Redis for chat history storage
- OpenTelemetry Collector for collecting telemetry data
- Loki for logs
- Grafana for visualization
- Tempo for traces
- Prometheus for metrics

Update your `.env` file to enable OpenTelemetry

```properties
ENABLE_OTEL=true
OTLP_ENDPOINT=http://localhost:4317
```

Run your agent with observability enabled

```sh
uv run main.py
```

View real-time telemetry data with Grafana at [http://localhost:3000](http://localhost:3000).

Click on **Explore** in the sidebar.

Select **Tempo** then click on the **Search** button to see traces.

You should see traces, metrics, and logs related to your agent's operations.

The telemetry shows you:

- **Traces**: How your agent processes requests
- **Metrics**: Token usage and performance data
- **Logs**: Debug information and agent activities

### Stop monitoring

To stop the observability stack and remove volumes, run:

```sh
docker compose down -v
```

## Check stored chat messages

If you're using Redis for chat history storage, you can view the stored messages using the Redis CLI or the VS Code extension for Redis.

## Next Steps

- Check out the [Agent Framework documentation](https://learn.microsoft.com/agent-framework/tutorials/quick-start?pivots=programming-language-python)
- Explore the [OpenAI chat client source](https://github.com/microsoft/agent-framework/blob/main/python/packages/core/agent_framework/openai/_chat_client.py)
