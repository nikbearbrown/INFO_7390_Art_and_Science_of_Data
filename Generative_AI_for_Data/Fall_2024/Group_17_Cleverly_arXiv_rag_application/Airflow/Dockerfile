# Base Image
FROM python:3.10-slim

# Set environment variables
ENV AIRFLOW_HOME=/usr/local/airflow

# Create airflow user
RUN mkdir -p $AIRFLOW_HOME \
    && useradd -ms /bin/bash airflow \
    && chown -R airflow:airflow $AIRFLOW_HOME

WORKDIR $AIRFLOW_HOME

# Install necessary dependencies, including git and other system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    curl \
    vim \
    libssl-dev \
    libffi-dev \
    python3-distutils \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip, upgrade, and set up Python environment
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install Python packages
COPY requirements.txt /usr/local/airflow/requirements.txt
RUN pip install --no-cache-dir -r /usr/local/airflow/requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port for webserver
EXPOSE 8080

# Ensure airflow user is used for further commands
USER airflow

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
