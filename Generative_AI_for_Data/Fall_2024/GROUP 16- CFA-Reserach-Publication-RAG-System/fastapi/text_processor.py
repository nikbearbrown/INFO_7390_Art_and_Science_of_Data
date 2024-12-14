from typing import List, Dict, Any
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, PodSpec
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from tqdm import tqdm
import time
import json

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        """Initialize the text processor with necessary clients and configurations"""
        # Initialize NVIDIA embeddings client
        self.embeddings_client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        # Initialize Pinecone
        self.pc = Pinecone(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment="gcp-starter"
        )
        
        # Get or create Pinecone index
        self.index_name = "pdf-embeddings"
        self.create_pinecone_index()
        
        # Get Pinecone index
        self.index = self.pc.Index(self.index_name)

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def create_pinecone_index(self) -> None:
        """Create Pinecone index if it doesn't exist"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes().names()
            if self.index_name not in existing_indexes:
                # Create the index for gcp-starter environment
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1024,  # E5 model dimension
                    metric='cosine',
                    spec=PodSpec(
                        environment="gcp-starter",
                        pod_type="starter"
                    )
                )
                logger.info(f"Created new Pinecone index: {self.index_name}")
            else:
                logger.info(f"Using existing Pinecone index: {self.index_name}")
                
        except Exception as e:
            logger.error(f"Error creating/checking Pinecone index: {str(e)}")
            raise

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        try:
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting text: {str(e)}")
            raise

    def create_embedding(self, text: str, input_type: str = 'passage') -> List[float]:
        """Create embedding for a single text chunk"""
        try:
            response = self.embeddings_client.embeddings.create(
                input=[text],
                model="nvidia/nv-embedqa-e5-v5",
                encoding_format="float",
                extra_body={
                    "input_type": input_type,
                    "truncate": "NONE"
                }
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise

    def process_nodes_and_store(self, nodes: List[Dict], pdf_id: str) -> None:
        """Process PDF nodes and store in Pinecone with complete information"""
        try:
            vectors = []
            for node_idx, node in enumerate(nodes):
                # Log the node structure
                logger.info(f"Processing node {node_idx}: {json.dumps(node, indent=2)}")
                
                # Get the content and metadata, with explicit logging
                content = node.get('content', '')
                page_num = node.get('page_num')
                image_path = node.get('image_path')
                
                logger.info(f"Node {node_idx} metadata:")
                logger.info(f"- page_num: {page_num}")
                logger.info(f"- image_path: {image_path}")
                
                # Split content into chunks
                chunks = self.text_splitter.split_text(content)
                logger.info(f"Split into {len(chunks)} chunks")
                
                for chunk_idx, chunk in enumerate(chunks):
                    # Create embedding for the chunk
                    embedding = self.create_embedding(chunk, input_type='passage')
                    
                    # Create structured node information
                    node_info = {
                        "page_num": page_num if page_num is not None else "",
                        "image_path": image_path if image_path is not None else "",
                        "content": chunk
                    }
                    
                    # Log the node_info being stored
                    logger.info(f"Storing node_info for chunk {chunk_idx}: {json.dumps(node_info, indent=2)}")
                    
                    # Convert node info to JSON string
                    node_info_str = json.dumps(node_info)
                    
                    # Prepare metadata
                    metadata = {
                        "pdf_id": pdf_id,
                        "chunk_index": chunk_idx,
                        "node_index": node_idx,
                        "text": node_info_str  # Store structured info as JSON string
                    }
                    
                    # Prepare vector
                    vector_id = f"{pdf_id}_node{node_idx}_chunk{chunk_idx}"
                    vectors.append((vector_id, embedding, metadata))
                    
                    # Process in batches of 50
                    if len(vectors) >= 50:
                        self.index.upsert(vectors=vectors)
                        vectors = []
                        time.sleep(0.5)  # Rate limiting
                
                # Upsert any remaining vectors
                if vectors:
                    self.index.upsert(vectors=vectors)
                
            logger.info(f"Successfully processed and stored nodes for PDF {pdf_id}")
            
        except Exception as e:
            logger.error(f"Error in process_nodes_and_store: {str(e)}")
            logger.error(f"Exception details: {str(e.__dict__)}")
            raise

    def search_similar(self, query: str, top_k: int = 5, filter_condition: dict = None) -> List[Dict]:
        """Search for similar text with optional filtering"""
        try:
            # Create query embedding
            query_embedding = self.create_embedding(query, input_type='query')
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                filter=filter_condition,
                include_metadata=True
            )
            
            # Format results to include structured node information
            formatted_results = []
            for match in results.matches:
                try:
                    # Parse the stored JSON string back into a dictionary
                    node_info = json.loads(match.metadata.get("text", "{}"))
                    
                    formatted_results.append({
                        "score": match.score,
                        "pdf_id": match.metadata.get("pdf_id"),
                        "chunk_index": match.metadata.get("chunk_index"),
                        "page_num": node_info.get("page_num", ""),
                        "image_path": node_info.get("image_path", ""),
                        "content": node_info.get("content", "")
                    })
                except (json.JSONDecodeError, KeyError) as e:
                    # Fallback with empty values for missing fields
                    formatted_results.append({
                        "score": match.score,
                        "pdf_id": match.metadata.get("pdf_id"),
                        "chunk_index": match.metadata.get("chunk_index"),
                        "page_num": "",
                        "image_path": "",
                        "content": match.metadata.get("text", "")
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in search_similar: {str(e)}")
            raise
        
    def generate_answer_from_chunks(self, query: str, chunks: List[Dict], max_tokens: int = 1000) -> str:
        """Generate an answer using the LLM based on retrieved chunks"""
        try:
            # Format the chunks into a single context
            context = "\n\n".join([
                f"Chunk {i+1}:\n{chunk['metadata']['text']}"
                for i, chunk in enumerate(chunks)
            ])
            
            # Create the prompt
            prompt = f"""Please provide a comprehensive answer to the following question using only the provided context. 
            If the answer cannot be fully derived from the context, please say so.

            Question: {query}

            Context:
            {context}

            Please provide a detailed answer and cite specific parts of the context where appropriate."""

            # Generate response using NVIDIA model
            response = self.embeddings_client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct-v0.1",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating answer from chunks: {str(e)}")
            raise

    async def search_and_answer(self, query: str, top_k: int = 5) -> Dict:
        """Search for relevant chunks and generate an answer"""
        try:
            # First, search for relevant chunks
            search_results = self.search_similar(query, top_k)
            
            # Extract chunks from results
            chunks = [
                {
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in search_results.matches
            ]
            
            # Generate answer using chunks
            answer = self.generate_answer_from_chunks(query, chunks)
            
            return {
                "query": query,
                "answer": answer,
                "supporting_chunks": chunks,
                "total_chunks": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error in search and answer: {str(e)}")
            raise

    def save_research_note(self, document_id: str, note_data: Dict) -> str:
        """Save a research note to Pinecone"""
        try:
            # Create a unique ID for the research note
            note_id = f"note_{document_id}_{int(time.time())}"
            
            # Format the note text combining all text blocks
            note_text = "\n\n".join(note_data["text_blocks"])
            
            # Create embedding for the note text
            try:
                note_embedding = self.create_embedding(note_text, input_type='passage')
            except Exception as e:
                logger.error(f"Error creating embedding for note: {str(e)}")
                raise Exception(f"Failed to create embedding: {str(e)}")
            
            # Prepare metadata
            metadata = {
                "pdf_id": document_id,
                "type": "research_note",
                "query": note_data["query"],
                "timestamp": note_data["timestamp"],
                "text": json.dumps({
                    "content": note_text,
                    "image_paths": note_data["image_paths"]
                })
            }
            
            # Store in Pinecone with retry logic
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    self.index.upsert(
                        vectors=[(note_id, note_embedding, metadata)]
                    )
                    logger.info(f"Saved research note {note_id} for document {document_id}")
                    return note_id
                except Exception as e:
                    logger.error(f"Attempt {attempt + 1} to save note failed: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        raise Exception(f"Failed to save note after {max_retries} attempts: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Error saving research note: {str(e)}")
            raise

    def get_research_notes(self, document_id: str) -> List[Dict]:
        """Retrieve all research notes for a document"""
        try:
            # Query Pinecone for research notes
            results = self.index.query(
                vector=[0] * 1024,  # Dummy vector since we're only using filters
                filter={
                    "pdf_id": document_id,
                    "type": "research_note"
                },
                top_k=100,  # Adjust based on expected number of notes
                include_metadata=True
            )
            
            # Format results
            notes = []
            for match in results.matches:
                try:
                    note_content = json.loads(match.metadata.get("text", "{}"))
                    notes.append({
                        "note_id": match.id,
                        "query": match.metadata.get("query"),
                        "timestamp": match.metadata.get("timestamp"),
                        "content": note_content.get("content", ""),
                        "image_paths": note_content.get("image_paths", [])
                    })
                except json.JSONDecodeError:
                    logger.error(f"Error parsing note content for {match.id}")
                    
            return sorted(notes, key=lambda x: x["timestamp"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error retrieving research notes: {str(e)}")
            raise
    
    # Add this method to your TextProcessor class

    def get_research_notes(self, document_id: str) -> List[Dict]:
        """Retrieve all research notes for a document from Pinecone"""
        try:
            # Query Pinecone for research notes using metadata filters
            search_response = self.index.query(
                vector=[0] * 1024,  # Placeholder vector since we're filtering by metadata
                filter={
                    "pdf_id": document_id,
                    "type": "research_note"
                },
                top_k=100,  # Adjust if you need more notes
                include_metadata=True
            )
            
            logger.info(f"Retrieved {len(search_response.matches)} notes for document {document_id}")
            
            # Format the results
            formatted_notes = []
            for match in search_response.matches:
                try:
                    # Parse the stored JSON string from metadata
                    note_info = json.loads(match.metadata.get("text", "{}"))
                    
                    formatted_note = {
                        "note_id": match.id,
                        "query": match.metadata.get("query", ""),
                        "timestamp": match.metadata.get("timestamp", ""),
                        "content": note_info.get("content", ""),
                        "image_paths": note_info.get("image_paths", [])
                    }
                    
                    logger.info(f"Processing note {match.id} with query: {formatted_note['query']}")
                    formatted_notes.append(formatted_note)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing note content for {match.id}: {str(e)}")
                    continue
                
            # Sort notes by timestamp (newest first)
            formatted_notes.sort(
                key=lambda x: x.get("timestamp", ""), 
                reverse=True
            )
            
            return formatted_notes
            
        except Exception as e:
            logger.error(f"Error retrieving research notes: {str(e)}")
            raise

    def search_notes_by_query(self, document_id: str, query: str) -> List[Dict]:
        """Search for research notes that match a specific query"""
        try:
            # Get all notes for the document
            all_notes = self.get_research_notes(document_id)
            logger.info(f"Searching through {len(all_notes)} notes for query match: {query}")
            
            # Find exact matches (case-insensitive)
            user_query = query.lower().strip()
            matching_notes = []
            
            for note in all_notes:
                saved_query = note.get("query", "").lower().strip()
                logger.info(f"Comparing queries - User: '{user_query}' vs Saved: '{saved_query}'")
                
                if user_query == saved_query:
                    logger.info(f"Found matching note with ID: {note.get('note_id')}")
                    matching_notes.append(note)
            
            return matching_notes
            
        except Exception as e:
            logger.error(f"Error searching notes by query: {str(e)}")
            raise
    
    def analyze_content_relevance(self, query: str, content: str) -> tuple[bool, str]:
        """
        Analyze if content is relevant to the query using LLM.
        Returns (is_relevant, processed_content)
        """
        try:
            system_prompt = """
            Analyze if the provided content answers the user's question.
            If relevant, extract and format the relevant portion.
            If not relevant, respond with exactly 'NO_MATCH'.
            
            Response format for relevant content:
            1. Start with clear relevance indicator
            2. Format content with markdown
            3. Highlight key information
            """
            
            user_prompt = f"""
            Question: {query}
            
            Content to analyze:
            {content}
            
            Determine if this content helps answer the question.
            If yes, provide formatted relevant excerpt.
            If no, respond with exactly 'NO_MATCH'.
            """
            
            response = self.embeddings_client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            is_relevant = "NO_MATCH" not in result
            return is_relevant, result if is_relevant else ""
            
        except Exception as e:
            logger.error(f"Error in content relevance analysis: {str(e)}")
            return False, ""

    def create_report_from_chunks(self, query: str, chunks: List[Dict]) -> str:
        """
        Generate a comprehensive report from document chunks
        """
        try:
            # Format chunks for context
            chunks_text = "\n\n".join([
                f"Chunk {i+1}:\nPage {chunk.get('page_num', 'N/A')}:\n{chunk['content']}"
                for i, chunk in enumerate(chunks)
            ])
            
            system_prompt = """
            Create a comprehensive report from the provided content chunks.
            
            Requirements:
            1. Use clear markdown formatting
            2. Include section headers
            3. Cite specific pages when referencing content
            4. Highlight key findings
            5. Include a brief summary
            
            Format:
            # Answer Summary
            [Brief overview]
            
            # Detailed Analysis
            [Main content with citations]
            
            # Key Points
            - [Bullet points of main findings]
            """
            
            user_prompt = f"""
            Question: {query}
            
            Content Chunks:
            {chunks_text}
            
            Generate a comprehensive report addressing the question.
            """
            
            response = self.embeddings_client.chat.completions.create(
                model="mistralai/mixtral-8x7b-instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise

# Export the class
__all__ = ['TextProcessor']