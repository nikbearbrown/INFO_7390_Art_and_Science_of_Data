import os
import streamlit as st
from pinecone import Pinecone
import requests
import json

import base64


# Configure page
st.set_page_config(page_title="MediQBot", page_icon="🏥", layout="wide")

# Initialize Pinecone
@st.cache_resource
def init_pinecone():
    """Initialize Pinecone client"""
    # Use Streamlit secrets instead of environment variables for deployment
    api_key = st.secrets["PINECONE_API_KEY"]
    pc = Pinecone(api_key=api_key)
    return pc

# Get embeddings from OpenAI
def get_embedding(text):
    """Get embedding for query text"""
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    
    payload = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers=headers,
        json=payload
    )
    
    return response.json()["data"][0]["embedding"]

# Groq API call
def call_groq(prompt, system_message=None, model="llama3-70b-8192"):
    """Call Groq API with a prompt"""
    groq_api_key = st.secrets["GROQ_API_KEY"]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_api_key}"
    }
    
    messages = []
    
    # Add system message if provided
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # Add user message
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "messages": messages,
        "model": model,
        "temperature": 0.2,
        "max_tokens": 4096
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    return response.json()["choices"][0]["message"]["content"]

# Retrieve documents from Pinecone
def retrieve_documents(query, top_k=5):
    """Retrieve documents from Pinecone index based on query"""
    pc = init_pinecone()
    index = pc.Index("mediqbot-index")
    
    # Get embedding for query
    query_embedding = get_embedding(query)
    
    # Search Pinecone (no filter)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    return results

# Extract context from search results
def extract_context(results):
    """Extract text and format context from search results"""
    context_chunks = []
    sources = []
    
    for match in results.get('matches', []):
        # Skip low-relevance matches (adjust threshold as needed)
        if match['score'] < 0.6:
            continue
            
        metadata = match['metadata']
        
        # Get text chunk
        chunk_text = metadata.get('chunk_text', '')
        if chunk_text:
            context_chunks.append(chunk_text)
        
        # Create source information
        source_info = {
            'score': match['score'],
            'content_type': metadata.get('content_type', 'unknown'),
            'title': metadata.get('title', 'Unknown Title')
        }
        
        # Add source-specific information
        if metadata.get('content_type') == 'youtube_video':
            source_info['channel'] = metadata.get('channel', 'Unknown Channel')
            source_info['url'] = metadata.get('url', '')
        else:
            source_info['authors'] = metadata.get('authors', 'Unknown Authors')
            source_info['journal'] = metadata.get('journal', '')
            source_info['article_url'] = metadata.get('article_url', '')
        
        sources.append(source_info)
    
    return context_chunks, sources

# Check if query is medical-related
def is_medical_query(query):
    """Check if the query is related to medical topics in our database"""
    medical_keywords = [
        'diabetes', 'cancer', 'cardiovascular', 'heart', 'disease', 'infection', 
        'mental health', 'depression', 'anxiety', 'treatment', 'symptoms', 
        'medication', 'therapy', 'diagnosis', 'prognosis', 'health', 'medical',
        'medicine', 'doctor', 'hospital', 'patient', 'blood', 'immune', 
        'surgery', 'drugs', 'prescription', 'condition', 'illness'
    ]
    
    query_lower = query.lower()
    
    # Check if query contains medical keywords
    return any(keyword in query_lower for keyword in medical_keywords)

# RAG function to query with context
def query_rag(question):
    """Run RAG pipeline: retrieve -> generate -> respond"""
    # Step 1: Retrieve relevant documents
    results = retrieve_documents(question, top_k=5)
    
    # Step 2: Extract and format context
    context_chunks, sources = extract_context(results)
    
    if not context_chunks:
        return "I couldn't find any relevant information to answer your question in my knowledge base.", []
    
    # Format context for prompt
    context_text = "\n\n".join(context_chunks)
    
    # Step 3: Create prompt with context
    system_message = """You are MediQBot, a helpful medical assistant that provides accurate information based on scientific articles and medical videos.
Your answers are based on a medical knowledge base of articles and video transcripts about diabetes, cancer, cardiovascular disease, infectious disease, and mental health.
Always cite your sources when providing information. Be concise but informative in your responses."""
    
    prompt = f"""Please answer the following medical question based on the provided context. Include citations to your sources.
If the context doesn't contain enough information to answer confidently, acknowledge the limitations.

QUESTION: {question}

CONTEXT:
{context_text}

Please provide a comprehensive answer with citations to specific sources.
"""
    
    # Step 4: Generate response with Groq
    response = call_groq(prompt, system_message)
    
    return response, sources

# Function to download response as a text file
def get_text_download_link(text, filename="mediqbot_response.txt", link_text="Download Response as Text"):
    """Generate a link to download text as a file"""
    text_bytes = text.encode()
    b64 = base64.b64encode(text_bytes).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# Streamlit UI
def main():
    # Title and intro
    st.title("🏥 MediQBot: Medical Query Assistant")
    st.write("Ask questions about diabetes, cancer, cardiovascular disease, infectious disease, and mental health.")
    
    # Disclaimer
    st.info("⚠️ **Disclaimer**: MediQBot provides information based on medical articles and videos, but does not provide medical advice. Always consult healthcare professionals for diagnosis and treatment.")
    
    # Input for user question
    user_question = st.text_input("Enter your medical question:", placeholder="e.g., What are the latest treatments for diabetes?")
    
    # Add a button for the query
    if st.button("Ask MediQBot") and user_question:
        with st.spinner("Searching medical knowledge base and generating response..."):
            # Query the RAG system
            response, sources = query_rag(user_question)
            
            # Display the response
            st.markdown("### Answer")
            st.markdown(response)
            
            # Display sources
            if sources:
                st.markdown("### Sources")
                for i, source in enumerate(sources):
                    source_type = "📄 Article" if source.get('content_type') == 'article' else "🎬 Video"
                    with st.expander(f"{source_type}: {source.get('title', 'Unknown Title')}"):
                        # Display score
                        st.write(f"**Relevance Score:** {source.get('score', 0):.4f}")
                        
                        # Display type-specific information
                        if source.get('content_type') == 'youtube_video':
                            st.write(f"**Channel:** {source.get('channel', 'Unknown')}")
                            video_url = source.get('url', '')
                            if video_url:
                                st.write(f"**URL:** {video_url}")
                                # Try to embed video if URL is available
                                try:
                                    st.video(video_url)
                                except:
                                    st.write("Video preview not available")
                        else:
                            st.write(f"**Authors:** {source.get('authors', 'Unknown')}")
                            st.write(f"**Journal:** {source.get('journal', 'Unknown')}")
                            article_url = source.get('article_url', '')
                            if article_url:
                                st.write(f"**URL:** {article_url}")
            else:
                st.info("No specific sources found for this response.")
            
            # Create a downloadable text file with the response
            if response:
                download_text = f"Question: {user_question}\n\nAnswer: {response}\n\nSources:\n"
                for i, source in enumerate(sources):
                    download_text += f"{i+1}. {source.get('title', 'Unknown Title')}\n"
                    if source.get('content_type') == 'youtube_video':
                        download_text += f"   Channel: {source.get('channel', 'Unknown')}\n"
                        if source.get('url'):
                            download_text += f"   URL: {source.get('url')}\n"
                    else:
                        download_text += f"   Authors: {source.get('authors', 'Unknown')}\n"
                        download_text += f"   Journal: {source.get('journal', 'Unknown')}\n"
                    download_text += "\n"
                
                st.markdown(get_text_download_link(download_text), unsafe_allow_html=True)

if __name__ == "__main__":
    main()