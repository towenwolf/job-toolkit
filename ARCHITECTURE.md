# Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Container                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              scheduler.py                           │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │  Schedule Configuration (from config.yaml)   │  │  │
│  │  │  - Time: 08:00                               │  │  │
│  │  │  - Days: Mon-Fri                             │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │                       ↓                             │  │
│  │              Triggers at scheduled time             │  │
│  │                       ↓                             │  │
│  └─────────────────────────────────────────────────────┘  │
│                        ↓                                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              job_toolkit.py                         │  │
│  │                                                     │  │
│  │  1. Search Jobs                                     │  │
│  │     ┌────────────────────────────┐                 │  │
│  │     │ OpenAI API (ChatGPT)       │                 │  │
│  │     │ Model: gpt-4               │                 │  │
│  │     │ Prompt: Custom job search  │                 │  │
│  │     └────────────────────────────┘                 │  │
│  │              ↓                                      │  │
│  │  2. Format Results                                  │  │
│  │     ┌────────────────────────────┐                 │  │
│  │     │ HTML Email Formatter       │                 │  │
│  │     │ - Professional styling     │                 │  │
│  │     │ - Job recommendations      │                 │  │
│  │     └────────────────────────────┘                 │  │
│  │              ↓                                      │  │
│  │  3. Send Email                                      │  │
│  │     ┌────────────────────────────┐                 │  │
│  │     │ SMTP Client                │                 │  │
│  │     │ Server: smtp.gmail.com     │                 │  │
│  │     └────────────────────────────┘                 │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         ↓
                    ┌─────────┐
                    │  Email  │
                    │ Inbox   │
                    └─────────┘
```

## Data Flow

1. **Scheduler Initialization**
   - Loads `config.yaml` for schedule settings
   - Validates configured days
   - Sets up scheduled tasks

2. **Scheduled Execution**
   - Runs at configured time (e.g., 8:00 AM daily)
   - Triggers `job_toolkit.run()`

3. **Job Search**
   - Reads custom prompt from `config.yaml`
   - Sends prompt to OpenAI API with context
   - Receives AI-generated job recommendations

4. **Email Formatting**
   - Takes raw AI response
   - Wraps in HTML template
   - Adds date, styling, and structure

5. **Email Delivery**
   - Connects to SMTP server
   - Authenticates with credentials
   - Sends formatted email to recipient

## Configuration Files

```
config.yaml
├── job_search_prompt    # Custom prompt for ChatGPT
├── openai_model         # Model selection (gpt-4, gpt-3.5-turbo)
├── max_tokens           # Response length limit
├── email                # Optional email settings
│   ├── smtp_server
│   ├── smtp_port
│   ├── sender_email
│   └── recipient_email
└── schedule             # When to run
    ├── time             # Format: "HH:MM"
    └── days             # Array of day names
```

```
.env (secrets)
├── OPENAI_API_KEY       # Required
├── SMTP_SERVER          # Optional (defaults in config)
├── SMTP_PORT            # Optional
├── SENDER_EMAIL         # Required
├── SENDER_PASSWORD      # Required
└── RECIPIENT_EMAIL      # Required
```

## Execution Modes

### Scheduler Mode (Default)
```bash
docker compose up -d
```
- Runs continuously
- Executes on schedule
- Restarts on failure

### One-Shot Mode (Testing)
```bash
docker compose run --rm job-toolkit python job_toolkit.py
```
- Runs once
- Immediate execution
- Useful for testing

## Dependencies

### Python Packages
- `openai>=1.0.0` - OpenAI API client
- `pyyaml>=6.0` - YAML configuration parsing
- `python-dotenv>=1.0.0` - Environment variable management
- `schedule>=1.2.0` - Task scheduling

### External Services
- OpenAI API - Job search intelligence
- SMTP Server - Email delivery (e.g., Gmail)

## Security Considerations

1. **Secrets Management**
   - API keys stored in `.env` (not committed to git)
   - Passwords never in code or config.yaml

2. **Container Security**
   - Read-only config volume mount
   - Non-root user execution
   - Minimal base image (python:3.11-slim)

3. **Network Security**
   - TLS/SSL for SMTP (STARTTLS)
   - HTTPS for OpenAI API
   - No exposed ports

## Customization Points

1. **Job Search Criteria**
   - Edit `config.yaml` → `job_search_prompt`
   - Tailor to your role, location, skills

2. **Schedule**
   - Edit `config.yaml` → `schedule`
   - Change time or days

3. **Email Template**
   - Modify `job_toolkit.py` → `format_email()`
   - Customize HTML/CSS

4. **AI Model**
   - Edit `config.yaml` → `openai_model`
   - Trade cost vs quality (gpt-3.5-turbo vs gpt-4)

## Troubleshooting Flow

```
Email not received?
├── Check logs: docker compose logs -f
├── Verify SMTP credentials in .env
├── Test one-shot: make test
└── Check spam folder

Invalid API key?
├── Verify .env has correct OPENAI_API_KEY
├── Check key at platform.openai.com
└── Ensure account has credits

Scheduler not running?
├── Check container status: docker ps
├── View logs: docker compose logs
├── Verify config.yaml has valid days
└── Check timezone: echo $TZ
```

## Scalability Notes

This is designed for personal use (single user). For scaling:
- Use a job queue (e.g., Celery, RQ)
- Add database for job tracking
- Implement rate limiting
- Add webhook/API interface
- Support multiple users
