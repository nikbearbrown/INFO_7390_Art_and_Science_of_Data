# Fitness Assistant with Pinecone and LangChain

## Overview
This project creates a fitness assistant powered by Pinecone, LangChain, and Google Generative AI. It leverages Pinecone for vector database management, LangChain for text processing and retrieval, and Gemini LLM for generating AI-driven responses. The system processes fitness-related textual data, embeds it into Pinecone for fast querying, and integrates with the Gemini language model for natural language interaction.

---

## Libraries Used

### Core Dependencies
The following libraries are essential for this project:

- *aiohttp* (3.9.5): Asynchronous HTTP client/server.
- *aiosignal* (1.3.2): Async signal handling.
- *altair* (5.5.0): Declarative statistical visualization library.
- *annotated-types* (0.7.0): Type annotations utility.
- *async-timeout* (4.0.3): Timeout control for async operations.
- *attrs* (24.2.0): Python attributes library.
- *google-generativeai* (0.8.3): Integration with Google's Generative AI.
- *langchain* (0.3.11): Framework for building applications powered by LLMs.
- *langchain-pinecone* (0.2.0): Pinecone integration for LangChain.
- *pinecone* (5.4.2): Pinecone API client.
- *pandas* (2.2.3): Data manipulation and analysis.
- *python-dotenv* (1.0.1): Manage environment variables.

### Additional Libraries
A full list of dependencies is available in the requirements.txt file.

---

## Project Structure


project/
├── createvector_database.py
├── llm_integrations.py
├── requirements.txt
├── data/
│   ├── <text files>
├── .env
├── README.md


- **createvector_database.py**: Main script for creating and managing Pinecone vector indexes and uploading embeddings.
- **llm_integrations.py**: Script for interacting with the Gemini language model.
- **requirements.txt**: Contains all dependencies for the project.
- **data/**: Directory containing text files to process.
- **.env**: Stores sensitive credentials like API keys.

---

## Setup Instructions

### Prerequisites
1. Python 3.10
2. Pinecone account and API key
3. Google Generative AI API key

### Installation

1. Clone the repository:
   bash
   git clone <repository_url>
   cd <repository_name>
   

2. Install dependencies:
   bash
   pip install -r requirements.txt
   

3. Create a .env file in the root directory with the following structure:
   env
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_google_gen_ai_api_key
   

4. Add your text files to the data/ folder.

---

## Execution Instructions

### Step 1: Create Pinecone Vector Database
Run the createvector_database.py script to create a Pinecone index and upload document embeddings:
bash
python createvector_database.py

This script:
- Initializes the Pinecone index.
- Processes and splits text files in the data/ folder.
- Uploads the embeddings to Pinecone.

### Step 2: Query the Fitness Assistant
Use the query_index function to interact with the system:
python
from createvector_database import query_index

response = query_index("What are some quick fitness tips?")
print(response)


### Step 3: Interact with Gemini LLM
You can directly use the Gemini model for general queries by invoking:
python
from llm_integrations import get_response_from_llm

response = get_response_from_llm("Create a workout plan for beginners.")
print(response)


---

## Project Goals

- Develop an AI-powered fitness assistant for efficient querying of fitness-related knowledge.
- Implement a scalable vector database using Pinecone for embedding management.
- Enable seamless natural language interaction through LangChain and Google Generative AI.

---

## Key Features
- *Vector Database*: Efficiently stores and retrieves document embeddings with Pinecone.
- *Text Splitting*: Processes and chunks large text files for embedding.
- *Natural Language Processing*: Uses LangChain and Gemini LLM for conversational AI capabilities.
- *Scalable Infrastructure*: Serverless architecture with AWS integration.

---

## Outputs

- *Accurate Fitness Query Responses*: Provides clear and relevant answers to fitness-related questions.
- *Custom Fitness Plans*: Generates personalized workout plans using Gemini LLM.
- *Improved Data Access*: Allows fast and efficient retrieval of embedded text data.

---

## Troubleshooting

1. *Environment Variable Errors*:
   - Ensure the .env file is correctly configured.
   - Verify API keys are valid.

2. *Data Folder Missing*:
   - Ensure the data/ folder exists and contains .txt files.

3. *Pinecone Index Issues*:
   - Check your Pinecone account for existing indexes.
   - Confirm your API key has the correct permissions.

---

## Future Improvements
- Enhance text splitting for more contextual embedding.
- Add support for more file formats (e.g., PDF, CSV).
- Enable multi-language embeddings.
- Improve conversational capabilities using advanced LLM models.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgments
- *Pinecone*: For vector database management.
- *LangChain*: For making LLM integrations seamless.
- *Google Generative AI*: For advanced natural language generation capabilities.
