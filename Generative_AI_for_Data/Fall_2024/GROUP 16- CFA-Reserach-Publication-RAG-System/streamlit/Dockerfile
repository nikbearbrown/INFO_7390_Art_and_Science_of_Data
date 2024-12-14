# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the application code
COPY . /app
COPY . .
COPY ./.env ./.env

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "index.py", "--server.port=8501", "--server.address=0.0.0.0"]