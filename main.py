#!/usr/bin/env python3
"""Updated mesh orchestrator using the new professional Mesh SDK."""

import os
import sys
import logging
from dotenv import load_dotenv

from mesh_sdk import MeshClient, MeshSDKError
from mesh_sdk.exceptions import AuthenticationError, APIError

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    """Main orchestrator function using professional SDK."""
    logger = setup_logging()
    
    # Load environment variables
    load_dotenv()
    mesh_api_key = os.getenv("MESH_API_KEY")
    
    if not mesh_api_key:
        logger.error("Please set MESH_API_KEY environment variable")
        return 1
    
    try:
        # Initialize the professional SDK client
        logger.info("🚀 Initializing Mesh SDK client...")
        with MeshClient(api_key=mesh_api_key) as client:
            
            # Demo different SDK capabilities
            logger.info("📋 Fetching available agents...")
            
            # List agents
            agents = client.list_agents()
            tools = client.list_tools()  
            llms = client.list_llms()
            
            logger.info(f"Found {len(agents)} agents, {len(tools)} tools, {len(llms)} LLMs")
            
            # Show available agents
            if agents:
                print("\n🤖 Available Agents:")
                for agent in agents[:3]:  # Show first 3
                    agent_type = agent.type.value if agent.type else "Unknown"
                    print(f"- {agent.name} ({agent_type}): {agent.description}")
                
                if len(agents) > 3:
                    print(f"  ... and {len(agents) - 3} more")
            
            # Test agent call if available
            if agents:
                logger.info("\n🔧 Testing agent call...")
                try:
                    first_agent = agents[0]
                    response = client.call_agent(
                        agent_id=first_agent.id,
                        inputs={"query": "Hello from the new professional SDK!"},
                        validate_inputs=False  # Skip validation for demo
                    )
                    
                    print(f"\n✅ Agent '{first_agent.name}' Response:")
                    print(response.data)
                    
                except Exception as e:
                    logger.warning(f"Agent call failed: {e}")
            
            # Test chat completions if LLMs available
            if llms:
                logger.info("\n💬 Testing chat completions...")
                
                # User query
                query = "What is 2+2? Also explain why mathematics is important."
                
                messages = [
                    {"role": "system", "content": "You are a helpful assistant that provides clear, concise answers."},
                    {"role": "user", "content": query}
                ]
                
                print(f"\n🔍 Query: {query}")
                print("-" * 50)
                
                try:
                    response = client.chat_completions(
                        model="openai/gpt-4o",  # Try the specified model first
                        messages=messages,
                        temperature=0.3,
                        max_tokens=200
                    )
                    
                    print(f"\n💡 Response from {response.model}:")
                    print(response.choices[0].message.content)
                    
                    # Show usage stats if available
                    if response.usage:
                        print(f"\n📊 Usage Stats:")
                        print(f"- Prompt tokens: {response.usage.prompt_tokens}")
                        print(f"- Completion tokens: {response.usage.completion_tokens}")
                        print(f"- Total tokens: {response.usage.total_tokens}")
                    
                except Exception as e:
                    # Fallback to first available LLM
                    logger.warning(f"Failed with specified model, trying first available LLM: {e}")
                    
                    try:
                        response = client.chat_completions(
                            model=llms[0].id,  # Use first available LLM
                            messages=messages,
                            temperature=0.3,
                            max_tokens=200
                        )
                        
                        print(f"\n💡 Response from {llms[0].name}:")
                        print(response.choices[0].message.content)
                        
                    except Exception as fallback_error:
                        logger.error(f"Chat completion failed: {fallback_error}")
            
            # Test streaming if supported
            if llms:
                logger.info("\n📡 Testing streaming response...")
                
                try:
                    messages = [
                        {"role": "user", "content": "Tell me a very short story about AI"}
                    ]
                    
                    print("\n📖 Streaming Story:")
                    print("-" * 25)
                    
                    full_response = ""
                    for chunk in client.chat_completions(
                        model=llms[0].id,
                        messages=messages,
                        stream=True,
                        temperature=0.8,
                        max_tokens=100
                    ):
                        if chunk.choices and len(chunk.choices) > 0:
                            delta = chunk.choices[0].delta
                            if delta.content:
                                print(delta.content, end="", flush=True)
                                full_response += delta.content
                    
                    print(f"\n\n✅ Streaming completed ({len(full_response)} characters)")
                    
                except Exception as e:
                    logger.warning(f"Streaming failed: {e}")
            
            print("\n" + "="*60)
            print("🎉 Professional SDK Demo Completed Successfully!")
            print("✨ The new SDK provides:")
            print("   - Type-safe API with Pydantic models")
            print("   - Comprehensive error handling")
            print("   - Async support (not shown in this demo)")
            print("   - Built-in retry logic")
            print("   - Professional logging")
            print("   - LangChain integration (optional)")
            print("="*60)
            
            return 0
            
    except AuthenticationError as e:
        logger.error(f"🔐 Authentication failed: {e}")
        return 1
        
    except APIError as e:
        logger.error(f"🚨 API error: {e}")
        if hasattr(e, 'status_code'):
            logger.error(f"   Status code: {e.status_code}")
        return 1
        
    except MeshSDKError as e:
        logger.error(f"⚠️  SDK error: {e}")
        return 1
        
    except Exception as e:
        logger.error(f"💥 Unexpected error: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)