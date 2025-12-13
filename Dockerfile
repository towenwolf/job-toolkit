FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install cron and other dependencies
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY job_searcher.py .
COPY cron_entry.sh .
COPY setup_cron.py .

# Copy config if exists (will be mounted as volume in production)
COPY config.example.yaml .

# Create .env file placeholder
RUN touch .env

# Make scripts executable
RUN chmod +x /app/cron_entry.sh

# Create log file for cron
RUN touch /var/log/cron.log

# Set timezone (default to UTC, can be overridden)
ENV TZ=UTC

# Copy startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Run cron in foreground
ENTRYPOINT ["/docker-entrypoint.sh"]
