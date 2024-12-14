FROM apache/airflow:2.10.2

USER root

# Install system dependencies including NTP
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    ntp \
    ntpdate \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directory for Chrome
RUN mkdir -p /opt/chrome && \
    chmod -R 777 /opt/chrome

# Add time synchronization script
COPY sync_time.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/sync_time.sh

USER airflow

# Install Python packages
RUN pip install --no-cache-dir \
    pandas \
    selenium \
    boto3 \
    requests \
    PyMuPDF \
    pillow \
    beautifulsoup4 \
    webdriver_manager \
    snowflake-connector-python \
    snowflake-sqlalchemy \
    cryptography \
    ntplib

# Set environment variables
ENV PYTHONPATH=/opt/airflow/dags \
    DISPLAY=:99 \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_BINARY_PATH=/usr/bin/chromium \
    AWS_DEFAULT_REGION=us-east-1

# Start Xvfb
RUN Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &

WORKDIR /opt/airflow