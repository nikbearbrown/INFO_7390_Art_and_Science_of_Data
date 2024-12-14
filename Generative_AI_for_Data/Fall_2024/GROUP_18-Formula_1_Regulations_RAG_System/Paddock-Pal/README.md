# Paddock Pal: Your Comprehensive Formula 1 Companion
- Saurabh Vyawahare
- Aniket Pataloe
- Bhavya Parmar

## Introduction

Formula 1 is a sport renowned for its high-speed drama, technological innovation, and global fan base. However, navigating its complexities—such as intricate race strategies, evolving regulations, and driver statistics—can be challenging. Fans often struggle to find comprehensive, accessible information, while the FIA, the sport's governing body, has faced criticism for inconsistent regulatory decisions that impact race outcomes and championships.

### Background

An example of the challenges within Formula 1 is the controversial 2021 Abu Dhabi Grand Prix, where regulatory decisions heavily influenced the championship outcome. These controversies underscore the need for greater transparency and data-driven decision-making in the sport.

**Paddock Pal** aims to bridge this gap by combining cutting-edge AI technology with a user-friendly platform to provide:

- Easy access to Formula 1 regulations, track details, and historical data.
- A decision-support system for the FIA to ensure fair and accurate penalties.
- An engaging platform for fans to predict race outcomes and explore the intricacies of the sport.

---

## Project Overview

### Objective

The goal of **Paddock Pal** is to create a Retrieval-Augmented Generation (RAG) platform that delivers:

- Comprehensive insights into Formula 1 regulations and race data.
- Interactive features such as a predictive game for fan engagement.
- Decision-support tools for race incidents, ensuring fairness and consistency.

### Scope

Paddock Pal offers a suite of features for:
1. **Fans**: Access to real-time race data, historical insights, and interactive predictions.
2. **FIA Officials**: Real-time regulation analysis to support incident-based decision-making.
3. **Content Creators and Journalists**: Quick, reliable access to F1 data for enhanced content creation.

---

## Key Features

1. **Information Hub**:
   - Access driver profiles, track details, and race analytics.
   - Learn about F1 regulations in an easily digestible format.

2. **RAG-Powered Chatbot**:
   - Ask complex questions about regulations, historical incidents, and live race data.
   - Get clear, accurate answers powered by Pinecone and OpenAI GPT-4.

3. **Predictive Game Module**:
   - Make predictions about race outcomes and driver performance.
   - Engage with F1 strategies through an interactive, gamified experience.

4. **Decision Support for FIA**:
   - Instantly analyze incidents and suggest penalties based on FIA regulations.
   - Enhance transparency and consistency in decision-making.

---

## Methodology

### Data Sources

- **FIA Regulation Documents**: Scraped from [FIA's official website](https://www.fia.com/).
- **OpenF1 API**: Provides real-time race data, standings, and driver statistics.
- **Custom Synthesized Data**: Includes historical race incidents and penalties.

### Technologies Used

#### Backend
- **FastAPI**: Backend framework for managing data requests and integrations.
- **Snowflake**: For storing structured regulation and race data.
- **Pinecone**: Vector database for efficient embedding retrieval.

#### Frontend
- **Streamlit**: Interactive interface with dropdown menus, chat UI, and data visualizations.

#### Data Processing
- **Adobe Extractor**: Extracts text from FIA regulation PDFs.
- **Airflow**: Automates data scraping and ingestion tasks.

#### AI & Machine Learning
- **OpenAI GPT-4**: Delivers RAG-based responses for complex queries.
- **Scikit-Learn**: Powers the predictive game module.

---

## Project Plan and Timeline

### Phase 1: Core Data Setup and Backend Foundation (Week 1)
- Extract and store FIA regulation documents.
- Set up Snowflake and Pinecone databases.
- Develop the FastAPI backend for handling data requests.

### Phase 2: Build Minimum Viable Product (MVP) (Week 2)
- Create a basic Streamlit interface with dropdowns and chatbot capabilities.
- Integrate real-time race data using the OpenF1 API.
- Deploy the RAG bot for regulation-based queries.

### Phase 3: UI Finalization and Testing (Week 3)
- Enhance the user interface for a seamless experience.
- Conduct functional and user acceptance testing.
- Document the platform for ease of use and deployment.

---

## Risks and Mitigation Strategies

### Risks
1. **Time Constraints**: Limited development window.
2. **Data Integration Challenges**: Potential compatibility issues between APIs and databases.
3. **API Reliability**: Outages or usage rate limitations may hinder real-time data feeds.
4. **Testing Limitations**: Insufficient time for thorough testing may leave undetected issues.

### Mitigation
- Prioritize core features and use parallel development for efficiency.
- Standardize data formats and perform incremental integration testing.
- Cache data to mitigate API reliability issues.
- Focus on critical bug fixes during testing to ensure core functionality.

---

## Deliverables

1. **Interactive Platform**:
   - Access to regulations, race data, and predictive tools.
   - Chatbot for regulation-related queries.
2. **Predictive Game**:
   - Engaging feature to increase fan interaction and knowledge of race dynamics.
3. **Documentation**:
   - Comprehensive guide for users and developers.

---

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:
bash
git clone https://github.com/your-repo/paddock-pal.git
cd paddock-pal
### Step 2: Install Dependencies
Install all required dependencies using Poetry:

bash
Copy code
poetry install
### Step 3: Configure Environment Variables
Create a .env file in the root directory and add the following variables:

env
Copy code
OPENAI_API_KEY=your_openai_api_key
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_ACCOUNT=your_snowflake_account
S3_BUCKET_NAME=your_s3_bucket_name
OPENF1_API_KEY=your_openf1_api_key


### Step 4: Initialize Databases
Set up Snowflake for structured data:

Create tables for storing regulatory clauses, historical race information, and user data.
Populate initial data for testing.
Populate Pinecone with embeddings:

Use the text embeddings from OpenAI to index regulatory content in Pinecone.
Configure Amazon S3:

Store FIA PDFs in an S3 bucket for text extraction.


### Step 5: Run Airflow for Automation
Initialize Airflow and set up data scraping:

bash
Copy code
airflow db init
airflow webserver -p 8080
airflow scheduler
Execution Instructions

### Step 1: Start the Backend Server
Run the FastAPI server to handle backend operations:

bash
Copy code
poetry run uvicorn fastapi_app:app --reload
### Step 2: Start the Frontend Application
Run the Streamlit application for the user interface:

bash
Copy code
poetry run streamlit run app.py

### Step 3: Access the Application
Open your browser and navigate to:

arduino
Copy code
http://localhost:8501

## Conclusion

**Paddock Pal** is designed to transform the way Formula 1 fans, professionals, and officials interact with the sport. By integrating advanced AI capabilities with real-time data access and an engaging user interface, the platform will enhance transparency, education, and entertainment. Whether you're a casual fan or a decision-maker in the FIA, Paddock Pal offers tools to enrich your understanding and engagement with Formula 1.

---

## References

1. [Formula 1 Revenue Report](https://www.si.com/fannation/racing/f1briefings/news/f1-reports-huge-revenue-increase-as-revenue-revealed-01j4szmv11p7#:~:text=Formula%20One%20Group%20has%20reported,the%20corresponding%20quarter%20of%202023.)
2. [FIA Official Website](https://www.fia.com/)
