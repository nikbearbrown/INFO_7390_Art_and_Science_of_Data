import asyncio
import os
import sys

try:
    from . import server
except ImportError:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    

    src_dir = os.path.dirname(current_dir)
    

    if src_dir not in sys.path:
        sys.path.append(src_dir)
    

    import mcp_server_ds.server as server

def main():
    """Main entry point for the package."""
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    main()