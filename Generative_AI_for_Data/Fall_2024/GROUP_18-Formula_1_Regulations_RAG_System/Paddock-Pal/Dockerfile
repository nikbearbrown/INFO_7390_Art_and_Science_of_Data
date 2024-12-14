# Use an official Python base image
FROM python:3.12-slim

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow \
    AIRFLOW__CORE__EXECUTOR=LocalExecutor \
    AIRFLOW__CORE__LOAD_EXAMPLES=False

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Apache Airflow
RUN poetry install --no-dev

# Create the Airflow home directory
RUN mkdir -p $AIRFLOW_HOME
WORKDIR $AIRFLOW_HOME

# Copy Airflow configuration (optional, if you have a custom airflow.cfg)
# COPY airflow.cfg $AIRFLOW_HOME/

# Expose the port for the Airflow webserver
EXPOSE 8080

# Set up the entrypoint script
ENTRYPOINT ["sh", "-c"]
CMD ["airflow db init && airflow webserver -p 8080"]