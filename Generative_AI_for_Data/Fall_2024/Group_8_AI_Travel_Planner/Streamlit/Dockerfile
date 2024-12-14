FROM python:3.10-slim
 
WORKDIR /app
 
# Install any system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/*
 
# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy in application code
COPY . .
 
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]