import streamlit as st
import chromadb
import os
import time
import pandas as pd
from datetime import datetime

# Constants
CHROMA_PERSIST_DIR = "data/chroma_db"
COLLECTION_NAME = "literature-review-assistant"

# Set page configuration
st.set_page_config(
    page_title="Literature Review Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS to improve appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        color: #1E88E5 !important;
        margin-bottom: 1rem !important;
    }
    .sub-header {
        font-size: 1.8rem !important;
        color: #424242 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    .paper-title {
        font-size: 1.2rem !important;
        color: #1E88E5 !important;
        font-weight: bold !important;
    }
    .paper-score {
        color: #4CAF50 !important;
        font-weight: bold !important;
    }
    .paper-category {
        background-color: #E3F2FD !important;
        padding: 3px 8px !important;
        border-radius: 15px !important;
        margin-right: 5px !important;
        font-size: 0.85rem !important;
        white-space: nowrap !important;
    }
    .paper-metadata {
        color: #616161 !important;
        font-size: 0.9rem !important;
        margin-bottom: 10px !important;
    }
    .abstract-text {
        background-color: #f8f9fa !important;
        padding: 15px !important;
        border-radius: 5px !important;
        border-left: 3px solid #1E88E5 !important;
        margin-top: 10px !important;
    }
    .results-container {
        margin-top: 30px !important;
    }
    .stAlert {
        padding: 15px !important;
        border-radius: 4px !important;
        margin-bottom: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

def format_categories(categories_str):
    """Format categories as badges"""
    if not categories_str:
        return ""
    
    categories = categories_str.split(", ")
    formatted = ""
    for category in categories:
        formatted += f'<span class="paper-category">{category}</span> '
    return formatted

def display_paper(i, paper_id, document, metadata, score):
    """Display a single paper with enhanced formatting"""
    title = metadata.get('title', 'Unknown Title')
    authors = metadata.get('authors', 'Unknown')
    date = metadata.get('date', 'Unknown')
    categories = metadata.get('categories', '')
    
    with st.expander(f"📄 {i+1}. {title}"):
        # Extract abstract from document
        abstract = document
        if "Title:" in document and "Abstract:" in document:
            abstract = document.split("Abstract:", 1)[1].strip()
            
        # Format categories as badges
        categories_html = format_categories(categories)
        
        # Paper metadata
        st.markdown(f'<div class="paper-metadata">'
                   f'<strong>Authors:</strong> {authors} | '
                   f'<strong>Date:</strong> {date} | '
                   f'<strong>ID:</strong> {paper_id}'
                   f'</div>', unsafe_allow_html=True)
        
        # Categories
        if categories_html:
            st.markdown(f'<div style="margin-bottom:15px;">{categories_html}</div>', unsafe_allow_html=True)
        
        # Relevance score with visual indicator
        col1, col2 = st.columns([1, 9])
        with col1:
            # Calculate a color based on the score
            score_color = f"rgba({int(255*(1-score))}, {int(255*score)}, 0, 0.8)"
            st.markdown(f"""
            <div style="width:50px;height:50px;line-height:50px;border-radius:50%;
                       background-color:{score_color};color:white;text-align:center;
                       font-weight:bold;font-size:0.9rem;">
                {score:.2f}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # Display the abstract with better formatting
            st.markdown(f'<div class="abstract-text">{abstract}</div>', unsafe_allow_html=True)

def main():
    # Sidebar with application information
    with st.sidebar:
        st.markdown("# 📚 Literature Review Assistant")
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application helps researchers explore academic 
        literature using vector search technology.
        
        👉 Enter a research question in the main panel
        👉 Adjust search parameters as needed
        👉 Get relevant papers instantly
        """)
        
        st.markdown("---")
        st.markdown("### Search Tips")
        st.markdown("""
        - Be specific in your query
        - Use key terms and concepts
        - Try different phrasings if needed
        - Adjust the number of results for better coverage
        """)
        
        st.markdown("---")
        st.markdown("### Statistics")
        
        # Connect to ChromaDB to get collection stats
        try:
            client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            collection = client.get_collection(name=COLLECTION_NAME)
            collection_count = collection.count()
            st.success(f"Database Status: Connected")
            st.info(f"Total Papers: {collection_count}")
        except Exception as e:
            st.error("Database Status: Not Connected")
            st.warning("Run data_processor.py first")
    
    # Main content
    st.markdown('<h1 class="main-header">🔍 Research Question Explorer</h1>', unsafe_allow_html=True)
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input("Enter your research question", value="reinforcement learning", 
                            placeholder="e.g., transformer models in natural language processing",
                            help="Enter a research topic or question to find relevant papers")
    
    with col2:
        top_k = st.slider("Number of results", min_value=1, max_value=15, value=5,
                        help="Adjust how many relevant papers to retrieve")
    
    # Create tabs for different search options
    tab1, tab2, tab3 = st.tabs(["📊 General", "🔄 Compare", "🔮 Future Research"])
    
    with tab1:
        search_button_general = st.button("🔍 Search", type="primary", use_container_width=True)
        search_type = "general"
    
    with tab2:
        search_button_compare = st.button("🔄 Compare Papers", type="primary", use_container_width=True)
        search_type = "comparison" if search_button_compare else search_type
    
    with tab3:
        search_button_future = st.button("🔮 Explore Future Directions", type="primary", use_container_width=True)
        search_type = "future_research" if search_button_future else search_type
        
    # Determine if any search button was pressed
    search_activated = search_button_general or search_button_compare or search_button_future
    
    # Execute search when button is pressed
    if search_activated and query:
        search_start_time = time.time()
        
        with st.spinner("Searching for relevant papers..."):
            try:
                # Connect to ChromaDB
                client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
                
                # Get collection
                collection = client.get_collection(name=COLLECTION_NAME)
                
                # Perform query
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                # Display results
                if 'ids' in results and results['ids'] and len(results['ids'][0]) > 0:
                    search_time = time.time() - search_start_time
                    
                    # Results header
                    st.markdown(f'<h2 class="sub-header">📚 Research Results</h2>', unsafe_allow_html=True)
                    st.markdown(f"Found **{len(results['ids'][0])}** relevant papers in {search_time:.2f} seconds")
                    
                    # Create paper objects
                    papers = []
                    for i in range(len(results['ids'][0])):
                        paper_id = results['ids'][0][i]
                        document = results['documents'][0][i]
                        metadata = results['metadatas'][0][i]
                        distance = results['distances'][0][i]
                        score = 1 - distance
                        
                        papers.append({
                            'id': paper_id,
                            'document': document,
                            'metadata': metadata,
                            'score': score
                        })
                    
                    # Display papers in order of relevance
                    for i, paper in enumerate(papers):
                        display_paper(i, paper['id'], paper['document'], paper['metadata'], paper['score'])
                    
                    # Show export options
                    st.markdown("---")
                    export_col1, export_col2 = st.columns(2)
                    
                    with export_col1:
                        if st.button("Export to CSV", use_container_width=True):
                            # Create dataframe for export
                            export_data = []
                            for paper in papers:
                                export_data.append({
                                    'ID': paper['id'],
                                    'Title': paper['metadata'].get('title', 'Unknown'),
                                    'Authors': paper['metadata'].get('authors', 'Unknown'),
                                    'Date': paper['metadata'].get('date', 'Unknown'),
                                    'Categories': paper['metadata'].get('categories', ''),
                                    'Score': paper['score'],
                                    'Abstract': paper['document']
                                })
                            
                            # Create dataframe
                            df = pd.DataFrame(export_data)
                            
                            # Generate CSV download link
                            csv = df.to_csv(index=False)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"research_results_{timestamp}.csv"
                            
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name=filename,
                                mime='text/csv',
                                use_container_width=True
                            )
                    
                    with export_col2:
                        if st.button("Save Search", use_container_width=True):
                            st.session_state["last_query"] = query
                            st.session_state["last_results"] = papers
                            st.success("Search saved! Access it from the 'History' section")
                
                else:
                    st.warning("No results found for your query. Try different keywords or check if your database is set up correctly.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure you've run data_processor.py first to set up the database.")
    
    # Display search history if available
    if hasattr(st.session_state, "last_query") and hasattr(st.session_state, "last_results"):
        st.markdown("---")
        st.markdown('<h2 class="sub-header">📜 Recent Searches</h2>', unsafe_allow_html=True)
        
        st.info(f"Previous search: **{st.session_state.last_query}**")
        
        if st.button("Show previous results"):
            st.markdown(f'<h3 class="sub-header">Results for: {st.session_state.last_query}</h3>', unsafe_allow_html=True)
            
            for i, paper in enumerate(st.session_state.last_results):
                display_paper(i, paper['id'], paper['document'], paper['metadata'], paper['score'])

if __name__ == "__main__":
    main()
