import os
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data if not present
# Run this once, can comment out after first run:
nltk.download('punkt')

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_TEXT_DIR = os.path.join(BASE_DIR, "data", "text")
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

CHUNK_SIZE = 500  # characters per chunk

def clean_text(text):
    # Remove extra whitespace
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def chunk_text(text, chunk_size=CHUNK_SIZE):
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Split into sentences
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence = sentence.strip()
        if current_length + len(sentence) > chunk_size:
            # If adding this sentence exceeds chunk_size, start a new chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence)
        else:
            current_chunk.append(sentence)
            current_length += len(sentence)
    # Add last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks

if __name__ == "__main__":
    # Ensure processed directory exists
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

    docs = []
    # Loop through all text files in data/text
    for filename in os.listdir(DATA_TEXT_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_TEXT_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                cleaned = clean_text(raw_text)
                text_chunks = chunk_text(cleaned)
                for chunk in text_chunks:
                    docs.append(chunk)
    
    # Save processed chunks into a single file or multiple files
    processed_file_path = os.path.join(DATA_PROCESSED_DIR, "processed_docs.txt")
    with open(processed_file_path, 'w', encoding='utf-8') as out_f:
        for doc_chunk in docs:
            out_f.write(doc_chunk + "\n\n")  # separate chunks by a blank line

    print(f"Preprocessing complete. Total chunks: {len(docs)}")
    print(f"Processed data saved to {processed_file_path}")




