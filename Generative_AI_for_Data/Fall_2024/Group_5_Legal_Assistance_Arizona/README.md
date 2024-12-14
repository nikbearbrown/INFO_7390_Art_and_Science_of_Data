# 📚 **Legal Case Semantic Search and Retrieval-Augmented Generation (RAG) System**

Welcome to the **Legal Case Semantic Search and RAG System** repository! This project implements a powerful **semantic search engine** and **retrieval-augmented generation (RAG)** pipeline designed to process large volumes of legal case data, primarily focused on laws related to the state of **Arizona, USA**. Leveraging FAISS for similarity search, OpenAI embeddings, and a user-friendly Streamlit interface, this project enables seamless querying and interaction with legal documents.

---


## **🚀 Project Overview**
![image](https://github.com/user-attachments/assets/6edc4229-8246-4201-a775-e5949522d85a)
This system provides:

- **Semantic Search**: Retrieve the most relevant legal documents based on user queries.
- **RAG (Retrieval-Augmented Generation)**: Generate natural language responses to queries, enriched with relevant legal context.
- **Interactive Frontend**: A chat-based interface using Streamlit for user interactions.
- **API Backend**: A Flask API for embedding generation, similarity search, and GPT-based responses.

---

## **📂 Repository Structure**

```
.
├── app.py                 # Streamlit frontend application
├── api.py                 # Flask backend API
├── faiss_index.index      # Precomputed FAISS index for semantic search
├── id_mapping.pkl         # Mapping of FAISS indices to document IDs
├── content_dict.pkl       # Metadata and content chunks of legal documents
├── requirements.txt       # Required Python packages
└── README.md              # This file
```

---

## **🛠️ Features**

### 1️⃣ **Embeddings Creation**
- **OpenAI Embeddings**: Converts legal documents and user queries into high-dimensional vector space using the `text-embedding-ada-002` model.
- **High Precision**: Enables semantic understanding and matching of queries to relevant content.

### 2️⃣ **Semantic Search Engine**
- **FAISS Index**: Stores vector embeddings of legal document chunks for fast similarity searches.
- **Efficient Retrieval**: Query the FAISS index to find top-k most relevant legal documents based on vector similarity.

### 3️⃣ **RAG (Retrieval-Augmented Generation)**
- **OpenAI GPT Integration**: Generates natural language responses enriched with retrieved context.
- **Dynamic Context Construction**: Combines relevant document chunks to create a contextual basis for answering queries.

### 4️⃣ **Interactive Frontend**
- **Streamlit Interface**: Provides an intuitive chat-like interface for users.
- **Real-Time Responses**: Submit queries and receive responses in real-time.

### 5️⃣ **Robust API**
- **Flask Backend**: Handles embedding generation, semantic search, and RAG pipeline via RESTful endpoints.

---

## **🔖 How It Works**

### **Step 1: Embedding Creation**
- **Process**: Both legal document chunks and user queries are converted into vector embeddings using OpenAI’s `text-embedding-ada-002` model. These embeddings represent the semantic meaning of the text in a high-dimensional space.

- **Theory**: Embeddings are numerical representations of text that capture meaning, context, and relationships between words. They enable semantic comparison by allowing text to be treated as vectors, where similar meanings have closer representations in high-dimensional space.

---

### **Step 2: Similarity Search with FAISS**
- **Process**: Query embeddings are matched against precomputed embeddings stored in the FAISS index to retrieve the top-k most relevant results based on cosine similarity.

- **Theory**: 
  - **Cosine Similarity**: Measures the cosine of the angle between two vectors. A smaller angle indicates higher similarity, making it ideal for determining how close the query embedding is to document embeddings.
  - **FAISS**: Developed by Facebook AI, FAISS optimizes vector similarity searches. It employs clustering and quantization to handle millions of embeddings efficiently, enabling near-instantaneous retrieval.

---

### **Step 3: Retrieval-Augmented Generation (RAG)**
- **Process**: The system dynamically constructs a context using the retrieved top-k results. This context is then input into OpenAI’s GPT model to generate a comprehensive and natural language response.

- **Theory**: 
  - **RAG**: Combines retrieval and generation to improve response relevance. Instead of relying solely on a language model’s internal knowledge, RAG ensures generated responses are grounded in external data, enhancing factual accuracy.
  - **Context Construction**: By concatenating relevant document chunks, the system provides GPT with the information needed to answer queries effectively.

---

### **Step 4: Interactive Display**
- **Process**: Responses and retrieved document snippets are displayed in a user-friendly Streamlit interface, allowing users to interact with the system in real time.

- **Theory**: Streamlit simplifies creating interactive web applications. By integrating real-time data exchange between the backend and frontend, it ensures a smooth user experience.

---

## **🔬 Theory Behind the Project**

### **Semantic Search**
Semantic search enhances traditional keyword-based search by considering the meaning of text rather than exact matches. This project employs embeddings to achieve semantic understanding, enabling the system to find relevant documents even when exact terms don’t match.

### **Embeddings**
Embeddings encode textual data into dense vector representations, capturing semantic meaning and context. For example, "law" and "legal" would have embeddings closer in vector space than "law" and "apple." This allows semantic search systems to infer relevance based on meaning rather than keywords.

### **Vector Similarity Search**
- **How it Works**: The query embedding is compared to document embeddings using cosine similarity. FAISS optimizes this process by indexing embeddings for fast and efficient similarity searches.
- **Applications**: Beyond legal search, vector similarity search powers recommendation systems, image search, and more.

### **Retrieval-Augmented Generation (RAG)**
RAG bridges the gap between information retrieval and generative AI. By retrieving context-specific data, it ensures language models generate responses that are grounded, relevant, and factual. This makes it particularly valuable in domains like legal research, where accuracy is paramount.

---

## **🔖 Setup Instructions**

### **Prerequisites**
- Python 3.8+
- OpenAI API key

### **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/legal-case-rag.git
   cd legal-case-rag
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

4. Run the Flask API:
   ```bash
   python api.py
   ```

5. Launch the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## **🖼️ Project Architecture**

```plaintext
+-----------------------+
|     User Query        |
+-----------------------+
             |
             v
+-----------------------+
|   Streamlit Frontend  | <--------> Flask API
+-----------------------+
             |
             v
+-----------------------+
|  FAISS Similarity     | -----> Retrieve Top-K Results
+-----------------------+
             |
             v
+-----------------------+
|  RAG with GPT Model   | -----> Generate Contextual Response
+-----------------------+
```

---

## **🔑 Key Components**

### **1. FAISS Index**
- Stores vector embeddings for fast similarity searches.
- Efficiently retrieves top-k most relevant document chunks.

### **2. OpenAI Embeddings**
- Embeds textual data into vector space using `text-embedding-ada-002`.
- Converts both document chunks and user queries into comparable formats.

### **3. Flask API**
- Provides endpoints for:
  - Generating embeddings.
  - Performing similarity search.
  - Handling RAG workflows.

### **4. Streamlit Frontend**
- User-friendly interface to interact with the system.
- Displays real-time query results and GPT-generated responses.

---

## **💡 Key Learnings**
- Semantic search improves precision in retrieving legal documents.
- RAG enables contextual and dynamic query answering.
- Efficient indexing (FAISS) ensures scalability for large datasets.

---

## **📝 License**
MIT License

Copyright (c) 2024 [Chiranjit Banerjee, Sathwik Matcha, Dhanush Nandesh]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

🎯 **Empower your legal research with intelligent search and RAG today!**

