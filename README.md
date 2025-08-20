# Mesh Orchestrator

This project demonstrates how to use the professional AI Mesh SDK to interact with AI agents, perform chat completions, and test various SDK capabilities.

## 🔧 Setup

```bash
# Install Poetry if you don't have it
pip install poetry

# Clone this repository
git clone <repository-url>
cd mesh-langchain-orchestrator-example

# Install dependencies
poetry install
```

## 🧠 Environment Variables

Set up your environment variables by editing the `.env` file with your actual Mesh API key:

```bash
# Edit .env with your actual MESH_API_KEY
MESH_API_KEY=your-actual-mesh-api-key-here
```

You can get your API token from the [AI Mesh platform](https://meshcore.ai).

## 🚀 Run the Demo

```bash
poetry run python main.py
```

## 📂 What It Does

The demo showcases the professional Mesh SDK capabilities:

- **Agent Discovery**: Loads all available agents from the Mesh platform
- **Agent Testing**: Demonstrates calling agents with sample inputs
- **Chat Completions**: Shows how to use LLM models through the Mesh API
- **Streaming Support**: Tests streaming responses for real-time interaction
- **Error Handling**: Comprehensive error handling with proper logging
- **Type Safety**: Uses Pydantic models for type-safe API interactions

## 🤖 Available Features

- **Type-safe API** with Pydantic models
- **Comprehensive error handling** with custom exceptions
- **Async support** (for production use)
- **Built-in retry logic** for robust API calls
- **Professional logging** with structured output
- **LangChain integration** (optional)

## 📊 Sample Output

The demo will show:
1. Available agents on the platform
2. Test agent call results
3. Chat completion responses
4. Streaming text generation
5. Usage statistics and token counts

## 🛠️ Dependencies

- `ai-mesh-sdk`: Official AI Mesh SDK from PyPI
- `openai`: For OpenAI API compatibility
- `langchain`: For agent orchestration capabilities
- `python-dotenv`: For environment variable management
- `requests`: For HTTP client functionality
- `jsonschema`: For JSON validation

## 💡 Example Usage

The demo automatically runs through various SDK features. For custom usage:

```python
from mesh_sdk import MeshClient

with MeshClient(api_key="your-token") as client:
    agents = client.list_agents()
    response = client.call_agent(
        agent_id=agents[0].id,
        inputs={"query": "Your query here"}
    )
```

