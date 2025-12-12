#!/bin/bash
# Run job search once for testing purposes

echo "Running job search (one-time execution)..."
docker compose run --rm job-searcher python job_searcher.py
