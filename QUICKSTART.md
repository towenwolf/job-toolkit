# Quick Start Guide

Get your Find Job running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key (from https://platform.openai.com/api-keys)
- Email account with SMTP access (Gmail recommended)

## Setup Steps

### 1. Get Your API Key

Visit https://platform.openai.com/api-keys and create a new API key.

### 2. Configure Email (Gmail Example)

For Gmail:
1. Enable 2-factor authentication
2. Generate an app password at https://myaccount.google.com/apppasswords
3. Use this app password (not your regular password)

### 3. Create Configuration Files

```bash
# Copy example files
cp config.example.yaml config.yaml
cp .env.example .env
```

### 4. Edit .env File

```bash
# Edit with your favorite editor
nano .env
```

Update these values:
```
OPENAI_API_KEY=sk-your-actual-key-here
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

### 5. Customize Your Job Search

Edit `config.yaml` and update the job search prompt with your preferences:

```yaml
job_search_prompt: |
  Find the top 5 job opportunities for [YOUR ROLE] with:
  - Location: [YOUR LOCATION]
  - Experience Level: [YOUR LEVEL]
  - Tech Stack: [YOUR SKILLS]
  - Industry: [YOUR INDUSTRY]
```

### 6. Test It

Run a one-time test:
```bash
docker compose run --rm find-job python find_job.py
```

Check your email!

### 7. Start the Scheduler

```bash
docker compose up -d
```

View logs:
```bash
docker compose logs -f
```

## Common Issues

### "Authentication failed" error
- For Gmail, make sure you're using an app password, not your regular password
- Check that 2FA is enabled on your Google account

### "No valid days configured" error
- Check `config.yaml` has valid day names: monday, tuesday, etc.
- Days are case-insensitive

### Email not arriving
- Check spam folder
- Verify sender and recipient email addresses
- Check logs: `docker compose logs -f`

## Next Steps

- Adjust the schedule in `config.yaml`
- Refine your job search prompt
- Try different OpenAI models (gpt-4 vs gpt-3.5-turbo)
- Monitor logs to ensure it's running: `docker compose logs -f`

## Support

For issues, check the main README.md or open an issue on GitHub.
