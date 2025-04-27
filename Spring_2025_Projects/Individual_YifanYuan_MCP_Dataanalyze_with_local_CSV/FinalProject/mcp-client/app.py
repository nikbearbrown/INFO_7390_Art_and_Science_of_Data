import streamlit as st
import asyncio
import os
import sys
from client import MCPClient
import nest_asyncio
from dotenv import load_dotenv



load_dotenv() 
nest_asyncio.apply()
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


st.set_page_config(page_title="MCP Client", layout="wide")
nest_asyncio.apply()
# Define the path to the server script
SERVER_SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    "mcp-server", "mcp-server-data-exploration", "src", "mcp_server_ds", "__init__.py"
)

# Initialize session state variables if they don't exist
if "client" not in st.session_state:
    st.session_state.client = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "connected" not in st.session_state:
    st.session_state.connected = True
if "available_tools" not in st.session_state:
    st.session_state.available_tools = []
if "connection_attempted" not in st.session_state:
    st.session_state.connection_attempted = False
# Add parameters for data exploration
if "csv_path" not in st.session_state:
    st.session_state.csv_path = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "parameters_set" not in st.session_state:
    st.session_state.parameters_set = False

# Helper function to run async functions - revise this to be more robust
async def init_client():
    # Create a new client instance with explicit API key handling
    client = MCPClient()
    # Add a simple test to verify client initialized correctly
    if not client.anthropic:
        raise RuntimeError("Failed to initialize Anthropic client - API key may be missing")
    return client

def run_async(func):
    loop = asyncio.new_event_loop()
    return loop.run_until_complete(func)

# Create client if not exists - make this more robust
if "client" not in st.session_state or st.session_state.client is None:
    try:
        st.session_state.client = run_async(init_client())
        st.sidebar.success("Client initialized successfully")
    except Exception as e:
        st.sidebar.error(f"Failed to initialize client: {str(e)}")
        st.sidebar.warning("Check that your .env file contains ANTHROPIC_API_KEY")

# Function to connect to the server
def connect_to_server():
    print(f"Attempting to connect to server at: {SERVER_SCRIPT_PATH}")
    print(f"File exists: {os.path.exists(SERVER_SCRIPT_PATH)}")
    
    with st.spinner("Connecting to MCP server..."):
        try:
            st.session_state.available_tools = run_async(
                st.session_state.client.connect_to_server(SERVER_SCRIPT_PATH)
            )
            st.session_state.connected = True
            return True, None
        except Exception as e:
            st.session_state.connected = False
            import traceback
            error_details = f"{str(e)}\n{traceback.format_exc()}"
            print(f"Connection error details: {error_details}")
            return False, error_details

# Parameters form
st.title("Data Exploration Parameters")

if not st.session_state.parameters_set:
    with st.form("data_exploration_params"):
        st.write("Before connecting to the server, please provide the following parameters:")
        
        # CSV path input
        csv_path = st.text_input(
            "CSV File Path (required)",
            value=st.session_state.csv_path,
            help="Enter the full path to your CSV file"
        )
        
        # Topic input
        topic = st.text_input(
            "Analysis Topic (optional)",
            value=st.session_state.topic,
            help="Enter a topic to focus the data exploration on"
        )
        
        # Form submission
        submit_button = st.form_submit_button("Set Parameters")
        
        if submit_button:
            if not csv_path:
                st.error("CSV path is required!")
            else:
                # Check if the CSV file exists
                if not os.path.exists(csv_path):
                    st.error(f"CSV file not found at: {csv_path}")
                else:
                    st.session_state.csv_path = csv_path
                    st.session_state.topic = topic
                    st.session_state.parameters_set = True
                    st.rerun()
else:
    # Display the current parameters
    st.success("Parameters set successfully!")
    st.write(f"**CSV Path:** {st.session_state.csv_path}")
    st.write(f"**Topic:** {st.session_state.topic}" if st.session_state.topic else "**Topic:** None (using default analysis)")
    
    if st.button("Change Parameters"):
        st.session_state.parameters_set = False
        st.rerun()

# Only show the rest of the UI if parameters are set
if st.session_state.parameters_set:
    # Sidebar for server status and control
    with st.sidebar:
        st.title("MCP Client")
        
        # Display server path (informational only)
        st.text_input(
            "Server Script Path",
            value=SERVER_SCRIPT_PATH,
            disabled=True
        )
        
        # Connection status and control
        connection_col1, connection_col2 = st.columns([3, 1])
        
        with connection_col1:
            if st.session_state.connected:
                st.success("✅ Connected to server")
            else:
                if st.session_state.connection_attempted:
                    st.error("❌ Not connected")
                else:
                    st.info("⏳ Not connected yet")
        
    
        
        # Available tools section
        if st.session_state.connected and st.session_state.available_tools:
            st.subheader("Available Tools")
            for tool in st.session_state.available_tools:
                st.write(f"- {tool}")
                
        # Add test button for direct Claude API testing
        st.markdown("---")
        st.subheader("API Connection Test")
        test_query = st.text_input("Test query", value="Tell me a brief joke", key="test_query")
        
        if st.button("Test Direct API Connection"):
            with st.spinner("Testing Claude API connection..."):
                try:
                    # Call the simple_query method that doesn't use tools
                    result = run_async(st.session_state.client.simple_query(test_query))
                    st.success("✅ API connection successful!")
                    with st.expander("View response"):
                        st.markdown(result)
                except Exception as e:
                    st.error(f"API test failed: {str(e)}")
                    st.info("Check your ANTHROPIC_API_KEY and internet connection.")


    # Main chat interface
    st.title("MCP Chat Interface")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if st.session_state.connected:
        user_input = st.chat_input("Type your message here...")
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Process the query with the CSV path and topic parameters
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        
                        # Modify to include the CSV path and topic parameters
                        enriched_query = f"Data exploration task:\nCSV: {st.session_state.csv_path}\nTopic: {st.session_state.topic}\n\nUser query: {user_input}"  
                        st.markdown(enriched_query)
                        response = run_async(st.session_state.client.process_query(enriched_query,SERVER_SCRIPT_PATH ))                       
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        

                        
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
                        # Ensure server process is terminated in case of error

    else:
        st.info("Waiting for server connection to start chatting...")
        if not st.session_state.connected and st.session_state.connection_attempted:
            st.error("Server connection failed. Please check the server status and try connecting again from the sidebar.")


# Improved app closure handling
def on_close():
    """Handle graceful shutdown for both standard Python environments and UV environments"""
    try:
        # Safely check if attributes exist in session state
        client = getattr(st.session_state, "client", None)
        connected = getattr(st.session_state, "connected", False)
        
        if client and connected:
            try:
                run_async(client.cleanup())
                print("Successfully cleaned up MCP client connection")
            except Exception as e:
                print(f"Error during cleanup: {e}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Register the cleanup function
import atexit
atexit.register(on_close)

# Add information about the environment
st.sidebar.markdown("---")
st.sidebar.info("""
**Environment Note**: This app is compatible with UV environments.
To run with UV:
```
uv venv .venv
uv pip install -r requirements.txt
.venv/bin/streamlit run app.py
```
""")
