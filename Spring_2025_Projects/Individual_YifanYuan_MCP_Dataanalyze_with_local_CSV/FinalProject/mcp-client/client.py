import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import os
import uuid

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        # Pass API key explicitly
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.connected = False
        self.available_tools = []

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        self.available_tools = [tool.name for tool in response.tools]
        self.connected = True
        
        return self.available_tools

    async def process_query(self, query: str, server_script_path: str) -> str:
        """Process a query using Claude and available tools"""
        try:
            # Connect to the server at the beginning
            await self.connect_to_server(server_script_path)
            
            messages = [
                {
                    "role": "user",
                    "content": query
                }
            ]
            
            response = await self.session.list_tools()
            available_tools = [{ 
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in response.tools]

            # Debug output
            print(f"Available tools: {[tool['name'] for tool in available_tools]}")

            final_text = []
            final_text.append(f"Available tools: {', '.join(self.available_tools)}")
            
            # Continue conversation until no more tool calls or max iterations
            max_iterations = 5
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                print(f"Iteration {iteration}")
                print(f"messages: {messages}")
                # Call Claude with tools
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    messages=messages,
                    tools=available_tools  # Always include tools
                )
                
                has_tool_use = False
                
                # Process response
                for content in response.content:
                    if content.type == 'text':
                        final_text.append(content.text)
                        # Add Claude's text response to message history
                        messages.append({
                            "role": "assistant",
                            "content": content.text
                        })
                        
                    elif content.type == 'tool_use':
                        has_tool_use = True
                        tool_name = content.name
                        tool_args = content.input
                        
                        print(f"Tool use detected: {tool_name} with args {tool_args}")
                        
                        try:
                            # Execute tool call
                            result = await self.session.call_tool(tool_name, tool_args)
                            result_content = result.content if hasattr(result, 'content') else str(result)
                            
                            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                            final_text.append(f"Tool result: {result_content}")
                            print(f"Tool result: {result_content}")
                            # Add tool call to message history (Claude's action)
                            tool_id = str(uuid.uuid4())  # Generate a unique ID for each tool use
                            messages.append({
                                "role": "assistant",
                                "content": [
                                    {
                                        "type": "tool_use", 
                                        "id": tool_id,
                                        "name": tool_name, 
                                        "input": tool_args
                                        
                                    }
                                ]
                            })
                            
                            # Add tool result to message history
                            messages.append({
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",  # Fixed indentation
                                        "tool_use_id": tool_id,  # Must match the ID from the tool_use
                                        "content": result_content
                                    }
                                ]
                            })
                        except Exception as e:
                            error_msg = f"Error calling tool {tool_name}: {str(e)}"
                            final_text.append(error_msg)
                            messages.append({
                                "role": "user",
                                "content": error_msg
                            })
                
                if not has_tool_use:
                    break
                    
            result_text = "\n".join(final_text)
            return result_text
        
        finally:
            # Disconnect from the server at the end
            await self.cleanup()
            self.connected = False

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
        self.connected = False

    async def simple_query(self, query: str) -> str:
        """Simple query without tools for testing"""
        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": query}],
                timeout=30
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"