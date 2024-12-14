# langraph-agentic-systems

## Overview

A research tool designed for efficient document parsing, vector storage, and multi-agent research using **Pinecone**, and **Langraph**. This end-to-end solution supports document analysis, interactive Q&A, and professional reporting. The project is powered by a user-friendly interface built with **Streamlit**, enabling streamlined research and interactive document exploration.

## Project Resources

## Project Resources

- **Google Codelab**: [Codelab Link]()
- **App (Deployed on AWS EC2)**: [Streamlit Link]()
- **YouTube Demo**: [Demo Link]()

## Features

### Document Parsing and Vector Storage

- **Vector Storage**: Stores document vectors in Pinecone for scalable and fast similarity searches.

### Multi-Agent Research System (using LangGraph)

- **Document Selection**: Provides access to parsed documents for research purposes.
- **Arxiv Agent**: Retrieves relevant research papers.
- **Web Search Agent**: Expands the research context through online searches.
- **RAG Agent**: Answers user queries using Retrieval-Augmented Generation with Pinecone.

### User Interface and Interaction

- **Streamlit or Coagents**: Interactive platform for conducting research and asking questions (5-6 per document).
- **Session Saving**: Stores the results of each research session for future reference.
- **Professional PDF Export**: Generates templated reports summarizing research findings.

## Architecture

The application includes the following main components:

1. **Document Parsing Pipeline**: Extracts structured information from the provided dataset with Langchain.
2. **Vector Storage**: Saves vectors in Pinecone for efficient document querying.
3. **Research Agents**: Utilizes Langraph to deploy multi-agent systems for comprehensive research.
4. **User Interface**: Built with Streamlit or Coagents for seamless user interaction.
5. **Report Generation**: Professional PDF export

## Technologies

- **Python**: Core programming language
- **Pinecone**: Vector database for similarity search
- **Langraph**: Multi-agent system framework
- **Streamlit**: User interface development
- **Streamlit Community Cloud**: Deployment
- **Render**: FastAPI Deployment

## Architecture Diagram

#### Langgraph Design

<img width="669" alt="image" src="https://github.com/user-attachments/assets/105950e5-b62a-4632-bf6a-acf95abbd659">

#### Streamlit and FastAPI Architecture

<img width="652" alt="image" src="https://github.com/user-attachments/assets/5bad6f9c-adfc-48c0-9891-d16f775df843">

---

## Project References

- **Pinecone**: [Official Website](https://www.pinecone.io/)
- **Langraph**: [Tutorial](https://langchain-ai.github.io/langgraph/tutorials/introduction/)

## How to Run the Application

### Prerequisites

- Pinecone API key
- SerpAPI Key
- Langsmith
- OpenAI API Key

## Contributions

| Name                | Contribution                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| Pragnesh Anekal     | 33% - Langcahin, building Graph using LangGraph, Streamlit Front end, Integrating Download files     |
| Mihir Sanjay Rahate | 33% - Web scraping, building the chat interface, Snowflake setup, Fast API , Pinecone, Arxiv Agent   |
| Dipen Manoj Patel   | 33% - Streamlit Front end, Web Search using SerpAPI, Extract as PDF, Deploying Streamlit and FastAPI |

## Attestation

**WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.**
