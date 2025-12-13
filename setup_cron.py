#!/usr/bin/env python3
"""
Setup cron schedule from config.yaml
"""
import yaml
import sys


def load_schedule_config():
    """Load schedule configuration from config.yaml"""
    try:
        with open('/app/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            return config.get('schedule', {})
    except FileNotFoundError:
        print("Warning: config.yaml not found, using default schedule")
        return {}


def time_to_cron_time(time_str):
    """Convert HH:MM format to cron hour and minute"""
    try:
        hour, minute = time_str.split(':')
        return int(minute), int(hour)
    except (ValueError, AttributeError):
        print(f"Warning: Invalid time format '{time_str}', using default 08:00")
        return 0, 8


def day_to_cron_day(day):
    """Convert day name to cron day number (0=Sunday, 1=Monday, etc.)"""
    day_mapping = {
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6
    }
    return day_mapping.get(day.lower())


def generate_crontab():
    """Generate crontab entries from config.yaml"""
    schedule_config = load_schedule_config()
    
    # Get schedule time (default: 8:00 AM)
    schedule_time = schedule_config.get('time', '08:00')
    minute, hour = time_to_cron_time(schedule_time)
    
    # Get days to run (default: Monday-Friday)
    days = schedule_config.get('days', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
    
    # Convert days to cron day numbers
    cron_days = []
    for day in days:
        day_num = day_to_cron_day(day)
        if day_num is not None:
            cron_days.append(str(day_num))
        else:
            print(f"Warning: Invalid day '{day}' ignored", file=sys.stderr)
    
    if not cron_days:
        print("Error: No valid days configured for scheduling", file=sys.stderr)
        sys.exit(1)
    
    # Generate cron expression
    # Format: minute hour day month day-of-week
    cron_days_str = ','.join(cron_days)
    cron_line = f"{minute} {hour} * * {cron_days_str} /app/cron_entry.sh"
    
    print(f"# Job Searcher - Scheduled for {schedule_time} on days: {', '.join(days)}")
    print(cron_line)


if __name__ == "__main__":
    generate_crontab()
