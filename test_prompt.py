#!/usr/bin/env python3
"""
Test script to validate and refine the job search prompt
Tests the search_jobs function from JobSearcher class without sending emails
"""
import json
from datetime import datetime
from job_searcher import JobSearcher


def main():
    print("="*80)
    print("Testing Job Search Prompt")
    print("="*80)
    
    # Initialize JobSearcher (loads config and env automatically)
    try:
        job_searcher = JobSearcher()
        config = job_searcher.config
    except Exception as e:
        print(f"\n✗ ERROR: Failed to initialize JobSearcher: {e}")
        return 1
    
    # Display configuration
    model = config.get('openai_model', 'gpt-4')
    max_tokens = config.get('max_completion_tokens', 2000)
    prompt = config.get('job_search_prompt', '')
    
    print("\nOpenAI Configuration:")
    print(f"  Model: {model}")
    print(f"  Max Tokens: {max_tokens}")
    print(f"\nJob Search Prompt:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    # Call search_jobs function
    print("\n" + "="*80)
    print("Calling search_jobs function...")
    print("="*80)
    
    try:
        start_time = datetime.now()
        
        # Call the search_jobs function
        job_results = job_searcher.search_jobs()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n✓ SUCCESS! search_jobs completed in {duration:.2f} seconds")
        
        print("\n" + "="*80)
        print("Job Search Results:")
        print("="*80)
        print(job_results)
        print("\n" + "="*80)
        
        # Analysis and recommendations
        print("\nPrompt Analysis:")
        print("="*80)
        
        result_length = len(job_results)
        word_count = len(job_results.split())
        line_count = len(job_results.split('\n'))
        
        print(f"  Result Length: {result_length} characters")
        print(f"  Word Count: {word_count} words")
        print(f"  Line Count: {line_count} lines")
        
        # Check if it's valid JSON
        is_json = False
        parsed_json = None
        try:
            parsed_json = json.loads(job_results)
            is_json = True
            print("\n  ✓ Response is valid JSON")
            if 'jobs' in parsed_json:
                job_count = len(parsed_json.get('jobs', []))
                print(f"  ✓ Found {job_count} jobs in JSON response")
        except json.JSONDecodeError:
            print("\n  ℹ Response is not valid JSON (plain text format)")
        
        # Quality checks
        print("\n  Quality Checks:")
        if word_count < 50:
            print("    ⚠ Response seems too short - consider refining the prompt")
        elif word_count > 1000:
            print("    ℹ Response is quite long - consider being more specific in prompt")
        else:
            print("    ✓ Response length looks reasonable")
        
        # Check for common job listing elements
        has_company = any(word in job_results.lower() for word in ['company', 'employer', 'organization'])
        has_location = any(word in job_results.lower() for word in ['location', 'remote', 'office', 'city'])
        has_requirements = any(word in job_results.lower() for word in ['requirements', 'skills', 'experience', 'qualifications'])
        
        print(f"    {'✓' if has_company else '✗'} Contains company information")
        print(f"    {'✓' if has_location else '✗'} Contains location information")
        print(f"    {'✓' if has_requirements else '✗'} Contains requirements/skills")
        
        # Save results to prompt_results.json
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "duration_seconds": duration,
            "prompt": prompt,
            "is_json_format": is_json,
            "job_results": parsed_json if is_json else job_results,
            "statistics": {
                "result_length_chars": result_length,
                "word_count": word_count,
                "line_count": line_count
            },
            "quality_checks": {
                "has_company_info": has_company,
                "has_location_info": has_location,
                "has_requirements": has_requirements
            }
        }
        
        with open('prompt_results.json', 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print("\n✓ Results saved to prompt_results.json")
        
        print("\n" + "="*80)
        print("Prompt Testing Complete!")
        print("="*80)
        print("\nTo refine the prompt:")
        print("  1. Edit the 'job_search_prompt' section in config.yaml")
        print("  2. Run this test again: python3 test_prompt.py")
        print("  3. Iterate until results meet your expectations")
        print("\n" + "="*80)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: API call failed")
        print(f"Error details: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
