import os
import requests
from google.cloud import storage
from google.api_core.exceptions import NotFound

# ============ CONFIGURATION ============
BUCKET_NAME   = "cfa-pdfs"
FOLDER_PREFIX = "cfa_pdfs/"   # your “folder” inside the bucket
TXT_FILE      = "cfa.txt"     # must be in same dir or give full path
# =======================================

def download_pdf(url: str) -> bytes:
    """Download PDF from URL; raises on HTTP errors."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.content

def upload_to_gcs(bucket: storage.Bucket, blob_path: str, data: bytes):
    """Upload raw bytes to GCS at the given blob path, unless it already exists."""
    blob = bucket.blob(blob_path)

    # --- check existence ---
    if blob.exists():
        print(f"ℹ️  gs://{bucket.name}/{blob_path} already exists, skipping.")
        return

    # --- otherwise upload ---
    blob.upload_from_string(data, content_type="application/pdf")
    print(f"→ Uploaded gs://{bucket.name}/{blob_path}")

def main():
    # Initialize GCS client and bucket (explicitly set your project to avoid quota warnings)
    client = storage.Client(project="multimodal-rag-457721")
    bucket = client.bucket(BUCKET_NAME)

    # create folder placeholder (only if you want the prefix to show in console)
    placeholder = bucket.blob(f"{FOLDER_PREFIX}__placeholder__")
    if not placeholder.exists():
        placeholder.upload_from_string("", content_type="text/plain")

    # Read and process links
    with open(TXT_FILE, "r") as f:
        for line in f:
            url = line.strip()
            if not url.lower().endswith(".pdf"):
                continue

            filename = os.path.basename(url)
            blob_path = f"{FOLDER_PREFIX}{filename}"

            try:
                pdf_bytes = download_pdf(url)
                upload_to_gcs(bucket, blob_path, pdf_bytes)
            except Exception as e:
                print(f"⚠️ Failed {url}: {e}")

if __name__ == "__main__":
    main()