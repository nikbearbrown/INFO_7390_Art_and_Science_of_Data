import logging
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
import tiktoken
from typing import List, Optional
from snowflake.connector import connect
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from config import (
    SNOWFLAKE_CONFIG,
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    YOUTUBE_API_KEY,
    INDEX_NAME,
    YOUTUBE_INDEX,
    DIMENSION,
    METRIC,
    CLOUD_PROVIDER,
    REGION,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    client,
    pc,
    youtube,
    index,
    youtube_index,
)
from queue import Queue
import snowflake.connector
from fastapi import Depends
import time

# OAuth2PasswordBearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Module(BaseModel):
    module: int
    title: str
    description: str

class Plan(BaseModel):
    Title: str
    Objective: str
    KeyTopics: List[str]
    Modules: List[Module]
    ExpectedOutcome: str

class SnowflakeConnectionPool:
    def __init__(self, config, maxsize=10):
        self.config = config
        self.pool = Queue(maxsize)
        self.maxsize = maxsize  # Track the max pool size
        self._initialize_pool(maxsize)
        logging.info(f"Initialized SnowflakeConnectionPool with size {maxsize}.")

    def _initialize_pool(self, maxsize):
        for _ in range(maxsize):
            try:
                conn = self._create_connection()
                self.pool.put(conn, timeout=5)
            except Exception as e:
                logging.error(f"Failed to create initial connection: {e}")
                continue  # Continue to ensure maximum number of valid connections.

    def _create_connection(self):
        try:
            conn = snowflake.connector.connect(
                user=self.config['user'],
                password=self.config['password'],
                account=self.config['account'],
                warehouse=self.config['warehouse'],
                database=self.config['database'],
                schema=self.config['schema'],
                validate_default_parameters=True,
            )
            conn.cursor().execute("ALTER SESSION SET TIMEZONE = 'UTC';")
            logging.info("Successfully created a new Snowflake connection.")
            return conn
        except Exception as e:
            logging.error(f"Error creating Snowflake connection: {e}")
            raise HTTPException(status_code=500, detail="Error creating Snowflake connection.")

    def get_connection(self):
        retries = 3
        for attempt in range(retries):
            try:
                connection = self.pool.get(timeout=10)
                if not self._validate_connection(connection):
                    logging.warning("Idle or invalid connection detected. Recreating connection.")
                    connection.close()
                    connection = self._create_connection()
                logging.info("Connection acquired from the pool.")
                return connection
            except Exception as e:
                logging.error(f"Attempt {attempt + 1}/{retries} to get a connection failed: {e}")
                if attempt == retries - 1:
                    self._restore_pool_size()  # Attempt to restore pool size if all retries fail.
                    raise HTTPException(
                        status_code=500,
                        detail="No available database connections in the pool after multiple retries."
                    )

    def release_connection(self, connection):
        try:
            if self._validate_connection(connection):
                self.pool.put(connection, timeout=5)
                logging.info("Connection released back to the pool.")
            else:
                logging.warning("Invalid connection detected during release. Closing connection and recreating.")
                connection.close()
                new_conn = self._create_connection()
                self.pool.put(new_conn, timeout=5)
                logging.info("Replaced invalid connection with a new one in the pool.")
        except Exception as e:
            logging.error(f"Error releasing connection: {e}")
            try:
                new_conn = self._create_connection()
                self.pool.put(new_conn, timeout=5)
                logging.info("Created a new connection during release error to maintain pool size.")
            except Exception as inner_e:
                logging.error(f"Error creating replacement connection during release failure: {inner_e}")


    def _validate_connection(self, connection):
        try:
            connection.cursor().execute("SELECT 1")
            return True
        except Exception as e:
            logging.warning(f"Connection validation failed: {e}")
            return False

    def close_all_connections(self):
        while not self.pool.empty():
            connection = self.pool.get()
            try:
                connection.close()
                logging.info("Connection closed.")
            except Exception as e:
                logging.error(f"Error closing connection: {e}")

    def periodic_validation(self):
        """ Periodically validate and refresh idle connections in the pool. """
        while True:
            try:
                validated_connections = 0
                with self.pool.mutex:
                    for _ in range(self.pool.qsize()):
                        connection = self.pool.get_nowait()
                        if not self._validate_connection(connection):
                            logging.info("Recreating idle or stale connection.")
                            connection.close()
                            connection = self._create_connection()
                        self.pool.put_nowait(connection)
                        validated_connections += 1
                logging.info(f"Periodic validation completed: {validated_connections} connections validated.")
            except Exception as e:
                logging.error(f"Error during periodic validation: {e}")
            time.sleep(60)  # Adjusted interval for validation.

    def _restore_pool_size(self):
        """ Ensure the pool size is restored to the maximum size after failures. """
        try:
            current_size = self.pool.qsize()
            if current_size < self.maxsize:
                for _ in range(self.maxsize - current_size):
                    try:
                        self.pool.put(self._create_connection(), timeout=5)
                        logging.info("Successfully restored connection to the pool.")
                    except Exception as e:
                        logging.error(f"Error restoring connection during pool resize: {e}")
        except Exception as e:
            logging.error(f"Failed to restore pool size: {e}")

