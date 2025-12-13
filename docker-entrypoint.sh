#!/bin/bash
# Docker entrypoint script to setup and start cron

set -e

echo "Setting up Job Searcher with cron..."

# Generate crontab from config.yaml
echo "Generating crontab from config.yaml..."
python3 /app/setup_cron.py > /etc/cron.d/job-searcher

# Add empty line at end of crontab (required by cron)
echo "" >> /etc/cron.d/job-searcher

# Set proper permissions
chmod 0644 /etc/cron.d/job-searcher

# Apply crontab
crontab /etc/cron.d/job-searcher

# Display the schedule
echo "Job Searcher cron schedule:"
crontab -l

echo ""
echo "Job Searcher is now running with cron scheduler"
echo "Logs will be available at: /var/log/cron.log"
echo ""

# Start cron in background
cron

# Wait a moment for cron to start
sleep 2

# Tail the log file (keeps container running)
tail -f /var/log/cron.log
