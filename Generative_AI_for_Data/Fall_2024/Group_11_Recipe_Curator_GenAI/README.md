# Recipe Curator: GenAI-powered Recipe Recommendation Platform

## Project Overview

The Recipe Curator is an intelligent platform that provides personalized recipe recommendations based on user inputs. Leveraging advanced technologies like Pinecone, OpenAI, Gemini, and FastAPI, the platform allows users to interact through natural language queries, such as searching for "spicy Indian curries" or "Butter Pecan Cookies." The application integrates **AWS S3**, **Snowflake** for storage, and Dockerized components to ensure scalability and maintainability.

By analyzing user queries and embeddings, Recipe Curator retrieves relevant recipes, generates suggestions, and allows users to create and manage a wishlist. It combines powerful NLP techniques and vector search engines to curate recipes tailored to user preferences, ensuring an engaging and intuitive culinary experience.

---

## Resources

[![YouTube](https://img.shields.io/badge/Watch%20Video-%F0%9F%92%AC%20YouTube-red?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/2ygSkvPSokg)
[![Docs](https://img.shields.io/badge/Documentation-%F0%9F%93%9A%20Docs-blue?style=for-the-badge&logo=read-the-docs&logoColor=white)](https://drive.google.com/file/d/1oAR2gobQzSSdFpAoQOSezkRM6P3O6x_k/view?usp=sharing)
[![App](https://img.shields.io/badge/Application-%F0%9F%92%BB%20App-green?style=for-the-badge&logo=appveyor&logoColor=white)](http://3.144.108.22:8501/)


---

## Tech Stack

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B6F6?style=for-the-badge&logo=snowflake&logoColor=white)
![Python](https://img.shields.io/badge/Python-4B8BBE?style=for-the-badge&logo=python&logoColor=yellow)
![Pinecone](https://img.shields.io/badge/Pinecone-6558F5?style=for-the-badge&logo=pinecone&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FF9900?style=for-the-badge&logo=huggingface&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-purple?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)

---

## Architecture Diagram

<img width="1046" alt="AD of recipe curator" src="https://github.com/user-attachments/assets/95fcba16-779a-4a1b-8704-4a3d4d1b8f63">


The architecture integrates a **Streamlit-based frontend** with a **FastAPI backend**, hosted on **Amazon EC2** for robust scalability. **AWS S3** is utilized for data storage, and cleaned datasets are ingested into **Snowflake** for structured querying. The embedding-based similarity search is powered by **Pinecone**, and **OpenAI's LLMs** enhance the natural language understanding of user queries, while **Gemini AI** supports query summarization. **Hugging Face models** are used for embedding generation, ensuring state-of-the-art NLP capabilities.

The user interacts with the frontend to search for recipes. These queries are passed to FastAPI, which generates embeddings for semantic understanding using **sentence-transformers** models from Hugging Face and retrieves matching recipes from Pinecone. Results are fetched from Snowflake for display on the frontend. The entire system is Dockerized for easy deployment and scalability.

---

## Run the Application

### 1. Clone the Repository:
   ```bash
   git clone https://github.com/sripoojitha-mandali/Recipe_Curator_GenAI.git
   cd Recipe_Curator_GenAI
   ```
### 2. Set Up Environment Variables

Create a `.env` file in the project directory with the following variables:

```env
SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_ACCOUNT=xxxx
SNOWFLAKE_WAREHOUSE=xxxx
SNOWFLAKE_SCHEMA=xxxx
SNOWFLAKE_ROLE=xxxx
SNOWFLAKE_DATABASE=xxxx
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
pinecone_key=xxxx
gemini_key=xxxx
huggingface_key=xxxx
JWT_SECRET=xxxx
```
### 3. Build the Containers

Run the following command to build the Docker containers:

```bash
docker-compose build
```

### 4. Run the Application

Start the application by running:

```bash
docker-compose up
```

Now the application is up and running. Navigate to the following link to check the application in your web browser:

[http://0.0.0.0:8501](http://0.0.0.0:8501)

## Project Structure
<img width="317" alt="Screenshot 2024-12-03 at 5 13 27 PM" src="https://github.com/user-attachments/assets/ce865d49-01f2-42c3-8f44-53ed7e05ffb3">

## Team Members
- Sri Poojitha Mandali
- Vasudha Ambre
- Rasika Kole
