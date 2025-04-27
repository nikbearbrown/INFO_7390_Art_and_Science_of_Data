import json
import chromadb
import os
import time
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---- CONFIG ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EVENTS_FILE = "data/events_cleaned.json"
CHROMA_DB_DIR = "data/chroma_db"
COLLECTION_NAME = "events"
BATCH_SIZE = 10  # <--- Number of documents to batch in one call

# ---- INIT ----
openai_client = OpenAI(api_key=OPENAI_API_KEY)

client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# ---- LOAD EVENTS ----
with open(EVENTS_FILE, "r", encoding="utf-8") as f:
    events = json.load(f)

print(f"Loaded {len(events)} events.")

# ---- PREPARE ----
ids = []
documents = []
metadatas = []

for idx, event in enumerate(events):
    title = event.get("title", "No Title")
    about = event.get("about", "No Description")
    date_time = event.get("date_time", "No Date")
    location = event.get("location", "No Location")
    tags = event.get("tags", "")
    event_link = event.get("event_link", "")

    # ENRICH FULL TEXT
    full_text = (
        f"Event Title: {title}. "
        f"Event Date and Time: {date_time}. "
        f"Event Location: {location}. "
        f"Event Tags: {tags}. "
        f"Event Description: {about}."
    )

    ids.append(f"event-{idx}")
    documents.append(full_text)
    metadatas.append({
        "title": title,
        "date_time": date_time,
        "location": location,
        "tags": tags,
        "link": event_link
    })

# ---- EMBEDDING FUNCTION (with batch support) ----
def generate_embeddings(texts, retries=5):
    for attempt in range(retries):
        try:
            response = openai_client.embeddings.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [r.embedding for r in response.data]
        except openai.RateLimitError:
            wait_time = (2 ** attempt) * 0.5
            print(f"Rate limit hit. Waiting {wait_time:.1f} seconds before retrying...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"Error: {e}")
            raise e
    raise Exception("Failed after retries.")

# ---- BATCH PROCESSING ----
print(f"Starting embedding generation with batch size {BATCH_SIZE}...")

for batch_start in range(0, len(documents), BATCH_SIZE):
    batch_end = min(batch_start + BATCH_SIZE, len(documents))
    batch_docs = documents[batch_start:batch_end]
    batch_ids = ids[batch_start:batch_end]
    batch_metas = metadatas[batch_start:batch_end]

    batch_embeddings = generate_embeddings(batch_docs)

    collection.add(
        documents=batch_docs,
        embeddings=batch_embeddings,
        metadatas=batch_metas,
        ids=batch_ids
    )

    print(f"Embedded events {batch_start} to {batch_end} ✅")
    time.sleep(0.5)  # Light sleep between batches (can tune)

print(f"All {len(documents)} events inserted into ChromaDB at '{CHROMA_DB_DIR}' 🚀")
