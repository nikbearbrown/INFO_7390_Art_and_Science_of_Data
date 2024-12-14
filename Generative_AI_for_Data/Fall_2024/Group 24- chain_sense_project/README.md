# **ChainSense: Supply Chain Intelligence with Weather Insights*

This project implements a **Retrieval-Augmented Generation (RAG)** system that combines static supply chain knowledge and dynamic real-time weather data to provide accurate and contextually grounded answers to user queries. By integrating **OpenAI GPT**, **Pinecone vector database**, and real-time weather APIs, the system demonstrates how advanced AI can enhance decision-making in logistics and supply chain management.

---

## **Features**

- **Data Preprocessing**: Raw supply chain data in PDF format is converted into clean, structured text chunks for embedding.
- **Embedding**: Text chunks are transformed into vector representations using OpenAI’s `text-embedding-ada-002` model.
- **Indexing**: Vectors are stored in Pinecone, enabling fast semantic search.
- **Dynamic Weather Data Integration**: Fetches real-time weather data, analyzes supply chain impacts, and dynamically embeds it.
- **Contextual Query Answering**: Combines supply chain and weather contexts to generate GPT-based responses.
- **Deployed App**: A live app on Google Cloud Platform (GCP) that lets users interact with the system.

---

## **App Links**

- **App (Deployed on GCP)**: http://35.238.75.76:8501
- **YouTube Demo**: https://youtu.be/nvPpeCmkYGo

---

## **Setup and Installation**

### **1. Prerequisites**

- Python 3.8+
- OpenAI API Key
- Pinecone API Key
- Google Cloud Platform (GCP) account for deployment

### **2. Install Dependencies**

Clone the repository and install the required libraries:

```bash
git clone https://github.com/your-repo-link.git
cd your-repo-link
pip install -r requirements.txt


### 3. Configure Environment Variables
Create a `.env` file with the following keys:

- OPENAI_API_KEY=your-openai-api-key 
- PINECONE_API_KEY=your-pinecone-api-key 
- PINECONE_ENV=your-pinecone-environment


### 4. Run Locally
To test the app locally:

- streamlit run app.py


### 5. How the System Works

Data Preprocessing:
Raw PDFs are converted to text and chunked for embedding.
Embedding:
Text chunks are embedded using OpenAI’s API and indexed in Pinecone.
Real-Time Weather:
Fetches dynamic weather data, preprocesses it, and indexes it for retrieval.
Query Handling:
Retrieves supply chain and weather contexts for a query.
Combines contexts and sends them to GPT-4 to generate the final response.


### 6. Results and Key Takeaways

The system successfully answers supply chain-related queries with contextual accuracy.
Real-time weather data integration enhances the system’s ability to handle dynamic scenarios.
Pinecone indexing ensures fast and scalable semantic search.


### 7 . Challenges and Learnings

Challenges
Handling large datasets required careful preprocessing and chunking to ensure compatibility with OpenAI models.
Real-time data integration demanded robust API error handling and retry mechanisms.
Learnings
Leveraging vector databases like Pinecone significantly improves query efficiency.
Combining static and dynamic data sources in a RAG pipeline enhances the system’s practical value.


###8. Future Enhancements

Expand the system to handle multi-step reasoning for complex queries.
Incorporate additional real-time data sources, such as traffic or inventory levels.
Optimize performance for larger datasets.


###9. Acknowledgements

OpenAI for providing the GPT and embedding models.
Pinecone for their powerful vector database.
Open Meteo API for real-time weather data.
