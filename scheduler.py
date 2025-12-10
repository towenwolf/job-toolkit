#!/usr/bin/env python3
"""
Scheduler for running job search on a configurable schedule
"""
import schedule
import time
import yaml
from job_toolkit import JobToolkit


def load_schedule_config():
    """Load schedule configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            return config.get('schedule', {})
    except FileNotFoundError:
        print("Warning: config.yaml not found, using default schedule")
        return {}


def run_job_search():
    """Run the job search"""
    try:
        toolkit = JobToolkit()
        toolkit.run()
    except Exception as e:
        print(f"Error running job search: {str(e)}")


def main():
    """Main scheduler loop"""
    schedule_config = load_schedule_config()
    
    # Get schedule time (default: 8:00 AM)
    schedule_time = schedule_config.get('time', '08:00')
    
    # Get days to run (default: Monday-Friday)
    days = schedule_config.get('days', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
    
    print(f"Scheduling job search for {schedule_time} on: {', '.join(days)}")
    
    # Mapping of day names to schedule methods
    day_mapping = {
        'monday': schedule.every().monday,
        'tuesday': schedule.every().tuesday,
        'wednesday': schedule.every().wednesday,
        'thursday': schedule.every().thursday,
        'friday': schedule.every().friday,
        'saturday': schedule.every().saturday,
        'sunday': schedule.every().sunday
    }
    
    # Schedule the job for specified days
    valid_days = []
    for day in days:
        day_lower = day.lower()
        if day_lower in day_mapping:
            day_mapping[day_lower].at(schedule_time).do(run_job_search)
            valid_days.append(day)
        else:
            print(f"Warning: Invalid day '{day}' ignored. Valid days: {', '.join(day_mapping.keys())}")
    
    if not valid_days:
        raise ValueError("No valid days configured for scheduling. Please check config.yaml")
    
    print("Scheduler started. Waiting for scheduled time...")
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
