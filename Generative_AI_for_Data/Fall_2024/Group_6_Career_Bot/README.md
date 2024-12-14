                                                 PRAJNA- The Career Guidance ChatBot
                                                                           Group 6

Introduction
The Career Guidance Bot is an innovative application leveraging cutting-edge technologies like OpenAI’s GPT models and Pinecone’s vector database to offer users intelligent, domain-specific recommendations and insights. The project is a part of our larger exploration into Generative AI applications, focusing on developing a Retrieval-Augmented Generation (RAG) application that combines semantic search with conversational capabilities.
The bot is designed to assist users in career-related decision-making by answering queries, providing relevant suggestions, and delivering insightful responses based on preprocessed career-related data. From offering tips for resume building to exploring trending skills in the job market, the bot aims to enhance user experience through interactive and meaningful guidance.
This document aims to provide a comprehensive overview of the project goals, technologies utilized, and the outputs generated, showcasing how state-of-the-art AI and database systems can be harnessed to solve real-world problems effectively.


Project Goals
The Career Guidance Bot project aims to address the following goals in an elaborate manner:
________________________________________
1. Develop a Domain-Specific RAG Application
The primary goal is to create a Retrieval-Augmented Generation (RAG) application that caters specifically to career guidance. This involves:
•	Combining Large Language Models (LLMs) with a vector database to provide precise, contextually relevant responses to user queries.
•	Enabling semantic search capabilities to fetch domain-specific knowledge efficiently.
________________________________________
2. Provide Accurate and Contextual Career Insights
The bot is designed to:
•	Deliver accurate responses to career-related questions by leveraging a preprocessed dataset on career guidance.
•	Offer insights on skills, roles, certifications, and market trends tailored to user needs.
________________________________________
3. Enhance User Experience with Interactive Features
This goal focuses on improving usability and engagement by:
•	Providing users with a conversational interface via Streamlit for a seamless experience.
•	Retaining chat history to foster continuity in user interactions.
•	Including suggestions and starter prompts to guide users toward effective queries.
________________________________________
4. Seamless Integration of Technologies
The project emphasizes the integration of advanced technologies, including:
•	OpenAI GPT Models: For generating human-like responses.
•	Pinecone Vector Database: For semantic search and efficient data retrieval.
•	Streamlit Framework: To develop a user-friendly web application interface.
________________________________________
5. Enable Easy Scalability and Reusability
The project is built with scalability in mind, ensuring:
•	The ability to expand the dataset for different domains or career fields.
•	Modularity in design for reusability across similar applications in education, healthcare, or other sectors.
________________________________________
6. Showcase Practical Use of Generative AI
As part of an academic portfolio, the bot demonstrates:
•	The practical implementation of AI in solving real-world problems.
•	The combination of data preprocessing, embedding generation, and conversational AI to build impactful applications.
Technologies Used
To achieve the goals of the Career Guidance Bot project, the following technologies were utilized:
________________________________________
1. OpenAI GPT Models
•	Model Used: GPT-4
•	Purpose: To generate conversational and contextually accurate responses to user queries.
•	Features:
o	Advanced natural language understanding.
o	Capability to process user input and generate meaningful, human-like responses.
o	Flexibility to customize prompts and system roles for specific tasks.
________________________________________
2. Pinecone Vector Database
•	Purpose: For semantic search and efficient data retrieval.
•	Features:
o	Indexing and querying of embeddings generated from the preprocessed career guidance dataset.
o	Fast and scalable vector search functionality.
o	Support for cosine similarity, ensuring precise document matching.
________________________________________
3. LangChain Framework
•	Purpose: To connect the OpenAI model with the Pinecone vector database seamlessly.
•	Features:
o	Text preprocessing, splitting, and embedding generation.
o	Retrieval-Augmented Generation (RAG) implementation to augment GPT responses with context from the vector database.
________________________________________
4. Streamlit Framework
•	Purpose: To develop a user-friendly web application interface.
•	Features:
o	Dynamic chat UI with history retention for a natural conversational experience.
o	Integration of dropdown menus for starter prompts and suggestions to guide user queries.
o	Intuitive controls for user inputs and response visualization.
________________________________________
5. Python Programming
•	Libraries Used:
o	openai: For API calls to generate embeddings and responses.
o	pinecone-client: For managing the vector database.
o	streamlit: To create the interactive user interface.
o	streamlit-chat: For displaying chat history and enhancing the user experience.
o	langchain: For embedding generation and retrieval functionality.
o	transformers (optional): For advanced NLP tasks if needed.
________________________________________
6. Data Preprocessing Tools
•	Tools and Libraries:
o	Textbook and Career Guidance Dataset: Cleaned and split into smaller, meaningful chunks for embedding generation.
o	LangChain Text Splitter: Used to split the data into optimized chunks (500 characters with 50-character overlap).
o	OpenAI Embedding API: Used to create embeddings for the dataset using the text-embedding-ada-002 model.
Project Outputs
The Career Guidance Bot project delivered the following tangible outputs:
________________________________________
1. Chatbot Application
•	Description: A fully functional, user-friendly chatbot that provides personalized career guidance.
•	Features:
o	Dynamic Chat Interface: Displays real-time query responses along with conversation history.
o	Starter Prompts: Dropdown menu offering pre-filled suggestions for commonly asked career questions.
o	Intuitive UI: Built with Streamlit, ensuring ease of use and accessibility.
________________________________________
2. Semantic Search Functionality
•	Description: Seamless integration of OpenAI GPT-4 with the Pinecone vector database to enhance responses with contextual relevance.
•	Features:
o	Retrieval-Augmented Generation (RAG) technique to include relevant data from the career guidance dataset.
o	Efficient semantic search and matching of user queries with preprocessed data.
________________________________________
3. Preprocessed Dataset
•	Description: A domain-specific dataset covering career guidance topics, split into optimized chunks for embedding generation.
•	Features:
o	Includes details on various career paths, skills required, tips, and industry-specific insights.
o	Indexed in Pinecone for quick retrieval and contextual response generation.
________________________________________
4. Deployment and Hosting
•	Description: The chatbot is hosted using Streamlit, making it accessible via a web interface.
•	Features:
o	Fully operational in any browser environment.
o	Easy to set up and maintain with clear instructions.
________________________________________
5. Documentation and Code Repository
•	Description: Comprehensive documentation and repository for project setup, execution, and usage.
•	Contents:
o	Source code with comments for easy understanding and modification.
o	Step-by-step instructions for setup, execution, and troubleshooting.
o	README file summarizing the project, tools used, and setup guide.
________________________________________
6. Integration and Results
•	Outputs Observed:
o	The chatbot successfully answered career-related queries with relevant, insightful responses.
o	Real-time retrieval of context from the vector database enhanced the accuracy and reliability of responses.
o	User experience validated with smooth interactions and accurate guidance.

