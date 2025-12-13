#!/bin/bash
# Cron entry point for running job search
# This script is executed by cron at scheduled times

# Change to app directory
cd /app

# Run the job searcher with output logging
echo "$(date): Starting job search via cron" >> /var/log/cron.log
if python3 job_searcher.py >> /var/log/cron.log 2>&1; then
    echo "$(date): Job search completed successfully" >> /var/log/cron.log
else
    echo "$(date): Job search failed with exit code $?" >> /var/log/cron.log
fi
