# Testing Guide for Job Searcher

This document describes how to run the tests for the Job Searcher application.

## Test Overview

The test suite includes:

1. **test_search_jobs** - Tests the OpenAI API integration and prints detailed JSON response
2. **test_send_email** - Tests the email sending functionality with a plain test email
3. **test_load_config** - Tests configuration file loading

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
- `OPENAI_API_KEY` - Your OpenAI API key (required for search_jobs test)
- `SMTP_SERVER` - Your SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (e.g., 587)
- `SENDER_EMAIL` - Email address to send from
- `SENDER_PASSWORD` - Email password or app-specific password
- `RECIPIENT_EMAIL` - Email address to receive test emails

#### Create config.yaml:

```bash
cp config.example.yaml config.yaml
```

You can customize the job search prompt in `config.yaml` if desired.

## Running Tests

### Run All Tests

```bash
pytest test_job_searcher.py -v -s
```

The `-v` flag provides verbose output, and `-s` allows print statements to be displayed.

### Run Specific Tests

#### Test OpenAI API Integration (search_jobs):

```bash
pytest test_job_searcher.py::TestJobSearcher::test_search_jobs -v -s
```

This test will:
- Call the OpenAI API with the configured prompt
- Print the full JSON response including:
  - Response ID and metadata
  - Model used
  - Token usage statistics
  - Complete message content
- Validate that the response is valid

#### Test Email Sending:

```bash
pytest test_job_searcher.py::TestJobSearcher::test_send_email -v -s
```

This test will:
- Send a plain test email to the configured recipient
- Print the email configuration being used
- Confirm successful delivery (check your inbox!)

**Note:** This test will be skipped if SMTP credentials are not configured.

#### Test Configuration Loading:

```bash
pytest test_job_searcher.py::test_load_config -v -s
```

This test validates that the configuration file can be loaded and contains required fields.

## Test Output

### search_jobs Test Output

The test will print detailed information including:

```
OPENAI RESPONSE OBJECT DETAILS
- Response ID: chatcmpl-xxxxx
- Model: gpt-4
- Created: 2024-xx-xx xx:xx:xx
- Usage Statistics (tokens used)

FULL JSON RESPONSE
- Complete JSON representation of the API response

MESSAGE CONTENT
- The actual job recommendations from the API
```

### send_email Test Output

The test will print:

```
EMAIL CONFIGURATION
- SMTP Server and Port
- Sender and Recipient addresses

Email sending status and confirmation
```

## Troubleshooting

### Missing API Key Error

If you see: `Error: Missing email configuration` or OpenAI API errors, ensure:
1. You've created the `.env` file
2. You've added your `OPENAI_API_KEY` to `.env`
3. You've added SMTP credentials to `.env`

### Email Test Skipped

If the email test is skipped, it means SMTP configuration is missing. Add the required environment variables to `.env`:
- `SMTP_SERVER`
- `SMTP_PORT`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `RECIPIENT_EMAIL`

### Gmail Users

If using Gmail, you need to:
1. Enable 2-factor authentication on your Google account
2. Generate an "App Password" (not your regular password)
3. Use the App Password for `SENDER_PASSWORD` in `.env`

## Running Tests in Docker

You can also run tests in the Docker environment:

```bash
docker compose run --rm job-searcher pytest test_job_searcher.py -v -s
```

## Notes

- The `search_jobs` test makes actual API calls and will consume OpenAI API credits
- The `send_email` test will send actual emails to the configured recipient
- Tests are designed to be informative with detailed output for debugging
- The config loading test uses `config.example.yaml` and doesn't require credentials
