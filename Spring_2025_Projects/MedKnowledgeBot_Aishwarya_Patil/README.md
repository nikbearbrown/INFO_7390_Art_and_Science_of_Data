# MediQBot: Multimodal Knowledge Retrieval for Medical Information
Application Link: https://mediqbotads-gzgzqrmh3c73dufmjevbba.streamlit.app/

## Project Overview
MediQBot is a comprehensive medical question answering system built using Retrieval Augmented Generation (RAG). It provides accurate, source-cited answers to questions about diabetes, cancer, cardiovascular disease, infectious disease, and mental health by drawing on a knowledge base of medical articles and educational videos.

## Data Collection and Processing Pipeline

### 1. Medical Article Collection
- **Source**: BMC Medicine journal articles
- **Method**: Built a web scraper using Selenium to extract metadata and PDF URLs
- **Data Collected**: Over 1,000 articles covering key medical topics including:
  - Diabetes research and treatments
  - Cancer studies and therapies
  - Cardiovascular disease management
  - Infectious disease research
  - Mental health findings

### 2. YouTube Medical Content Collection
- **Implementation**: Utilized the YouTube API to collect educational videos
- **Focus**: Medical channels and content covering the five key health topics
- **Dataset**: Gathered 49 educational videos with professional medical content
- **Metadata**: Preserved important context (channel, publication date, view count)

### 3. Data Storage and Processing

#### S3 Storage Implementation
- Created an AWS S3 bucket for structured data storage
- Organized into separate directories for articles, videos, and metadata
- Implemented secure API key management using environment variables
- S3 structure:
mediqbot-data/
├── articles/pdfs/           # PDF files of medical articles
├── metadata/
│   ├── articles/            # Article metadata CSVs
│   ├── videos/              # Video metadata CSVs
│   └── processed/           # Enhanced metadata
└── processed/               # Combined JSON data
- I have added two csv files in the data folder for preview of my dataset
#### Text Extraction Pipeline
- **For Articles**: Used PyPDF2 to extract text from PDF files
- **For Videos**: Utilized YouTube's transcript API to obtain video content
- **Challenge**: Handled character encoding and malformed content issues
- **Output**: Structured JSON files with full text and associated metadata

### 4. Vector Database Implementation
- **Technology**: Pinecone vector database
- **Preprocessing**: 
- Chunked long texts into manageable segments (500 words with 50-word overlap)
- Created embeddings using OpenAI's text-embedding-ada-002 model
- **Indexing**: 
- Created a unified index with both article and video content
- Preserved metadata for source attribution and filtering
- Applied content-type tagging for differentiated retrieval

## RAG System Architecture

### Knowledge Retrieval
- **Semantic Search**: Converts user queries into embeddings for similarity search
- **Relevance Filtering**: Applies a 0.6 similarity threshold to ensure quality matches
- **Context Assembly**: Dynamically combines relevant text chunks into comprehensive context

### Response Generation
- **LLM Integration**: Uses Groq's LLaMA 3 70B model for high-quality responses
- **Prompt Engineering**: Carefully crafted system and user prompts that:
- Require source attribution
- Prevent hallucination
- Enforce domain limitations
- Include medical disclaimers

### Guardrails Implementation
- **Medical Topic Validation**: Ensures queries relate to supported medical domains
- **Source Limitation**: Forces responses to only use retrieved information
- **Disclaimer System**: Clearly communicates the system's informational (not medical advice) nature
- **Ethical Boundaries**: Rejects inappropriate or harmful requests

## User Interface

- **Technology**: Streamlit for accessible, responsive interface
- **Features**:
- Clean, intuitive question input
- Comprehensive answers with source citations
- Expandable source information panels
- Embedded YouTube videos when available
- Response download functionality
- Medical disclaimer

## Deployment

- **Platform**: Streamlit Cloud for easy access and sharing
- **Security**: API keys stored securely using Streamlit's secrets management
- **Updates**: Automatic redeployment through GitHub integration

## Future Enhancements

- Expanded medical topic coverage
- Integration of more specialized medical knowledge sources
- Advanced user personalization
- Citation formatting improvements
- Multi-language support

## Technologies Used

- **Data Collection**: Selenium, YouTube API, Requests
- **Data Processing**: PyPDF2, pandas, JSON
- **Storage**: AWS S3
- **Embeddings**: OpenAI Embeddings API
- **Vector Database**: Pinecone
- **LLM**: Groq LLaMA 3 70B
- **Frontend**: Streamlit
- **Deployment**: Streamlit Cloud

## Installation and Setup

For local development:

# Clone repository
git clone https://github.com/yourusername/mediqbot.git
cd mediqbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables in .env file
# PINECONE_API_KEY=your_pinecone_api_key
# OPENAI_API_KEY=your_openai_api_key
# GROQ_API_KEY=your_groq_api_key

# Run the application
streamlit run app.py