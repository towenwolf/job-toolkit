# Testing Guide for Job Searcher

This document describes how to test the two core components of the Job Searcher application.

## Test Overview

The testing process validates two main components:

1. **test_prompt.py** - Tests the OpenAI API integration and receives results as JSON
2. **test_email_send.py** - Tests formatting and sending the JSON results as an email

## Prerequisites

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration

#### Create .env file with your credentials:

```bash
cp .env.example .env
```

Then edit `.env` and add:
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `APP_PASSWORD` - Your email app password (required for email test)

#### Create config.yaml:

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` and configure:
- `job_search_prompt` - Customize your job search criteria
- `openai_model` - Model to use (e.g., gpt-4, gpt-4o)
- `email` section - SMTP server, port, sender, and recipient emails

## Running Tests

### Test 1: OpenAI API Integration (Prompt → JSON)

Run the prompt test to search for jobs and receive JSON results:

```bash
python test_prompt.py
```

**What this test does:**
- Loads configuration from `config.yaml` and `.env`
- Initializes the `JobSearcher` class
- Calls `search_jobs()` function with your custom prompt
- Requests JSON formatted output from OpenAI
- Validates and parses the JSON response
- Saves results to `prompt_results.json`

**Expected Output:**
```
================================================================================
Testing Job Search Prompt
================================================================================

OpenAI Configuration:
  Model: gpt-4
  Max Tokens: 2000

Job Search Prompt:
--------------------------------------------------------------------------------
[Your custom prompt from config.yaml]
--------------------------------------------------------------------------------

================================================================================
Calling search_jobs function...
================================================================================

✓ SUCCESS! search_jobs completed in X.XX seconds

================================================================================
Job Search Results:
================================================================================
[JSON formatted job results]
================================================================================

Prompt Analysis:
================================================================================
  Result Length: XXXX characters
  Word Count: XXX words
  Line Count: XX lines

  ✓ Response is valid JSON
  ✓ Found X jobs in JSON response

  Quality Checks:
    ✓ Contains company information
    ✓ Contains location information
    ✓ Contains requirements/skills

✓ Results saved to prompt_results.json
```

**Output File:** `prompt_results.json` contains:
- Timestamp and model information
- Original prompt
- Job results (parsed JSON or raw text)
- Statistics and quality checks

### Test 2: Email Formatting and Sending (JSON → Email)

Run the email test to format and send the JSON results:

```bash
python test_email_send.py
```

**What this test does:**
- Loads `prompt_results.json` from Test 1
- Initializes the `JobSearcher` class
- Calls `format_email()` to convert JSON to formatted HTML
- Calls `send_email()` to send the formatted email
- Delivers email to your inbox

**Expected Output:**
```
================================================================================
Testing format_email and send_email from JobSearcher
================================================================================

1. Loading prompt_results.json...
   ✓ Successfully loaded prompt_results.json

2. Initializing JobSearcher...
   ✓ JobSearcher initialized

3. Formatting job results using format_email()...
   ✓ Email formatted successfully

4. Sending email...
================================================================================
Email sent successfully to your-email@example.com

✓ SUCCESS! Email sent successfully

Check your inbox for the formatted job results!

================================================================================
Email Test Complete!
================================================================================
```

**Email Content:** If results are in JSON format, you'll receive a beautifully formatted email with:
- Header with date
- Job cards for each opportunity showing:
  - 🏢 Company name
  - 📍 Location
  - 📋 Requirements list
  - ✨ Why it's a good fit
  - 🔗 Application URL (if available)
- Footer with automation notice

## Complete Test Workflow

To test the entire system end-to-end:

```bash
# Step 1: Test OpenAI API and get JSON results
python test_prompt.py

# Step 2: Test formatting and sending the results as email
python test_email_send.py
```

## Troubleshooting

### Test 1 Issues (test_prompt.py)

**Missing API Key:**
```
✗ ERROR: OPENAI_API_KEY not found in .env
```
→ Ensure you've created `.env` and added your `OPENAI_API_KEY`

**Config not found:**
```
✗ ERROR: Failed to initialize JobSearcher: Configuration file not found
```
→ Copy `config.example.yaml` to `config.yaml`

### Test 2 Issues (test_email_send.py)

**Missing prompt_results.json:**
```
✗ ERROR: prompt_results.json not found
```
→ Run `python test_prompt.py` first to generate the results file

**Email sending failed:**
```
✗ ERROR: Failed to send email
```
→ Check your email configuration in `config.yaml` and `APP_PASSWORD` in `.env`

## Notes

- **API Costs:** Test 1 makes actual OpenAI API calls and will consume credits
- **Email Delivery:** Test 2 sends real emails to the configured recipient
- **JSON Format:** The system automatically detects JSON format and creates formatted job cards
- **Fallback:** If JSON parsing fails, results are displayed as formatted text
- The `send_email` test uses mocking and does NOT send actual emails or require SMTP credentials
- Tests are designed to be informative with detailed output for debugging
- The config loading test uses `config.example.yaml` and doesn't require credentials
