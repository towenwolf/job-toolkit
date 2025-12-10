#!/bin/bash
# Convenience script to start Find Job

echo "Starting Find Job..."
docker compose up -d

echo ""
echo "Find Job is now running in the background!"
echo ""
echo "Useful commands:"
echo "  View logs:        docker compose logs -f"
echo "  Stop service:     docker compose down"
echo "  Test once:        docker compose run --rm find-job python find_job.py"
echo ""
