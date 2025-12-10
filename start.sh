#!/bin/bash
# Convenience script to start Job Toolkit

echo "Starting Job Toolkit..."
docker compose up -d

echo ""
echo "Job Toolkit is now running in the background!"
echo ""
echo "Useful commands:"
echo "  View logs:        docker compose logs -f"
echo "  Stop service:     docker compose down"
echo "  Test once:        docker compose run --rm job-toolkit python job_toolkit.py"
echo ""