CODE SNIPPETS
1.Python notebook:-
Code- 
"
!pip install openai==0.28
# Install required libraries
!pip install pinecone-client openai langchain

# Import dependencies
from pinecone import Pinecone, ServerlessSpec
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Step 1: Combine and Preprocess Data
with open("Textbook3.txt", "r", encoding="utf-8") as file1, open("career_guidance_text_expanded.txt", "r", encoding="utf-8") as file2:
    combined_text = file1.read() + "\n" + file2.read()

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(combined_text)
print(f"Total chunks created: {len(chunks)}")

# Step 2: Generate Embeddings for Text Chunks
openai.api_key = "api-key-here"

embeddings = []
for chunk in chunks:
    response = openai.Embedding.create(input=chunk, model="text-embedding-ada-002")
    embeddings.append(response['data'][0]['embedding'])

print(f"Generated {len(embeddings)} embeddings.")

# Step 3: Initialize Pinecone
api_key = "pinecone-api-key"
index_name = "career-guidance"
host = "pine-cone-host"

pc = Pinecone(api_key=api_key)

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
print(f"Index '{index_name}' created or already exists.")

index = pc.Index(name=index_name, host=host)

# Step 4: Upsert Embeddings into Pinecone
for i, embedding in enumerate(embeddings):
    index.upsert([(f"chunk-{i}", embedding, {"text": chunks[i]})])

