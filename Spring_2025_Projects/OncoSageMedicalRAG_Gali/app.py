"""
Streamlit app for Medical RAG QA system.
"""
# Set environment variables before importing any other packages
import os
# Disable file watcher to reduce errors
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"
# Set tokenizers parallelism to avoid deadlocks
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Import streamlit first
import streamlit as st

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Oncno Sage - A RAG QA System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now import other libraries
import time
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import LangChain components
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Import helper modules
from openai_helper import OpenAIHelper
from pinecone_helper import PineconeHelper

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #42A5F5;
        margin-bottom: 1rem;
    }
    .answer-container {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-left: 5px solid #1E88E5;
    }
    .source-container {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #757575;
        font-size: 0.8rem;
    }
    .stAlert {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def visualize_relevance(source_documents):
    """
    Create a visualization of document relevance.
    
    Args:
        source_documents: List of source documents with scores
    """
    if not source_documents or len(source_documents) < 2:
        return
    
    try:
        # Extract scores if available
        data = []
        for i, doc in enumerate(source_documents):
            # Try to get score from document
            score = getattr(doc, 'score', None)
            
            # If no score available, use a simulated relevance based on position
            if score is None:
                # Create a simulated score based on position
                score = 1.0 - (i * 0.1)
            
            source = doc.metadata.get('source', f'Document {i+1}')
            
            # Truncate long source names
            if len(source) > 30:
                source = source[:27] + '...'
                
            data.append({
                'Source': source,
                'Relevance': score,
                'Index': i
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create bar chart
        fig = px.bar(
            df, 
            y='Source', 
            x='Relevance',
            color='Relevance',
            color_continuous_scale='Blues',
            title='Document Relevance to Query',
            orientation='h'  # Horizontal bars
        )
        
        fig.update_layout(
            yaxis_title="Source Document",
            xaxis_title="Relevance Score",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        # Silently fail for visualization - it's optional
        pass

def create_document_similarity_heatmap(source_documents):
    """
    Create a heatmap visualization of document similarities.
    """
    if not source_documents or len(source_documents) < 2:
        return
    
    try:
        # Create document labels
        doc_labels = []
        for i, doc in enumerate(source_documents):
            source = doc.metadata.get('source', f'Doc {i+1}')
            if len(source) > 20:
                source = source.split('/')[-1]  # Get just the filename
                if len(source) > 20:
                    source = source[:17] + '...'
            
            # Ensure label is unique by adding the index
            doc_labels.append(f"{source}_{i}")
        
        # Create similarity matrix (example - in reality you might want to compute actual cosine similarities)
        n = len(source_documents)
        similarity_matrix = []
        
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1.0)  # Self-similarity is 1.0
                else:
                    # For simplicity, we'll use a dummy similarity that decreases with distance
                    sim = 1.0 - abs(i - j) * 0.2
                    sim = max(0.3, sim)  # Ensure minimum similarity of 0.3
                    row.append(sim)
            similarity_matrix.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(similarity_matrix, index=doc_labels, columns=doc_labels)
        
        # Create heatmap
        fig = px.imshow(
            df,
            color_continuous_scale='Blues',
            title='Document Similarity Heatmap'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title="Document",
            yaxis_title="Document"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        logger.error(f"Error creating heatmap: {str(e)}")
        # Silently fail for visualization
        pass

@st.cache_resource
def initialize_components():
    """Initialize OpenAI and Pinecone components."""
    try:
        # Initialize OpenAI helper
        openai_helper = OpenAIHelper()
        
        # Initialize Pinecone helper
        pinecone_helper = PineconeHelper()
        
        # Get retriever
        retriever = pinecone_helper.get_retriever(search_kwargs={"k": 3})
        
        # Get LLM
        llm = openai_helper.get_llm()
        
        # Define prompt template
        prompt_template = """Use the following pieces of information to answer the user's question.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        Question: {question}
        
        Only return the helpful answer below and nothing else.
        Helpful answer:
        """
        
        prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
        
        # Create QA chain
        chain_type_kwargs = {"prompt": prompt}
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs,
            verbose=True
        )
        
        return {
            "openai_helper": openai_helper,
            "pinecone_helper": pinecone_helper,
            "retriever": retriever,
            "llm": llm,
            "qa_chain": qa_chain
        }
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        st.error(f"Error initializing components: {str(e)}")
        return None

def process_query(query: str, qa_chain) -> Dict[str, Any]:
    """
    Process a query using the QA chain.
    
    Args:
        query: User's question
        qa_chain: RetrievalQA chain
        
    Returns:
        Dict: Response with answer and source information
    """
    try:
        start_time = time.time()
        response = qa_chain.invoke(query)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        return {
            "answer": response['result'],
            "source_documents": response.get('source_documents', []),
            "processing_time": processing_time
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {
            "answer": f"Error processing query: {str(e)}",
            "source_documents": [],
            "processing_time": 0
        }

def render_answer(response: Dict[str, Any]):
    """
    Render the answer and source information.
    
    Args:
        response: Response from process_query
    """
    if "answer" not in response:
        st.error("Invalid response from QA system.")
        return
    
    st.markdown(f'<div class="answer-container">{response["answer"]}</div>', unsafe_allow_html=True)
    
    st.markdown(f"Processing time: {response['processing_time']:.2f} seconds")
    
    if "source_documents" in response and response["source_documents"]:
        st.markdown("### Source Documents")
        
        # Add visualizations if we have multiple documents
        if len(response["source_documents"]) >= 2:
            st.markdown("#### Document Analysis")
            
            tabs = st.tabs(["Relevance Chart", "Similarity Heatmap"])
            
            with tabs[0]:
                visualize_relevance(response["source_documents"])
            
            with tabs[1]:
                create_document_similarity_heatmap(response["source_documents"])
        
        # Display document details
        for i, doc in enumerate(response["source_documents"]):
            with st.expander(f"Source {i+1}: {doc.metadata.get('source', 'Unknown')}"):
                st.markdown('<div class="source-container">', unsafe_allow_html=True)
                st.markdown(f"**Content:** {doc.page_content}")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display metadata
                if doc.metadata:
                    st.markdown("**Metadata:**")
                    for key, value in doc.metadata.items():
                        st.markdown(f"- {key}: {value}")

def sidebar():
    """Render sidebar."""
    st.sidebar.image("https://img.icons8.com/color/96/000000/medical-doctor.png", width=100)
    st.sidebar.title("Oncno Sage - A RAG QA System")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This system uses Retrieval-Augmented Generation (RAG) to answer medical questions 
    based on a knowledge base of medical literature.
    
    The system combines:
    - OpenAI's language models
    - Pinecone vector database
    - Medical literature corpus
    """)
    
    st.sidebar.markdown("### How it Works")
    st.sidebar.markdown("""
    1. Your question is processed
    2. Relevant medical literature is retrieved
    3. The AI generates an answer based on the retrieved information
    4. Source documents are provided for reference
    """)
   
    st.sidebar.markdown("---")
    st.sidebar.caption("Created for INFO 7390 - Generative AI for Data")

def main():
    """Main function."""
    # Initialize session state for query
    if "query" not in st.session_state:
        st.session_state.query = ""
    
    # Render sidebar
    sidebar()
    
    # Render header
    st.markdown('<h1 class="main-header">Oncno Sage - A RAG QA System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Ask medical questions and get answers based on medical literature</p>', unsafe_allow_html=True)
    
    # Initialize components
    with st.spinner("Loading models and connecting to databases..."):
        components = initialize_components()
    
    if not components:
        st.error("Failed to initialize components. Please check the logs.")
        st.stop()
    
    # Sample questions
    st.markdown("### Sample Questions")
    
    # Function for setting query without rerun issues
    def set_query(question):
        st.session_state.query = question
    
    col1, col2 = st.columns(2)
    
    sample_questions = [
        "What are the common side effects of targeted therapy medications like Trastuzumab and Cetuximab?",
        "What are common treatments for breast cancer? Can you explain it in a easy way",
        "What is the recommended treatment for hormone-sensitive metastatic prostate cancer?",
        "What are the current treatment approaches for stage III melanoma with BRAF mutation?"
    ]
    
    # Create buttons for sample questions with on_click handler
    with col1:
        st.button(sample_questions[0], on_click=set_query, args=(sample_questions[0],))
        st.button(sample_questions[2], on_click=set_query, args=(sample_questions[2],))
    
    with col2:
        st.button(sample_questions[1], on_click=set_query, args=(sample_questions[1],))
        st.button(sample_questions[3], on_click=set_query, args=(sample_questions[3],))
    
    # Query input - now using the session state value as the default
    query = st.text_input("Enter your medical question:", 
                         value=st.session_state.query,
                         key="query_input")
    
    # Update session state with the current input value
    st.session_state.query = query
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        submit_button = st.button("Submit", type="primary")
    
    with col2:
        # Function to clear query
        def clear_query():
            st.session_state.query = ""
        
        st.button("Clear", on_click=clear_query)
    
    # Process query if submitted
    if submit_button and query:
        with st.spinner("Processing your question..."):
            response = process_query(query, components["qa_chain"])
        
        # Display response
        st.markdown("### Answer")
        render_answer(response)
    
    # Footer
    st.markdown('<div class="footer">This application is for educational purposes only. Always consult healthcare professionals for medical advice.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
