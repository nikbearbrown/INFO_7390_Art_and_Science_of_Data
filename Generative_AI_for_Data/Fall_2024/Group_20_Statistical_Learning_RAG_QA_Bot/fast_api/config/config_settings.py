import os

# snowflake_connect.py
import snowflake.connector
from dotenv import load_dotenv 
# Load environment variables from .env file (if applicable)
load_dotenv()
def create_snowflake_connection():
    """Creates and returns a Snowflake connection."""
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )
    return conn