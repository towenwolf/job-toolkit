#!/usr/bin/env python3
"""
Test script for format_email and send_email functions from JobSearcher
Loads prompt_results.json, formats it to human-readable HTML, and sends email
"""
import json
import os
from job_searcher import JobSearcher


def main():
    print("="*80)
    print("Testing format_email and send_email from JobSearcher")
    print("="*80)
    
    # Check if prompt_results.json exists
    if not os.path.exists('prompt_results.json'):
        print("\n✗ ERROR: prompt_results.json not found")
        print("Please run test_prompt.py first to generate prompt_results.json")
        return 1
    
    # Load prompt_results.json
    print("\n1. Loading prompt_results.json...")
    try:
        with open('prompt_results.json', 'r') as f:
            results_data = json.load(f)
        print("   ✓ Successfully loaded prompt_results.json")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to load prompt_results.json: {e}")
        return 1
    
    # Initialize JobSearcher
    print("\n2. Initializing JobSearcher...")
    try:
        job_searcher = JobSearcher()
        print("   ✓ JobSearcher initialized")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to initialize JobSearcher: {e}")
        return 1
    
    # Get job_results from the data (can be JSON or string)
    job_results = results_data.get('job_results')
    if not job_results:
        print("\n✗ ERROR: No job_results found in prompt_results.json")
        return 1
    
    # Format the results using JobSearcher.format_email()
    print("\n3. Formatting job results using format_email()...")
    try:
        formatted_email = job_searcher.format_email(job_results)
        print("   ✓ Email formatted successfully")
    except Exception as e:
        print(f"   ✗ ERROR: Failed to format email: {e}")
        return 1
    
    # Send the email
    print("\n4. Sending email...")
    print("="*80)
    try:
        job_searcher.send_email(formatted_email)
        print("\n✓ SUCCESS! Email sent successfully")
        print("\nCheck your inbox for the formatted job results!")
    except Exception as e:
        print(f"\n✗ ERROR: Failed to send email: {e}")
        return 1
    
    print("\n" + "="*80)
    print("Email Test Complete!")
    print("="*80)
    return 0

if __name__ == "__main__":
    exit(main())
