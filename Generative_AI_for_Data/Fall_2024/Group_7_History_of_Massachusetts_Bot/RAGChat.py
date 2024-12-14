import os
import pickle
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
import streamlit as st

class RAGChat:
    """
    A class that implements a Retrieval-Augmented Generation (RAG) chat system.
    It uses markdown documents as the knowledge base, a vector store for similarity-based retrieval, 
    and OpenAI's GPT-3.5-turbo for generating concise, factual answers.
    """

    def __init__(self, markdown_directory='./'):  # Default directory for markdown files
        """
        Initializes the RAGChat system and sets up the RAG pipeline.
        """
        # Load OpenAI API key from Streamlit secrets
        os.environ["OPENAI_API_KEY"] = st.secrets["api"]
        
        # Set the directory for markdown files and vector store
        self.markdown_directory = markdown_directory
        self.vectorstore_path = os.path.join(self.markdown_directory, "vectorstore.pkl")
        
        # Setup the RAG system (loading documents, creating vector store, etc.)
        self.setup_rag_system()

    def load_documents(self):
        """
        Loads markdown documents from the specified directory and prepares them for processing.
        """
        docs = []
        for filename in os.listdir(self.markdown_directory):
            if filename.endswith('.md'):  # Only process markdown files
                filepath = os.path.join(self.markdown_directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                # Wrap each document with metadata for source tracking
                docs.append(Document(page_content=text, metadata={"source": filepath}))
        return docs

    def setup_rag_system(self):
        """
        Sets up the RAG system:
        - Loads or creates the vector store
        - Configures embeddings for document vectors
        - Establishes the retriever and compression mechanism
        - Defines the question-answering chain
        """
        # Check if the vector store already exists
        if os.path.exists(self.vectorstore_path):
            # Load pre-existing vector store
            with open(self.vectorstore_path, "rb") as f:
                self.vectorstore = pickle.load(f)
        else:
            # Load and process documents into smaller chunks
            docs = self.load_documents()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
            split_docs = text_splitter.split_documents(docs)

            # Initialize embeddings using HuggingFace's model
            embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},  # Set to CPU (adjustable for GPUs)
                encode_kwargs={'normalize_embeddings': True}  # Normalize for better similarity matching
            )

            # Create a FAISS vector store for similarity search
            self.vectorstore = FAISS.from_documents(split_docs, embeddings)

            # Save the vector store for future use
            with open(self.vectorstore_path, "wb") as f:
                pickle.dump(self.vectorstore, f)

        # Set up the retriever to search the vector store
        retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        # Set up a language model and document compressor
        llm = ChatOpenAI(model="gpt-3.5-turbo")  # Use OpenAI GPT-3.5-turbo
        compressor = LLMChainExtractor.from_llm(llm)  # Compressor extracts relevant context
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )

        # Define a system prompt for question answering
        system_prompt = """You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, output NA. Keep the answer very concise with as few words as possible.

        {context}"""

        # Create a prompt template for the system
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # Create a chain for combining retrieved documents into an answer
        question_answer_chain = create_stuff_documents_chain(llm, prompt)

        # Set up the full RAG chain with retrieval and answering components
        self.rag_chain = create_retrieval_chain(compression_retriever, question_answer_chain)

    def get_answer(self, question):
        """
        Retrieves and generates an answer to the given question using the RAG system.
        
        Parameters:
        - question (str): The user's query

        Returns:
        - str: The generated answer
        """
        # Invoke the RAG chain with the input question
        answer = self.rag_chain.invoke({"input": question})
        return answer['answer']
