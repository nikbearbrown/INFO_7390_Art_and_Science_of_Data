import os
import json
from dotenv import load_dotenv
import chromadb
import openai

# Load environment variables
load_dotenv()

# Constants
CHROMA_PERSIST_DIR = "data/chroma_db"
COLLECTION_NAME = "literature-review-assistant"
DEFAULT_TOP_K = 5

# Check if we have an OpenAI API key for completions
# If not, we'll use a simpler alternative (placeholder)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = False

# Safely try to import OpenAI
try:
    # Try to initialize OpenAI client based on the version installed
    try:
        # First try the newer version style (OpenAI v1.0.0+)
        openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        USE_OPENAI = OPENAI_API_KEY is not None and OPENAI_API_KEY.startswith("sk-")
    except (TypeError, AttributeError):
        # Fall back to older version style
        openai.api_key = OPENAI_API_KEY
        USE_OPENAI = OPENAI_API_KEY is not None and OPENAI_API_KEY.startswith("sk-")
    
    if USE_OPENAI:
        COMPLETION_MODEL = "gpt-3.5-turbo"  # Use a less expensive model as fallback
        print("Using OpenAI for completions")
    else:
        print("OpenAI API key not found or invalid. Will use basic summarization instead.")
except ImportError:
    print("OpenAI library not installed. Will use basic summarization instead.")
    USE_OPENAI = False

