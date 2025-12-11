FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY job_searcher.py .
COPY scheduler.py .

# Copy config if exists (will be mounted as volume in production)
COPY config.example.yaml .

# Create .env file placeholder
RUN touch .env

# Set timezone (default to UTC, can be overridden)
ENV TZ=UTC

# Run the scheduler by default
CMD ["python", "scheduler.py"]
