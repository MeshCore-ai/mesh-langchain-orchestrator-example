# Mesh Orchestrator

This project demonstrates how to use the AI Mesh SDK with LangChain to dynamically compose agents into intelligent workflows.

## 🔧 Setup

```bash
# Install poetry if you don't have it
pip install poetry

# Clone this repo or create the structure
cd mesh_langchain_orchestrator_example
poetry install
```

## 🧠 Environment Variables

Copy the example environment file and update with your tokens:

```bash
cp .env.example .env
# Edit .env with your actual MESH_TOKEN
```

## 🚀 Run the Orchestrator

```bash
poetry run python main.py
```

## 📂 What It Does

- Loads all registered agents from Mesh using MeshSDK
- Wraps them as LangChain tools
- Lets an LLM decide which agents to call and when
- Logs all tool calls to `logs/tool_calls.log`

## 💡 Example Prompt

> "Find an article about AI regulation in the EU and summarize it."