pool = SnowflakeConnectionPool(SNOWFLAKE_CONFIG, maxsize=24)

def monitor_pool():
    """
    Monitor the state of the connection pool for debugging purposes.
    Includes enhanced connection state logging.
    """
    try:
        active_connections = pool.pool.qsize()
        logging.info(f"Pool state: {active_connections}/{pool.maxsize} active connections.")
    except Exception as e:
        logging.error(f"Error monitoring pool state: {e}")


# Example usage of monitoring (can be invoked periodically)
monitor_pool()

class YouTubeVideoResponse(BaseModel):
    video_url: Optional[str]
    relevance_score: Optional[float]

# class FlashcardGeneration(BaseModel):
#     question: str
#     answer: str

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardGeneration(BaseModel):
    flashcards: List[Flashcard]

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class QuizGeneration(BaseModel):
    quiz: List[QuizQuestion]

class SummarizationRequest(BaseModel):
    image_urls: List[str]

# class ImageSummaryRequest(BaseModel):
#     module_id: str
#     image_urls: List[str]

class ArxivPaperResponse(BaseModel):
    title: str
    summary: str
    authors: List[str]
    published: str
    link: str
    pdf_url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Deep Learning in Neural Networks: An Overview",
                "summary": "This paper provides an overview of deep learning techniques and their applications.",
                "authors": ["Jürgen Schmidhuber"],
                "published": "2014-09-01T00:00:00Z",
                "link": "http://arxiv.org/abs/1404.7828",
                "pdf_url": "http://arxiv.org/pdf/1404.7828.pdf"
            }
        }

# -------- Utility Functions --------

def get_db_connection():
    """
    Get a connection from the pool. Retry up to 3 times if the pool is exhausted.
    Includes additional validation to ensure no stale connections are used.
    """
    retries = 3
    for attempt in range(retries):
        try:
            connection = pool.get_connection()
            if not pool._validate_connection(connection):
                logging.warning("Detected a stale connection. Attempting to recreate.")
                connection = pool._create_connection()
            return connection
        except HTTPException as e:
            logging.error(f"Attempt {attempt + 1}/{retries} to get a connection failed: {e.detail}")
            if attempt == retries - 1:
                raise HTTPException(
                    status_code=500,
                    detail="Unable to get a database connection after multiple attempts."
                )


# Utility functions
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_user(username: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT USERNAME, PASSWORD, CREATED_AT FROM USERS WHERE USERNAME = %s", (username,))
            row = cursor.fetchone()
            return {"username": row[0], "password": row[1], "created_at": row[2]} if row else None
    finally:
        pool.release_connection(connection)  # Ensure the connection is released back to the pool

def create_user(username: str, password: str):
    hashed_password = get_password_hash(password)
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO USERS (USERNAME, PASSWORD, CREATED_AT) VALUES (%s, %s, %s)""",
                (username, hashed_password, datetime.utcnow())
            )
            connection.commit()
    finally:
        pool.release_connection(connection)  # Ensure the connection is released back to the pool

def inspect_index():
    try:
        results = index.describe_index_stats()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inspecting index")

async def get_current_username(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")