print(f"Upserted {len(embeddings)} embeddings into Pinecone index '{index_name}'.")

# Step 5: Query and Retrieve Relevant Context
query = "What are the qualifications for a software engineer?"
query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']

query_result = index.query(vector=query_embedding, top_k=5, include_metadata=True)

# Combine top results into a single context
context = "\n\n".join([match['metadata']['text'] for match in query_result['matches']])
print("Context Retrieved:\n", context)

# Use OpenAI Chat Model (v1/chat/completions)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful career guidance assistant."},
        {"role": "user", "content": f"Context: {context}\n\nQuery: {query}\n\nAnswer:"}
    ],
    max_tokens=300,
    temperature=0.5
)

# Print the chatbot response
print("Chatbot Response:", response['choices'][0]['message']['content'].strip())”


 
 
 
Explanation:
Step 1: Combine and Preprocess Data
The first step is to prepare the data that will be used for the application. Two text files containing relevant information are combined into a single dataset. This combined dataset is then divided into smaller, manageable chunks to enable efficient processing and embedding generation.
Step 2: Generate Embeddings for Text Chunks
Each text chunk is transformed into a numerical representation called an embedding. These embeddings capture the semantic meaning of the text and allow the system to perform similarity searches. OpenAI’s embedding model is used to generate these representations for all the chunks.
Step 3: Initialize the Pinecone Vector Database
A vector database, Pinecone, is set up to store and manage the embeddings. This ensures efficient retrieval of relevant information based on user queries. An index is created in Pinecone to hold the embeddings, enabling semantic searches later in the process.
Step 4: Store Embeddings in the Pinecone Database
The embeddings generated in the previous step are uploaded (upserted) into the Pinecone database along with their associated text chunks. This step prepares the database to retrieve relevant text chunks based on query embeddings.
Step 5: Query and Retrieve Relevant Context
When a user submits a query, it is converted into an embedding using OpenAI's embedding model. The Pinecone database is queried with this embedding to find the most relevant text chunks. These text chunks are then combined to form a context that provides the necessary information for the query.
Step 6: Generate a Response Using OpenAI GPT
The combined context and the user’s query are passed to OpenAI’s GPT-4 model. The model uses this input to generate a detailed and accurate response. This final step ensures the chatbot provides helpful and context-aware answers to user queries.
By following these steps, a robust, intelligent chatbot capable of providing relevant and accurate career guidance is created.

2. Snowflake:
Actual code- 
1. Importing Libraries
python
Copy code
import streamlit as st
import openai
from pinecone import Pinecone
Streamlit: Used to build the web application interface.
OpenAI: Accesses the OpenAI API for GPT-4 and embeddings.
Pinecone: Used for semantic search by storing and querying vector embeddings.
2. Initializing OpenAI API
python
Copy code
openai.api_key = "your-openai-api-key"
Sets up the OpenAI API key for embedding generation and GPT-4 query handling.
Ensure the API key is valid and has permissions for embedding and GPT-based operations.
3. Initializing Pinecone
python
Copy code
api_key = "your-pinecone-api-key"
host = "https://career-guidance-index..."
pc = Pinecone(api_key=api_key)
index_name = "career-guidance"
Pinecone API Key and Host: Configures Pinecone to interact with the vector database.
Index Name: Specifies the name of the Pinecone index (career-guidance) for storing and retrieving vector embeddings.
4. Checking and Creating Pinecone Index
python
Copy code
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Matches the embedding size
        metric="cosine"
    )
