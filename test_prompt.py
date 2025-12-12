#!/usr/bin/env python3
"""
Test script to validate and refine the job search prompt
Tests the OpenAI API response without sending emails
"""
import os
import yaml
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


def main():
    print("="*80)
    print("Testing Job Search Prompt")
    print("="*80)
    
    # Load configuration
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("\n✗ ERROR: config.yaml not found")
        return 1
    
    # Get OpenAI configuration
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n✗ ERROR: OPENAI_API_KEY not found in .env")
        return 1
    
    model = config.get('openai_model', 'gpt-4')
    max_tokens = config.get('max_completion_tokens', 2000)
    prompt = config.get('job_search_prompt', '')
    
    if not prompt:
        print("\n✗ ERROR: No job_search_prompt found in config.yaml")
        return 1
    
    # Display configuration
    print("\nOpenAI Configuration:")
    print(f"  Model: {model}")
    print(f"  Max Tokens: {max_tokens}")
    print(f"\nJob Search Prompt:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Make API call with web search enabled
    print("\n" + "="*80)
    print("Calling OpenAI API with web search enabled...")
    print("="*80)
    
    try:
        start_time = datetime.now()
        
        # Use Responses API with web_search tool for real-time job search
        response = client.responses.create(
            model=model,
            tools=[{"type": "web_search"}],
            input=prompt
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Extract response details
        job_results = response.output_text
        
        # Note: Responses API may have different usage structure
        usage = getattr(response, 'usage', None)
        
        print(f"\n✓ SUCCESS! API call completed in {duration:.2f} seconds")
        print("\n" + "="*80)
        print("API Response Statistics:")
        print("="*80)
        print(f"  Response ID: {getattr(response, 'id', 'N/A')}")
        print(f"  Model: {getattr(response, 'model', model)}")
        
        # Check if web search was used
        if hasattr(response, 'tool_calls') or 'search' in str(response).lower():
            print(f"  ✓ Web search tool was used for real-time results")
        
        # Display token usage if available
        if usage:
            print(f"\n  Token Usage:")
            print(f"    Prompt Tokens: {getattr(usage, 'prompt_tokens', 'N/A')}")
            print(f"    Completion Tokens: {getattr(usage, 'completion_tokens', 'N/A')}")
            print(f"    Total Tokens: {getattr(usage, 'total_tokens', 'N/A')}")
            
            # Calculate approximate cost (rough estimates for gpt-4)
            if 'gpt-4' in model.lower() and hasattr(usage, 'total_tokens'):
                prompt_cost = getattr(usage, 'prompt_tokens', 0) * 0.00003  # $0.03 per 1K tokens
                completion_cost = getattr(usage, 'completion_tokens', 0) * 0.00006  # $0.06 per 1K tokens
                total_cost = prompt_cost + completion_cost
                print(f"    Estimated Cost: ${total_cost:.4f}")
        
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
        
        # Check if response was truncated (Responses API structure)
        finish_reason = getattr(response, 'finish_reason', None)
        if finish_reason == 'length':
            print("\n  ⚠ WARNING: Response was truncated due to max_tokens limit")
            print("  Consider increasing max_completion_tokens in config.yaml")
        elif finish_reason == 'stop' or finish_reason is None:
            print("\n  ✓ Response completed naturally (not truncated)")
        
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
        
        # Save results to JSON file
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "model": getattr(response, 'model', model),
            "response_id": getattr(response, 'id', 'N/A'),
            "duration_seconds": duration,
            "prompt": prompt,
            "job_results": job_results,
            "statistics": {
                "result_length_chars": result_length,
                "word_count": word_count,
                "line_count": line_count,
                "finish_reason": finish_reason
            },
            "usage": {
                "prompt_tokens": getattr(usage, 'prompt_tokens', 'N/A') if usage else 'N/A',
                "completion_tokens": getattr(usage, 'completion_tokens', 'N/A') if usage else 'N/A',
                "total_tokens": getattr(usage, 'total_tokens', 'N/A') if usage else 'N/A'
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
