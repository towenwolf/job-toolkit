#!/bin/bash
# Convenience script to start Job Searcher

echo "Starting Job Searcher..."
docker compose up -d

echo ""
echo "Job Searcher is now running in the background!"
echo ""
echo "Useful commands:"
echo "  View logs:        docker compose logs -f"
echo "  Stop service:     docker compose down"
echo "  Test once:        docker compose run --rm job-searcher python job_searcher.py"
echo ""
