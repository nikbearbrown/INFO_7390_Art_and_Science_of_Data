import os
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Snowflake connection details
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

# Connect to Snowflake
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    return conn

# Function to create USERS table
def create_users_table():
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        # SQL query to create the USERS table with the additional columns
        create_users_sql = '''
        CREATE OR REPLACE TABLE USERS (
            user_id STRING PRIMARY KEY,
            username STRING UNIQUE NOT NULL,
            password STRING NOT NULL,
            name STRING NOT NULL,
            country STRING NOT NULL,
            favorite_categories STRING,  -- JSON array stored as a string
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_users_sql)
        conn.commit()
        print("USERS table created successfully.")

    except Exception as e:
        print(f"Error creating USERS table: {e}")

    finally:
        cursor.close()
        conn.close()

# Function to create CONVERSATIONS table
def create_conversations_table():
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        # SQL query to create the CONVERSATIONS table
        create_conversations_sql = '''
        CREATE OR REPLACE TABLE CONVERSATIONS (
            conversation_id STRING PRIMARY KEY,
            user_id STRING REFERENCES USERS(user_id),
            session_id STRING NOT NULL,
            query STRING NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_conversations_sql)
        conn.commit()
        print("CONVERSATIONS table created successfully.")

    except Exception as e:
        print(f"Error creating CONVERSATIONS table: {e}")

    finally:
        cursor.close()
        conn.close()

# Function to create WISHLIST table
def create_wishlist_table():
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        # SQL query to create the WISHLIST table
        create_wishlist_sql = '''
        CREATE OR REPLACE TABLE WISHLIST (
            wishlist_id STRING PRIMARY KEY,
            username STRING NOT NULL,
            recipe_name STRING NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(create_wishlist_sql)
        conn.commit()
        print("WISHLIST table created successfully.")

    except Exception as e:
        print(f"Error creating WISHLIST table: {e}")

    finally:
        cursor.close()
        conn.close()

# Main function to create tables
def main():
    create_users_table()
    create_conversations_table()
    create_wishlist_table()

if __name__ == "__main__":
    main()

