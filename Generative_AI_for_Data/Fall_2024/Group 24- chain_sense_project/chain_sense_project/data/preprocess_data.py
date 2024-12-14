import os
import json
import re

INPUT_PATH = os.path.join("data", "scraped_articles.json")
OUTPUT_PATH = os.path.join("data", "processed_documents.json")

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text: str, chunk_size=1500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def preprocess_scraped_data():
    # Load scraped articles
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    processed_docs = []
    for idx, art in enumerate(articles):
        cleaned = clean_text(art['text'])
        chunks = chunk_text(cleaned)
        for cid, chunk in enumerate(chunks):
            doc = {
                "id": f"{idx}_{cid}",
                "text": chunk,
                "metadata": {
                    "source": art['url'],
                    "title": art['title']
                }
            }
            processed_docs.append(doc)

    # Save processed documents
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(processed_docs, f, ensure_ascii=False, indent=2)

    print(f"Preprocessing complete. {len(processed_docs)} documents saved to {OUTPUT_PATH}.")

if __name__ == "__main__":
    preprocess_scraped_data()
