# Career Navigator AI

## Overview

Career Navigator AI is a **domain-specific RAG (Retrieval-Augmented Generation) application** built to assist job seekers and recruiters in finding the best matches between resumes and job descriptions.  
By leveraging **semantic search with embeddings**, a **vector database (Pinecone)**, and **Large Language Models (LLMs)**, Career Navigator AI creates a smart and interactive platform for career exploration.

This project is submitted as part of the INFO 7390 Spring 2025 Final Project, following **Option 1: AI-Powered RAG Application**.

---

## Project Goals

- Create a **semantic search engine** for matching resumes and job descriptions.
- Use **domain-specific datasets** of resumes and job descriptions.
- Integrate **Pinecone** as a **vector database** for efficient retrieval.
- Leverage **sentence-transformer models** (`all-MiniLM-L6-v2`) to create high-quality text embeddings.
- Build an interactive **Streamlit** UI for users to input queries and view relevant matches.

---

## Tools and Technologies

- **Vector Database:** Pinecone
- **Embeddings Model:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Frontend:** Streamlit
- **Backend:** Python (Pandas, dotenv, Pinecone SDK)
- **Environment Management:** venv (Python Virtual Environment)

---

## Project Architecture

```plaintext
[User Input] ➔ [Embedding Model] ➔ [Pinecone Semantic Search] ➔ [Relevant Matches] ➔ [Display in Streamlit]
```

---

## Team Contribution

| Name | Contribution |
|------|--------------|
| **Weijia Yan** | Led the backend development, including data preprocessing, embedding generation, and Pinecone integration. Built the semantic search logic and designed the Streamlit application structure. Also responsible for final project integration and deployment. |
| **Ming-Tse Chen** | Focused on frontend improvements in Streamlit, user interface refinement, search result visualization, and contributed to dataset cleaning and validation. Participated in testing and optimization for search performance. |

---
dataset link:https://www.kaggle.com/datasets/pranavvenugo/resume-and-job-description
