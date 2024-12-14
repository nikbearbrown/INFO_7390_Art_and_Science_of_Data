from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.generic.storage import Storage
from diagrams.onprem.mlops import Mlflow
from diagrams.generic.database import SQL
from diagrams.generic.compute import Rack
from diagrams.custom import Custom
from diagrams.aws.storage import S3

# Import the Docker icon
from diagrams.onprem.container import Docker

with Diagram("End-to-End Research Tool Architecture", show=False, filename="research_tool_architecture", direction="LR", graph_attr={"ranksep": "1.5", "nodesep": "1.0"}):
    # Combined Pipeline Cluster - Data Acquisition and Preprocessing
    with Cluster("Airflow Pipeline - Data Acquisition and Preprocessing"):
        # Docker icon at the bottom left of the Airflow cluster
        docker_airflow = Docker("Docker")

        # New data acquisition pipeline
        airflow1 = Airflow("Airflow Scheduler")  # Orchestrates the pipeline
        snowflake2 = Custom("Snowflake Database \n (python links)", "images\snowflake.png")  # Snowflake for storing user information
        selenium = Custom("Selenium (Python)", "images\python.png")  # Web scraping with Selenium

        pinecone = Custom("Pinecone Vector Database", "images\pinecone1.png") 

        # Data flow through the new pipeline
        airflow1 >> snowflake2 >> selenium  >> pinecone
        snowflake4 = Custom("Snowflake Database \n metadata for the extracted data", "images\snowflake.png")  # Snowflake for storing user information

        selenium >> snowflake4

        # New data acquisition pipeline
        airflow2 = Airflow("Airflow Scheduler")  # Orchestrates the pipeline
        gfg = Custom("Webpage for link extraction \n (based on keyword)", "images\gfg.png")  # Web scraping with Selenium
        python2 = Custom("Python link generator \n (based on keyword)", "images\python.png")  # Web scraping with Selenium
        snowflake1 = Custom("Snowflake Database \n (python links)", "images\snowflake.png")  # Snowflake for storing user information
        airflow2 >> gfg >> python2 >> snowflake1

    # FastAPI Cluster
    with Cluster("API Management and Authentication"):
        # Docker icon at the bottom left of the FastAPI cluster
        docker_fastapi = Docker("Docker")

        fastapi = Custom("FastAPI Interface", "images\fastapi.png")  # Acts as the API interface for interaction
        jwt_auth = Custom("JWT Authentication", "images\jwt.png")  # JWT authentication for FastAPI access
        jwt_auth >> fastapi  # JWT Authentication for FastAPI access

    # Snowflake Interaction
    snowflake = Custom("Snowflake Database", "images\snowflake.png")  # Snowflake for storing user information
    fastapi >> snowflake  # FastAPI interacts with Snowflake for storing/retrieving user information
    fastapi << snowflake

    # Pinecone Interactions
    pinecone >> fastapi  # Pinecone provides data to FastAPI
    fastapi >> pinecone  # FastAPI interacts with Pinecone for querying

    # Langraph Interaction
    langraph = Custom("Langraph Multi-Agent System", "images\langraph.png")
    fastapi >> langraph  # FastAPI interacts with Langraph for multi-agent processing
    fastapi << langraph  # Langraph also sends data back to FastAPI

    # Agent Cluster
    with Cluster("Multi-Agent System - Research Agents"):
        youtube_agent = Custom("YouTube Agent", "images\youtube.png")
        research_agent = Custom("Reseach Agent", "images\arxiv.png")
        rag_agent = Custom("RAG Agent", "images\Document_Search.png")

        # Langraph interacts with the research agents
        langraph >> [youtube_agent, research_agent, rag_agent]

    # User Interface Cluster
    with Cluster("User Interaction Interface - Frontend"):
        # Docker icon at the bottom left of the Streamlit cluster
        docker_streamlit = Docker("Docker")

        streamlit = Custom("Streamlit User Interface", "images\streamlit.png")  # User interacts with the system via Copilot UI
        streamlit >> fastapi  # Copilot sends user requests to FastAPI
        streamlit << fastapi
