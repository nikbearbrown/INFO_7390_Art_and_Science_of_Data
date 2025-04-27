# Use an official Python runtime as a parent image
FROM python:3.12.7

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory in the container to /app
WORKDIR /app

# Copy the FastAPI directory and Poetry files from the root context
COPY ./FastAPIs_Services /app
COPY ./poetry.lock /app
COPY ./pyproject.toml /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-cache

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI with Uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
