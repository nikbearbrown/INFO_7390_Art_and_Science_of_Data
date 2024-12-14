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
 
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]