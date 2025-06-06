FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    dnsutils \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Install subfinder (optional, if used in utils/subfinder.py)
RUN curl -s https://api.github.com/repos/projectdiscovery/subfinder/releases/latest \
    | grep "browser_download_url.*linux_amd64.zip" \
    | cut -d '"' -f 4 \
    | xargs curl -L -o subfinder.zip && \
    unzip subfinder.zip -d /usr/local/bin/ && rm subfinder.zip

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ .

# Set environment variable to make Flask listen on 0.0.0.0
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expose Flask port
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run"]
