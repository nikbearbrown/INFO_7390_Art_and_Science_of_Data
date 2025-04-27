# Use an official Python runtime as a parent image
FROM python:3.12.7

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set the working directory in the container to /app
WORKDIR /app

# Copy the Streamlit_app directory and Poetry files from the root context
COPY ./Streamlit_App /app
COPY ./poetry.lock /app
COPY ./pyproject.toml /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --no-cache

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run Streamlit when the container launches
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
