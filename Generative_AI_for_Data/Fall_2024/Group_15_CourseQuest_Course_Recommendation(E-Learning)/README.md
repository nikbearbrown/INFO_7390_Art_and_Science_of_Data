# Course Recommender System

The **Course Recommender System** leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide tailored course recommendations. By integrating Pinecone as a vector database and OpenAI embeddings, the system ensures accurate and contextual responses to user queries through a Streamlit-based user interface.

---

## Features

- **Data Preprocessing**: Cleans and preprocesses raw course data to create a standardized format for embeddings.
- **Embedding Generation**: Utilizes OpenAI's `text-embedding-ada-002` model for creating high-dimensional embeddings.
- **Vector Storage**: Employs Pinecone to store and query course embeddings for efficient retrieval.
- **Contextual Recommendations**: Enhances course suggestions using GPT for detailed and user-friendly outputs.
- **Interactive UI**: Built with Streamlit, allowing users to interact and query course recommendations.

---

## System Architecture

1. **Data Preparation**:
   - Preprocess raw course datasets (CSV) and store structured data in JSON format.
   - Apply text cleaning and stopword removal to optimize data for embeddings.

2. **Embedding Creation and Indexing**:
   - Generate embeddings for course descriptions using OpenAI.
   - Store embeddings and metadata (course title, instructor, level, etc.) in a Pinecone index.

3. **Query and Recommendation**:
   - Convert user queries into embeddings and search Pinecone for similar vectors.
   - Retrieve contextual data and summarize recommendations using GPT.

4. **User Interface**:
   - Streamlit app to input queries and display course recommendations with detailed metadata.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/course-recommender.git
   cd course-recommender
