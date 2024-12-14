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
COPY  . /app
COPY . .
COPY ./.env ./.env

# Expose the default Streamlit port
EXPOSE 8000

# Run the Streamlit app using Poetry
CMD ["uvicorn", "main_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]