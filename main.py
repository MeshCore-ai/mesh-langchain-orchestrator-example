import os
import sys
from pathlib import Path
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging

# Add the local mesh_sdk to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "mesh_sdk"))
from sdk import MeshSDK

# === Load secrets ===
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
mesh_token = os.getenv("MESH_TOKEN")

# === Logging ===
logging.basicConfig(
    filename="logs/tool_calls.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Monkeypatch Tool to log calls ===
from langchain.agents import Tool

original_call = Tool.__call__

def logged_call(self, *args, **kwargs):
    logging.info(f"[Tool Start] {self.name}\nArgs: {args}\nKwargs: {kwargs}")
    result = original_call(self, *args, **kwargs)
    logging.info(f"[Tool End] {self.name}\nOutput: {result}")
    return result

Tool.__call__ = logged_call  # Override tool call behavior

# === Set up SDK and Tools ===
sdk = MeshSDK()  # No token needed for public endpoints

# Load available agents
agents = sdk.list_agents()
print(f"Loaded {len(agents)} agents from mesh API")

tools = sdk.to_langchain_tools()

# === Set up LLM and Agent ===
llm = ChatOpenAI(temperature=0.3, model="gpt-4o-mini")

# Get the prompt template for ReAct agent
prompt = hub.pull("hwchase17/react")

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# === User Prompt ===
query = "Can you search the internet for the hottest AI agents, scrape their github repos, and summarize their capabilities and list their github urls?"
# query = "Search for Python programming language information"

# === Run Agent ===
print("\n=== RUNNING AGENT ===\n")
response = agent_executor.invoke({"input": query})

print("\n=== FINAL RESULT ===\n")
print(response["output"])