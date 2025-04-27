import os
import sys
import asyncio
import logging
import subprocess
import signal
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServerManager:
    """Manager for MCP data exploration server operations"""
    
    def __init__(self, server_path: Optional[str] = None):
        """Initialize the server manager.
        
        Args:
            server_path: Path to the MCP server directory. If None, will try to determine automatically.
        """
        self.server_process = None
        
        # Try to determine server path if not provided
        if server_path is None:
            # Navigate up from current directory and find the mcp-server directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            self.server_path = os.path.join(parent_dir, 'mcp-server', 'mcp-server-data-exploration')
        else:
            self.server_path = server_path
            
        logger.info(f"Using server path: {self.server_path}")
        
        # Add server path to Python path if needed
        server_src_path = os.path.join(self.server_path, 'src')
        if server_src_path not in sys.path:
            sys.path.append(server_src_path)
    
    def start_server(self):
        """Start the MCP server as a subprocess."""
        try:
            logger.info("Starting MCP data exploration server...")
            
            # Use Python executable to run the server module
            cmd = [
                sys.executable, 
                "-m", 
                "mcp_server_ds"
            ]
            
            # Start the server as a subprocess
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.server_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            logger.info(f"Server started with PID {self.server_process.pid}")
            
            # Monitor server process output in separate threads
            def monitor_output(stream, prefix):
                for line in stream:
                    logger.info(f"{prefix}: {line.strip()}")
            
            import threading
            stdout_thread = threading.Thread(
                target=monitor_output, 
                args=(self.server_process.stdout, "SERVER_STDOUT"),
                daemon=True
            )
            stderr_thread = threading.Thread(
                target=monitor_output, 
                args=(self.server_process.stderr, "SERVER_STDERR"),
                daemon=True
            )
            
            stdout_thread.start()
            stderr_thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start server: {str(e)}")
            return False
    
    def stop_server(self):
        """Stop the running MCP server."""
        if self.server_process:
            try:
                logger.info("Stopping MCP server...")
                
                # Send termination signal
                if sys.platform == 'win32':
                    self.server_process.send_signal(signal.CTRL_C_EVENT)
                else:
                    self.server_process.terminate()
                
                # Wait for process to terminate with timeout
                try:
                    self.server_process.wait(timeout=5)
                    logger.info("Server stopped successfully")
                except subprocess.TimeoutExpired:
                    logger.warning("Server did not stop gracefully, forcing termination")
                    self.server_process.kill()
                
                self.server_process = None
                return True
                
            except Exception as e:
                logger.error(f"Error stopping server: {str(e)}")
                return False
        else:
            logger.warning("No server is currently running")
            return False
    
    def is_server_running(self):
        """Check if the server is currently running."""
        if self.server_process:
            return self.server_process.poll() is None
        return False


async def init_server():
    """Initialize and start the MCP data exploration server."""
    server_manager = MCPServerManager()
    success = server_manager.start_server()
    return server_manager if success else None


def main():
    """Main entry point for the script."""
    try:
        logger.info("Initializing MCP data exploration server")
        server_manager = asyncio.run(init_server())
        
        if server_manager:
            logger.info("Server started successfully")
            
            # Keep the script running until interrupted
            try:
                while server_manager.is_server_running():
                    asyncio.run(asyncio.sleep(1))
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
            finally:
                server_manager.stop_server()
        else:
            logger.error("Failed to start server")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    """
How to use this script:

1. Direct Execution:
   - Run this file directly to start the MCP data exploration server
   - Command: python serverfront.py
   - The server will run until you press Ctrl+C to stop it
   
2. Programmatic Usage:
   - Import functions from this file in your own scripts
   - Example:
     ```
     from serverfront import init_server
     
     async def my_function():
         # Start the server
         server_manager = await init_server()
         
         # Do other operations with the server running
         
         # When finished, stop the server
         server_manager.stop_server()
     ```

3. Server Management Functions:
   - MCPServerManager class provides methods to control the server:
     * start_server(): Start the MCP server
     * stop_server(): Stop the running server
     * is_server_running(): Check if server is active
    """
    main()
