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
- Test the email sending functionality with mocked SMTP connection
- Print the email configuration being used
- Verify that SMTP methods are called correctly (connection, starttls, login, send_message)

**Note:** This test uses mocking and does NOT require real SMTP credentials or send actual emails.

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

SMTP method verification status:
- SMTP connection established
- STARTTLS called
- Login called with correct credentials
- Message sent
```

## Troubleshooting

### Missing API Key Error

If you see OpenAI API errors in `test_search_jobs`, ensure:
1. You've created the `.env` file
2. You've added your `OPENAI_API_KEY` to `.env`

**Note:** The `test_send_email` test uses mocking and does not require SMTP credentials.
The `test_load_config` test does not require any credentials.

## Running Tests in Docker

You can also run tests in the Docker environment:

```bash
docker compose run --rm job-searcher pytest test_job_searcher.py -v -s
```

## Notes

- The `search_jobs` test makes actual API calls and will consume OpenAI API credits
- The `send_email` test uses mocking and does NOT send actual emails or require SMTP credentials
- Tests are designed to be informative with detailed output for debugging
- The config loading test uses `config.example.yaml` and doesn't require credentials
