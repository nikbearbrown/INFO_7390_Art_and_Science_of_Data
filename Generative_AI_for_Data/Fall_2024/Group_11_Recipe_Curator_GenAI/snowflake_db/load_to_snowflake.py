import os
import boto3
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS and Snowflake credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

# Step 1: Create the table in Snowflake
def create_table_in_snowflake():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cursor = conn.cursor()

    try:
        # Drop the table if it exists
        drop_table_sql = '''
        DROP TABLE IF EXISTS RECIPES;
        '''
        cursor.execute(drop_table_sql)
        print("Table dropped successfully in Snowflake (if it existed).")
        
        # Create the table
        create_table_sql = '''
        CREATE TABLE RECIPES (
            RecipeId STRING,
            Barcode STRING,
            Name STRING,
            AuthorId STRING,
            AuthorName STRING,
            CookTime STRING,
            PrepTime STRING,
            TotalTime STRING,
            DatePublished STRING,
            Description STRING,
            Images STRING,
            RecipeCategory STRING,
            Keywords STRING,
            RecipeIngredientQuantities STRING,
            RecipeIngredientParts STRING,
            AggregatedRating STRING,
            ReviewCount STRING,
            Calories STRING,
            FatContent STRING,
            SaturatedFatContent STRING,
            CholesterolContent STRING,
            SodiumContent STRING,
            CarbohydrateContent STRING,
            FiberContent STRING,
            SugarContent STRING,
            ProteinContent STRING,
            RecipeServings STRING,
            RecipeYield STRING,
            RecipeInstructions STRING
        );
        '''
        cursor.execute(create_table_sql)
        print("Table created successfully in Snowflake.")
    except Exception as e:
        print(f"Failed to create table in Snowflake: {e}")
    finally:
        cursor.close()
        conn.close()

# Step 2: Load data from S3 to Snowflake using COPY INTO
def load_data_into_snowflake_from_s3():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cursor = conn.cursor()

    try:
        # Define the COPY INTO command
        copy_into_sql = f'''
        COPY INTO RECIPES
        FROM 's3://{S3_BUCKET_NAME}/recipes_data/cleaned_recipes_data.csv'
        CREDENTIALS = (
            AWS_KEY_ID = '{AWS_ACCESS_KEY_ID}'
            AWS_SECRET_KEY = '{AWS_SECRET_ACCESS_KEY}'
        )
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
        ON_ERROR = 'CONTINUE';
        '''
        cursor.execute(copy_into_sql)
        print("Data loaded into Snowflake successfully.")
    except Exception as e:
        print(f"Failed to load data into Snowflake: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # First, create the Snowflake table
    create_table_in_snowflake()

    # Then, load the data from the S3 bucket into Snowflake
    load_data_into_snowflake_from_s3()

