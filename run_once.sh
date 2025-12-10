#!/bin/bash
# Run job search once for testing purposes

echo "Running job search (one-time execution)..."
docker compose run --rm find-job python find_job.py
