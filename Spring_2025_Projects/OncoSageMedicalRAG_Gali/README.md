# Oncno Sage: Medical RAG QA System

## Project Overview
Oncno Sage is a Retrieval-Augmented Generation (RAG) system designed to answer medical questions by combining large language models with a vectorized knowledge base of medical literature.  
**Goals:**  
- Provide evidence-based, verifiable answers to medical queries.  
- Offer transparent source attribution and relevance visualizations.  
- Enable clinicians and researchers to quickly access up-to-date information.  

## Resources

[![Watch Video](https://img.shields.io/badge/YouTube-Video-FF0000?logo=youtube)](https://youtu.be/VaA9NGJIRys)  [![Documentation](https://img.shields.io/badge/Documentation-📄-555?logo=read-the-docs)](docs/) [![Application](https://img.shields.io/badge/Application-live-28a745?logo=streamlit&logoColor=white)](http://3.93.76.163:8501/)

---

## Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://python.org) [![Streamlit](https://img.shields.io/badge/Streamlit-FF4C31?logo=streamlit&logoColor=white)](https://streamlit.io) [![LangChain](https://img.shields.io/badge/LangChain-000000?logo=langchain&logoColor=white)](https://github.com/langchain-ai/langchain) [![Pinecone](https://img.shields.io/badge/Pinecone-5B21B6?logo=pinecone&logoColor=white)](https://pinecone.io) [![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)](https://openai.com) [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com) [![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org) [![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://docker.com) [![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FDAE3F?logo=huggingface&logoColor=white)](https://huggingface.co) [![Amazon EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/ec2)



**Scope & Architecture:**  
- **Frontend:** Streamlit web UI for interactive querying and visualization.  
- **Backend:**  
  - **LangChain** to orchestrate the RAG pipeline.  
  - **Pinecone** vector database to store and retrieve document embeddings.  
  - **OpenAI API** for embeddings and chat completions.  

 
<img width="963" alt="Model_Archietecture" src="https://github.com/user-attachments/assets/d7cd6f14-34dc-4040-9742-e3483b1b7ae6" />


## Architecture Overview

Oncno Sage employs a modular, cloud-ready architecture to deliver medical question answering with full traceability:

- **Frontend (Streamlit):** A Streamlit app runs in the user’s browser, capturing medical queries and rendering answers, relevance bar charts and similarity heatmaps.  
- **Ingestion Pipeline:** PDF documents (stored locally or on AWS S3) are loaded by `ingest.py`, split into overlapping chunks, and embedded using either Hugging Face sentence-transformers (local dev) or OpenAI embeddings (cloud).  
- **Vector Store (Pinecone):** Chunk embeddings are indexed in Pinecone for ultra-fast similarity search.  
- **RAG Orchestration (LangChain):** LangChain’s RetrievalQA chain glues together the retriever and OpenAI’s LLM. Retrieved chunks become context for answer generation.  
- **LLM & Summarization:** OpenAI’s `gpt-3.5-turbo` (or higher) produces the final answer; Gemini AI can optionally post-process or summarize longer responses.  
- **Deployment & Scalability:**  
  - **Docker Compose** packages all services (Streamlit, ingestion, helpers) into containers for consistent environments.  
  - **AWS EC2** hosts the Dockerized stack, ensuring horizontal scalability.  
  - **AWS S3** (optional) holds the raw PDF corpus.  
  - **Environment Variables:** `.env` stores secrets (API keys, Pinecone index name) to keep credentials out of source control.  

---

## Data Flow

1. **Document Ingestion**  
   - Load PDFs from `data/` or S3 → split into 1 000-token chunks → generate embeddings via Hugging Face or OpenAI → push to Pinecone index.  
2. **Query Processing**  
   - User submits a question in the Streamlit UI → LangChain’s retriever fetches the top k relevant chunks from Pinecone → OpenAI LLM generates an evidence-based answer using the retrieved context.  
3. **Response & Visualization**  
   - Streamlit renders the answer in a styled container, displays relevance scores as a Plotly bar chart, and shows a document similarity heatmap.  
   - Expandable source panels list chunk content and metadata for full transparency.  

---

## Installation & Setup

### Prerequisites
- Python 3.8+  
- Docker & Docker Compose (optional)  
- Git  
- OpenAI API Key  
- Pinecone API Key  
---


### Local Setup
```bash
git clone https://github.com/your-org/oncnosage.git
cd oncnosage
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env to add:
# OPENAI_API_KEY=your_openai_key
# PINECONE_API_KEY=your_pinecone_key
# PINECONE_INDEX_NAME=medical-knowledge
```

### Docker Compose
```
docker-compose up --build
```
* The app will be available at http://localhost:8501

## Usage Instructions

### Running Locally
```
# Activate your virtual environment
source venv/bin/activate
# Ingest documents (once)
python ingest.py
# Start the Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
### Testing


Verify both OpenAI and Pinecone integrations before running the app:

```bash
# Activate your venv
source venv/bin/activate    # or `venv\Scripts\activate` on Windows

# Run tests
python test_openai.py
python test_pinecone.py
```


### Sample Queries
*“What are the common side effects of Trastuzumab?”

*“Explain breast cancer treatments in simple terms.”

### Project Structure
<img width="337" alt="ProjectStructure" src="https://github.com/user-attachments/assets/186053e7-66b6-4e06-b171-5c89bfcd79f5" />

### License
* This project is licensed under the MIT License — see the LICENSE file for details.

### Acknowledgments
* LangChain for the RAG framework

* Pinecone for vector-based retrieval

* Streamlit for rapid UI development

* Hugging Face for local embedding models


### Done By Kusumanth - Individual project






