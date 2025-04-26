#!/bin/bash
set -e

# Run ingest if specified
if [ "$RUN_INGEST" = "true" ]; then
    echo "Running data ingestion..."
    python ingest.py
fi

# Start Streamlit application
echo "Starting Streamlit application..."
exec python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
