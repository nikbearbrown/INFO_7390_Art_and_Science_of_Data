FROM apache/airflow:2.10.4

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libu2f-udev \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a requirements.txt file
COPY requirements.txt /tmp/requirements.txt

# Switch to airflow user and install dependencies using Airflow's recommended method
USER airflow
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium

# Download spaCy model
RUN python -m spacy download en_core_web_sm