Index Existence Check: Verifies whether the career-guidance index exists in Pinecone.
Index Creation: Creates the index with:
dimension: The size of the embedding vectors (1536 for text-embedding-ada-002).
metric: The cosine similarity metric for vector comparison.
5. Connecting to the Index
python
Copy code
index = pc.Index(name=index_name, host=host)
Establishes a connection to the Pinecone index to perform search and retrieval operations.
6. Streamlit App Setup
python
Copy code
st.title("PRAJNA- The Career Guidance Bot")
st.markdown("""
    Welcome to *PRAJNA*, your personal career guidance assistant!  
    🔍 Ask questions about career growth, skills, opportunities, and more.  
    🤖 Powered by OpenAI and Pinecone for intelligent responses.
""")
Title: Displays the app name on the web interface.
Markdown: Adds descriptive text to introduce the bot and its purpose.
7. Initializing Chat History in Session State
python
Copy code
if "messages" not in st.session_state:
    st.session_state.messages = []
Maintains chat history for the session using Streamlit's session_state.
Ensures that past user and bot messages are displayed for a conversational experience.
8. Trimming Chat History
python
Copy code
def trim_chat_history():
    if len(st.session_state.messages) > 6:  # Keeps last 3 user-bot pairs
        st.session_state.messages = st.session_state.messages[-6:]
