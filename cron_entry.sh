#!/bin/bash
# Cron entry point for running job search
# This script is executed by cron at scheduled times

set -e

# Change to app directory
cd /app

# Run the job searcher with output logging
echo "$(date): Starting job search via cron" >> /var/log/cron.log
python3 job_searcher.py >> /var/log/cron.log 2>&1
echo "$(date): Job search completed" >> /var/log/cron.log
