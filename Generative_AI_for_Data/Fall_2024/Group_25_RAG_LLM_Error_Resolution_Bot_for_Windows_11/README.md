# RAG-Based LLM Error Resolution Bot for Windows 11

## Table of Contents
- [Introduction](#introduction)
- [Relevance](#relevance)
- [Technologies Used](#technologies-used)
- [Problem Statement](#problem-statement)
- [Architecture Diagram](#architecture-diagram)
- [Desired Outcome](#desired-outcome)
- [File Structure](#file-structure)
- [Features](#features)
- [How It Works](#how-it-works)
- [System Architecture](#system-architecture)
- [Example Use Cases](#example-use-cases)
- [Installation](#installation)
- [Deployment](#deployment)
- [Usage](#usage)
- [Contributors](#contributors)
- [References](#references)
- [Additional Notes](#additional-notes)

---

## Introduction
The **RAG-Based LLM Error Resolution Bot for Windows 11** is an AI-powered troubleshooting tool designed to diagnose and resolve common Windows 11 errors. It leverages **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)** to efficiently retrieve and process error logs, troubleshooting guides, and FAQs, providing users with precise solutions.

---

## Technologies Used
- **Streamlit**: User-friendly interface.
- **LLM (e.g., GPT-4)**: Generates natural language solutions.
- **PDFPlumber** & **BeautifulSoup**: Extract text from PDFs and online documentation.
- **Milvus**: Vector database for storing and retrieving embeddings.
- **Text Embedding Models**: Create vector representations of text.

---

## Problem Statement

### Objective:
Develop an intelligent and automated system for diagnosing, exploring, and resolving common Windows 11 errors.

### Challenges:
1. **Error Identification**: Resolving errors like blue screens, update failures, and performance issues often requires searching through extensive forums and documentation.
2. **Data Complexity**: Error-related data exists in various formats (PDFs, web pages, and databases), making efficient retrieval difficult.

### Goals:
- Efficiently process and store structured/unstructured troubleshooting data.
- Integrate RAG-based workflows to generate contextualized solutions.
- Provide a simple and intuitive user interface for error diagnosis and resolution.

---

## Architecture Diagram
![Screenshot 2024-12-14 214506](https://github.com/user-attachments/assets/eb6071ae-4689-42e8-afb0-2068d44aa4dc)

---

## Desired Outcome
A user-friendly platform that enables users to:
- Diagnose errors by inputting error codes or descriptions.
- View categorized solutions grouped by severity and complexity.
- Use natural language queries to retrieve accurate troubleshooting steps.
- Stay updated with Microsoft documentation and community fixes.
- Analyze error trends for proactive troubleshooting.

---


---

## Features

### 1. **Natural Language Querying**:
   - Input queries like:
     - *"How do I fix the blue screen error with code 0x00000116?"*
     - *"Why is Windows 11 update stuck at 80%?"*

### 2. **Solution Categorization**:
   - Group solutions by:
     - Severity (critical, warning, minor).
     - Step complexity (basic, advanced).

### 3. **Real-Time Updates**:
   - Sync with official Microsoft documentation for up-to-date fixes.

### 4. **Error History Insights**:
   - Analyze trends in past errors to improve future recommendations.

---

## How It Works

### **Data Ingestion**:
- Collect error logs, FAQs, and troubleshooting guides from:
  - Microsoft Support documentation.
  - Community forums and error solution databases.
- Process data using tools like **PDFPlumber** and **BeautifulSoup**.
- Store processed data as vector embeddings in **Milvus**.

### **Error Query Input**:
- Input formats:
  - Specific error codes (e.g., `0x80070005`).
  - Keywords (e.g., *"Windows update stuck"*).
  - Natural language questions (e.g., *"How do I resolve GPU crashes?"*).

### **Error Diagnosis and Resolution**:
- Retrieve solutions from the vector database.
- Use **RAG workflow**:
  - **Retrieve**: Relevant solutions from stored data.
  - **Generate**: LLM creates a precise, context-aware response.

### **Interactive Q&A Interface**:
- Chat-like interface for query refinement and detailed responses.
- Step-by-step troubleshooting instructions.

---

## System Architecture

### **Data Ingestion**:
- Collect data from Microsoft and error databases.

### **Data Processing**:
- Use **PDFPlumber** and **BeautifulSoup** to extract text.
- Generate embeddings with `text-embedding-ada-002`.

### **Storage**:
- Store vector embeddings in **Milvus** with metadata (error code, category, severity).

### **RAG Workflow**:
- **Retrieve**: Fetch solutions from Milvus.
- **Generate**: Use LLM for natural language responses.

### **Frontend**:
- Query input and solution display in a web-based UI.

---

## Example Use Cases
1. **Home Users**:
   - Solve Windows Update errors (e.g., *"Update stuck at 27%"*).
2. **Gamers**:
   - Fix GPU-related crashes on Windows 11.
3. **IT Professionals**:
   - Diagnose BSOD errors across multiple systems.

---
<p>Steps to run this application</p>
<p>Clone the repository:
bashCopygit clone <a href="https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/tree/main/Generative_AI_for_Data/Fall_2024/Group_25_RAG_LLM_Error_Resolution_Bot_for_Windows_11">https://github.com/nikbearbrown/INFO_7390_Art_and_Science_of_Data/tree/main/Generative_AI_for_Data/Fall_2024/Group_25_RAG_LLM_Error_Resolution_Bot_for_Windows_11</a></p>
<p>Install dependencies:
bashCopypip install -r requirements.txt</p>
<p>Set up environment variables:</p>
<p>Create a .env file with the following keys:
MilvusAPI key
LLM model API key</p>
<p>Run the application:
bashCopystreamlit run app.py</p>
<p>Deployment
The system is deployed on Google Cloud Platform (GCP), using Docker for containerized deployment:</p>
<p>Docker: Containers manage FastAPI and Streamlit, with Docker Compose orchestrating the components for consistent deployment.
GCP: Ensures public access to the application and scalable infrastructure to accommodate user demand.</p>
<p>Usage</p>
<p>Query Error Codes:</p>
<p>Enter an error code or keyword in the input box
Receive step-by-step troubleshooting instructions</p>
<p>Explore Error Trends:</p>
<p>View error history and recommendations based on past queries</p>
<p>Access Categorized Solutions:</p>
<p>Browse resolutions grouped by severity and complexity</p>
<p>Contributors</p>
<p>Nagapriyaham Pindi (50%)
Vishodhan Krishnan (50%)</p>
<p>References</p>
<p>Airflow Documentation
FastAPI Documentation
Streamlit Documentation
RAG Model
RAG
LLM
Chatbot</p>
<p>Additional Notes
WE ATTEST THAT WE HAVEN&#39;T USED ANY OTHER STUDENTS&#39; WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.</p>