Purpose: Limits the number of chat pairs to three to avoid overwhelming memory and clutter in the UI.
Ensures the bot maintains a manageable conversational context.
9. Handling Query Submission
python
Copy code
def handle_query():
    query = st.session_state.query
    if query:
        # Add query to history
        st.session_state.messages.append({"role": "user", "content": query})

        # Generate embedding
        response = openai.Embedding.create(model="text-embedding-ada-002", input=query)
        query_embedding = response['data'][0]['embedding']

        # Query Pinecone
        query_result = index.query(vector=query_embedding, top_k=5, include_metadata=True)

        # Combine contexts
        context = "\n\n".join([match['metadata']['text'] for match in query_result['matches']])

        # Generate GPT-4 response
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages + [
                {"role": "system", "content": "You are a helpful career guidance assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            max_tokens=300,
            temperature=0.5
        )
        bot_response = gpt_response['choices'][0]['message']['content'].strip()

        # Add bot response to history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Trim chat history
        trim_chat_history()

        # Clear input field
        st.session_state.query = ""
    else:
        st.warning("Please enter a query!")
Steps in Query Handling:
User Query: Captures the query entered by the user.
Embedding Generation: Uses text-embedding-ada-002 to convert the query into a vector.
Pinecone Query: Retrieves the most relevant text snippets (top 5) based on vector similarity.
Context Combination: Merges the retrieved text snippets to create a meaningful context.
GPT-4 Response: Sends the combined context and query to GPT-4 for generating a response.
History Management: Adds the query and bot response to the chat history and trims older messages.
10. Displaying Chat History
python
Copy code
st.write("### Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"*User:* {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"*Prajna:* {message['content']}")
Displays the chat history in the web interface.
Differentiates between messages from the user (User:) and the bot (Prajna:).
11. User Input Field
python
Copy code
st.text_input(
    "Enter your query:",
    key="query",
    on_change=handle_query,
    placeholder="Type your question and press Enter..."
)
Provides a text input field for users to enter their queries.
Automatically triggers the handle_query function when the user presses Enter.
Key Features of the Application
User-Friendly Interface: Built using Streamlit for an intuitive experience.
Intelligent Retrieval: Combines OpenAI embeddings and Pinecone for semantic search.
Dynamic Responses: GPT-4 generates contextually rich and meaningful replies.
Chat Continuity: Maintains a conversation-like history for better engagement.
 
 
 
 

 
Explanation:
Explanation of the Streamlit Code
This code implements a Streamlit-based web application called PRAJNA - The Career Guidance Bot. It integrates OpenAI's GPT model and Pinecone vector database to provide intelligent and context-aware career guidance. Below is a detailed breakdown of each section of the code:
________________________________________
1. Importing Required Libraries
•	streamlit: Used to create the user interface for the chatbot application.
•	openai: Allows interaction with OpenAI's API for generating embeddings and GPT responses.
•	pinecone: Facilitates storing and retrieving embeddings using a vector database.
________________________________________
2. OpenAI and Pinecone Initialization
•	OpenAI API Key:
o	The openai.api_key is set to authenticate with OpenAI's API for generating embeddings and responses.
•	Pinecone Initialization:
o	The Pinecone client is initialized using an API key.
o	The application checks if the index (career-guidance) exists in Pinecone. If it doesn’t, it creates the index with the appropriate dimension size (1536) and metric (cosine) for embeddings.
________________________________________
3. Connecting to the Pinecone Index
•	A connection to the Pinecone index is established using its name and host URL.
•	This index stores embeddings and metadata for efficient semantic search.
________________________________________
4. Streamlit Application Setup
•	App Title and Welcome Message:
o	The title is set to "PRAJNA - The Career Guidance Bot" and includes a welcome message.
________________________________________
5. Chat History Maintenance
•	Session State for Chat History:
o	st.session_state.messages is used to store the chat history, ensuring the conversation persists across user interactions.
•	Trim Chat History:
o	A function trim_chat_history keeps the chat history limited to the last three user-bot pairs (six messages total). This prevents the session from becoming too long or memory-intensive.
________________________________________
6. Displaying Chat History
•	The chat history is displayed in the app with labels for the user (*User:*) and the bot (*Bot:*).
•	This creates a conversational format for users to review previous messages.
________________________________________
7. User Input
•	Text Input:
o	A text input box allows users to type their queries.
•	Send Button:
o	When the "Send" button is clicked, the user query is processed.
________________________________________
8. Processing the User Query
•	Adding Query to History:
o	The user's query is appended to the chat history.
•	Generating Embedding for Query:
o	OpenAI’s text-embedding-ada-002 model is used to convert the user query into an embedding for semantic similarity searches.
•	Querying Pinecone for Context:
o	The embedding is sent to the Pinecone index to retrieve the top 5 most relevant text chunks. These chunks are combined to create a context for GPT.
________________________________________
9. Generating the Bot's Response
•	Sending Query and Context to GPT-4:
o	OpenAI’s ChatCompletion.create API is called to generate a response from GPT-4. The following inputs are used:
	Chat History: Combines the previous conversation with the new query and context.
	System Role: Sets the system’s role as a helpful career guidance assistant.
	Query and Context: The user query and the retrieved Pinecone context are passed as inputs.
•	Extracting the Response:
o	The response text is extracted and trimmed.
________________________________________
10. Updating and Displaying the Response
•	Updating Chat History:
o	The bot's response is appended to the chat history for display.
•	Trimming Chat History:
o	The trim_chat_history function ensures only the last three user-bot pairs are retained.
•	Displaying the Response:
o	The bot's response is displayed in the app under the label *Bot:*.
________________________________________
11. Error Handling
•	If the user clicks "Send" without entering a query, a warning message prompts them to enter text.
________________________________________
Key Features
1.	Conversation History:
o	The chat history is maintained across user interactions, enhancing the conversational experience.
2.	Dynamic Response Generation:
o	The bot dynamically generates personalized and context-aware responses based on Pinecone's context retrieval and OpenAI’s GPT-4.
3.	Efficient History Management:
o	By trimming the chat history, the app ensures efficiency without losing recent context.
________________________________________
User Workflow
1.	Enter a Query:
o	The user types their question in the input box and clicks "Send."
2.	Get a Response:
o	The bot retrieves relevant context, processes the query, and generates a detailed response.
3.	Review Chat History:
o	Users can review past interactions and engage in a seamless conversation.
This code provides a robust implementation of a career guidance chatbot, integrating powerful AI tools with an intuitive user interface.
3.Actual Chat snippet:
 

Conclusion:
The PRAJNA Career Guidance Bot successfully demonstrates the integration of state-of-the-art technologies, such as OpenAI's GPT-4 and Pinecone's vector database, to create an intelligent and interactive chatbot for personalized career advice. This project showcases the following:
1.	Robust Semantic Search:
o	By leveraging Pinecone for storing and retrieving embeddings, the bot delivers highly relevant context for user queries, enhancing response accuracy and relevance.
2.	Dynamic and Context-Aware Responses:
o	OpenAI's GPT-4 ensures the bot provides insightful and human-like responses, tailored to the user’s specific career-related concerns.
3.	Streamlined User Experience:
o	The use of Streamlit for the frontend ensures a smooth and interactive interface, making the application user-friendly and accessible.
4.	Modular and Scalable Architecture:
o	The modular structure of the project, encompassing data preprocessing, embedding generation, and chatbot development, allows for easy scalability and customization for other domains.
5.	Real-World Impact:
o	PRAJNA serves as a valuable tool for individuals seeking career guidance, offering recommendations, tips, and insights into various industries and roles.
Learnings and Future Enhancements
•	Key Learnings:
o	Integration of LLMs with vector databases provides a powerful framework for creating domain-specific intelligent applications.
o	Handling large datasets and managing conversation history are crucial for building scalable chatbots.
•	Future Enhancements:
o	Personalized Suggestions:
	Incorporating user-specific preferences and past interactions for tailored recommendations.
o	Multimodal Capabilities:
	Enhancing the bot to support multimedia inputs (e.g., resumes, job descriptions) for more personalized advice.
o	Cloud Deployment:
	Hosting the application on a cloud platform for broader accessibility and scalability.
Final Note
This project exemplifies the practical application of generative AI in solving real-world problems. It provides a strong foundation for future explorations into intelligent systems, setting the stage for innovative solutions in various domains. By integrating cutting-edge technologies, PRAJNA empowers users with actionable career insights, making it a noteworthy addition to the growing field of AI-driven applications.

References:
1.	OpenAI GPT-4
o	Official Website: https://openai.com
o	Documentation: https://platform.openai.com/docs
o	Usage in Chat Completion: Leveraged GPT-4 for generating intelligent, human-like responses to user queries.
2.	Pinecone Vector Database
o	Official Website: https://www.pinecone.io
o	Documentation: https://docs.pinecone.io
o	Purpose: Used for efficient semantic search and retrieval of relevant information from indexed embeddings.
3.	Streamlit
o	Official Website: https://streamlit.io
o	Documentation: https://docs.streamlit.io
o	Usage: Built the user-friendly frontend interface for interactive chatbot conversations.
4.	LangChain Framework
o	Official Website: https://www.langchain.com
o	GitHub Repository: https://github.com/hwchase17/langchain
o	Purpose: Used for text splitting and preprocessing to prepare data for embedding generation.
5.	Hugging Face Sentence Transformers
o	GitHub Repository: https://github.com/UKPLab/sentence-transformers
o	Purpose: Provided the text-embedding-ada-002 model to generate semantic embeddings for queries and data.
6.	Career Guidance Data Sources
o	Data utilized in the project was preprocessed and combined from the provided files Textbook3.txt and career_guidance_text_expanded.txt.
7.	Python Libraries
o	NumPy: Used for handling numerical operations and data manipulation.
o	Pandas: Utilized for preprocessing tabular data.
o	Matplotlib/Seaborn: For visualization (if applicable).
8.	Documentation on Best Practices
o	Design Patterns for AI Applications:
	Source: https://towardsdatascience.com
o	Streamlit Application Development:
	Source: Streamlit Blog
9.	Project-Based References
o	AI-Powered RAG Application:
	Lecture Notes and Class Assignments.
	Project Outline and Guidelines provided by the instructor.
Acknowledgments
•	Course Instructor: For guidance and feedback throughout the development of the project.
•	Team Members: For collaboration on data collection, preprocessing, and testing.
•	Community Contributions: Open-source tools and libraries that made this project possible.

MIT LICENSE:
Copyright (c) 2024 Vinay1289Sai
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHTMIT License
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.