class RAGEngine:
    def __init__(self):
        # Initialize ChromaDB client
        try:
            self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
            print(f"Connected to ChromaDB at {CHROMA_PERSIST_DIR}")
            
            # Get the collection
            try:
                self.collection = self.client.get_collection(name=COLLECTION_NAME)
                collection_count = self.collection.count()
                print(f"Found collection '{COLLECTION_NAME}' with {collection_count} documents")
            except Exception as e:
                print(f"Error accessing collection: {e}")
                print("Please run simple_chroma_processor.py first to create the collection")
                self.collection = None
        except Exception as e:
            print(f"Error connecting to ChromaDB: {e}")
            print("Please run simple_chroma_processor.py first to set up ChromaDB")
            self.client = None
            self.collection = None
    
    def retrieve_relevant_papers(self, query, top_k=DEFAULT_TOP_K):
        """Retrieve most relevant papers based on the query"""
        if self.collection is None:
            print("Collection not available. Please run simple_chroma_processor.py first.")
            return []
        
        # Query the collection
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Convert the results to a list of paper objects
            papers = []
            
            if not results['ids'][0]:  # No results found
                return papers
            
            for i in range(len(results['ids'][0])):
                paper_id = results['ids'][0][i]
                document = results['documents'][0][i]
                metadata = results['metadatas'][0][i]
                
                # Calculate a score from the distance (convert distance to similarity)
                # ChromaDB uses cosine distance, so 1 - distance = cosine similarity
                distance = results['distances'][0][i]
                score = 1 - distance  # Convert to similarity score
                
                # Create a paper object
                paper = type('Paper', (), {
                    'id': paper_id,
                    'document': document,
                    'metadata': metadata,
                    'score': score
                })
                
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error retrieving papers: {e}")
            return []
    
    def format_paper_for_context(self, paper):
        """Format a paper for inclusion in LLM context"""
        # Extract title from metadata (if available) or from the document
        title = paper.metadata.get('title', 'Unknown Title')
        
        # Format authors
        authors = paper.metadata.get('authors', 'Unknown Authors')
        
        # Format other metadata
        formatted = f"""
Title: {title}
Authors: {authors}
Date: {paper.metadata.get('date', 'Unknown Date')}
Categories: {paper.metadata.get('categories', 'Unknown Categories')}
Source: {paper.metadata.get('source', 'Unknown Source')}
Abstract: {paper.document.replace('Title: ' + title, '').replace('Abstract: ', '')}
Relevance Score: {paper.score:.4f}
Paper ID: {paper.id}
"""
        return formatted
    
    def generate_response(self, query, papers, response_type="general"):
        """Generate a response based on query and retrieved papers"""
        
        # Format papers for context
        papers_context = "\n\n".join([self.format_paper_for_context(paper) for paper in papers])
        
        # Prepare system message based on response type
        if response_type == "summary":
            system_message = """You are a specialized academic research assistant. Your task is to provide a comprehensive summary of the research papers provided in the context, focusing on their key findings, methodologies, and contributions to the field. Organize the summary by themes or research questions, rather than paper by paper. Highlight agreements, disagreements, and research gaps across the papers."""
        elif response_type == "comparison":
            system_message = """You are a specialized academic research assistant. Your task is to compare and contrast the research papers provided in the context. Focus on their methodologies, findings, strengths, limitations, and how they relate to each other. Identify points of agreement, disagreement, and complementary insights."""
        elif response_type == "future_research":
            system_message = """You are a specialized academic research assistant. Based on the research papers provided in the context, identify promising directions for future research. Focus on research gaps, limitations of current approaches, emerging trends, and potential interdisciplinary connections."""
        else:  # general
            system_message = """You are a specialized academic research assistant. Your task is to help researchers understand the most relevant papers to their query. Based on the papers provided in the context, provide a helpful response that addresses the user's query. Include key insights from the papers, how they relate to the query, and suggestions for further exploration."""
        
        if USE_OPENAI:
            try:
                # Try the newer OpenAI client API style first
                try:
                    # Generate response using OpenAI API (newer style)
                    response = openai_client.chat.completions.create(
                        model=COMPLETION_MODEL,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": f"Query: {query}\n\nRelevant Papers:\n{papers_context}"}
                        ],
                        temperature=0.5,
                        max_tokens=1500
                    )
                    content = response.choices[0].message.content
                except (AttributeError, TypeError):
                    # Fall back to older OpenAI client API style
                    response = openai.ChatCompletion.create(
                        model=COMPLETION_MODEL,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": f"Query: {query}\n\nRelevant Papers:\n{papers_context}"}
                        ],
                        temperature=0.5,
                        max_tokens=1500
                    )
                    content = response.choices[0].message['content']
            except Exception as e:
                print(f"Error using OpenAI API: {e}")
                # Fall back to basic response
                content = self._generate_basic_response(query, papers, response_type)
        else:
            # Basic response generation without OpenAI
            content = self._generate_basic_response(query, papers, response_type)
        
        return {
            "response": content,
            "papers": papers
        }
    
    def _generate_basic_response(self, query, papers, response_type):
        """Generate a basic response without using OpenAI API"""
        
        # Create a simple formatted response
        if len(papers) == 0:
            return f"No relevant papers found for your query: '{query}'"
        
        if response_type == "summary":
            response = f"# Summary of Research Papers Related to: '{query}'\n\n"
            response += "## Key Findings\n\n"
            
            for i, paper in enumerate(papers):
                response += f"### {i+1}. {paper.metadata.get('title', 'Untitled')}\n"
                response += f"**Authors:** {paper.metadata.get('authors', 'Unknown Authors')}\n"
                response += f"**Date:** {paper.metadata.get('date', 'Unknown Date')}\n"
                response += f"**Relevance Score:** {paper.score:.4f}\n"
                
                # Extract abstract
                abstract = paper.document.replace(f"Title: {paper.metadata.get('title', 'Untitled')}", "").replace("Abstract: ", "").strip()
                
                # Extract first two sentences of abstract for a brief summary
                sentences = abstract.split('.')
                brief = '.'.join(sentences[:2]) + '.' if len(sentences) > 1 else abstract
                
                response += f"**Summary:** {brief}\n\n"
        
        elif response_type == "comparison":
            response = f"# Comparison of Research Papers Related to: '{query}'\n\n"
            
            response += "## Papers Overview\n\n"
            for i, paper in enumerate(papers):
                response += f"### {i+1}. {paper.metadata.get('title', 'Untitled')}\n"
                response += f"**Authors:** {paper.metadata.get('authors', 'Unknown Authors')}\n"
                response += f"**Date:** {paper.metadata.get('date', 'Unknown Date')}\n"
                response += f"**Categories:** {paper.metadata.get('categories', 'Unknown Categories')}\n"
                response += f"**Relevance Score:** {paper.score:.4f}\n\n"
            
            response += "\n## Similarities and Differences\n\n"
            response += "The papers above approach the topic from different angles. To understand their relationships in detail, please review the abstracts in the papers section below.\n\n"
        
        elif response_type == "future_research":
            response = f"# Future Research Directions Based on: '{query}'\n\n"
            
            response += "## Potential Research Opportunities\n\n"
            response += "Based on the retrieved papers, there appear to be several promising research directions:\n\n"
            
            # Generate some generic research directions
            response += "1. Expanding the methodologies used in these papers to other domains\n"
            response += "2. Addressing limitations mentioned in these studies\n"
            response += "3. Combining approaches from multiple papers for novel solutions\n"
            response += "4. Exploring interdisciplinary connections\n\n"
            
            response += "To identify specific research gaps, please review the papers in detail below.\n\n"
        
        else:  # general
            response = f"# Research Insights for: '{query}'\n\n"
            
            response += "## Overview\n\n"
            response += f"Found {len(papers)} relevant papers that might address your research question.\n\n"
            
            response += "## Key Papers\n\n"
            for i, paper in enumerate(papers[:3]):  # Just show top 3 for the overview
                response += f"### {i+1}. {paper.metadata.get('title', 'Untitled')}\n"
                response += f"**Authors:** {paper.metadata.get('authors', 'Unknown Authors')}\n"
                response += f"**Date:** {paper.metadata.get('date', 'Unknown Date')}\n"
                response += f"**Relevance Score:** {paper.score:.4f}\n"
                
                # Extract abstract
                abstract = paper.document.replace(f"Title: {paper.metadata.get('title', 'Untitled')}", "").replace("Abstract: ", "").strip()
                
                # Extract first sentence of abstract for a very brief summary
                first_sentence = abstract.split('.')[0] + '.' if '.' in abstract else abstract
                
                response += f"**Preview:** {first_sentence}\n\n"
            
            response += "\nFor more details, please review all the retrieved papers below.\n\n"
        
        response += "\n## Papers\n\n"
        for i, paper in enumerate(papers):
            response += f"### Paper {i+1}: {paper.metadata.get('title', 'Untitled')}\n"
            response += f"**Authors:** {paper.metadata.get('authors', 'Unknown Authors')}\n"
            response += f"**Date:** {paper.metadata.get('date', 'Unknown Date')}\n"
            response += f"**Categories:** {paper.metadata.get('categories', 'Unknown Categories')}\n"
            
            # Extract abstract
            abstract = paper.document.replace(f"Title: {paper.metadata.get('title', 'Untitled')}", "").replace("Abstract: ", "").strip()
            
            response += f"**Abstract:** {abstract}\n\n"
        
        return response

    def process_query(self, query, top_k=DEFAULT_TOP_K, response_type="general"):
        """Process a user query end-to-end"""
        # Retrieve relevant papers
        papers = self.retrieve_relevant_papers(query, top_k)
        
        # Generate response
        result = self.generate_response(query, papers, response_type)
        
        return result