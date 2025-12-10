# Find Job

Automated job search system that sends daily email recommendations using ChatGPT.

## Overview

Find Job automates the tedious task of searching for jobs by leveraging your ChatGPT subscription to find and recommend the top 5 jobs matching your criteria. Results are formatted and emailed to you on a configurable schedule, perfect for running on a home server with Docker.

## Features

- 🤖 **AI-Powered Search**: Uses OpenAI's ChatGPT to find relevant job opportunities
- 📧 **Email Delivery**: Formatted HTML emails with job recommendations
- ⏰ **Configurable Schedule**: Run daily, weekly, or on custom schedules
- 🐳 **Docker Ready**: Easy deployment with Docker and docker-compose
- ⚙️ **Flexible Configuration**: Customize search criteria, prompts, and schedules
- 🏠 **Home Server Friendly**: Designed for self-hosted Linux environments

## Quick Start

> 📖 **New to Find Job?** Check out [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide!

### Prerequisites

- Docker and docker-compose installed
- OpenAI API key (ChatGPT subscription)
- SMTP email server access (e.g., Gmail with app password)

### Setup (Easy Mode)

```bash
# 1. Setup config files
make setup

# 2. Edit .env and config.yaml with your details
nano .env
nano config.yaml

# 3. Test your configuration
make test

# 4. Start the scheduler
make start
```

### Setup (Manual)

1. **Clone the repository**
   ```bash
   git clone https://github.com/towenwolf/find-job.git
   cd find-job
   ```

2. **Create configuration files**
   ```bash
   # Copy and edit the configuration file
   cp config.example.yaml config.yaml
   
   # Copy and edit the environment file
   cp .env.example .env
   ```

3. **Configure your settings**

   Edit `config.yaml` to customize your job search prompt:
   ```yaml
   job_search_prompt: |
     Please search for and recommend the top 5 job opportunities for a Software Engineer...
   
   schedule:
     time: "08:00"  # 8 AM
     days:
       - monday
       - tuesday
       - wednesday
       - thursday
       - friday
   ```

   Edit `.env` with your credentials:
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=your-app-password
   RECIPIENT_EMAIL=your-email@gmail.com
   ```

4. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

5. **Check logs**
   ```bash
   docker-compose logs -f
   ```

## Configuration

### Job Search Prompt

The `job_search_prompt` in `config.yaml` is sent to ChatGPT. Customize it to specify:
- Job titles and roles
- Location preferences
- Required skills and technologies
- Experience level
- Company size and industry
- Salary expectations

Example:
```yaml
job_search_prompt: |
  Find the top 5 remote Software Engineer positions with:
  - 5+ years Python experience
  - Docker/Kubernetes knowledge
  - Remote-friendly companies
  - Competitive salary ($150k+)
```

### Schedule Configuration

Configure when the job search runs:

```yaml
schedule:
  time: "08:00"  # 24-hour format
  days:
    - monday
    - wednesday
    - friday
```

### Email Configuration

You can configure email settings in `config.yaml` or use environment variables:

**Option 1: config.yaml**
```yaml
email:
  smtp_server: smtp.gmail.com
  smtp_port: 587
  sender_email: your-email@gmail.com
  recipient_email: your-email@gmail.com
```

**Option 2: Environment Variables** (in `.env`)
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=your-email@gmail.com
```

#### Gmail Setup

To use Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an app password at https://myaccount.google.com/apppasswords
3. Use the app password in `SENDER_PASSWORD`

## Usage

### Docker Compose (Recommended)

```bash
# Start the scheduler
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the scheduler
docker-compose down
```

### Run Once (Manual Test)

```bash
# Run a single job search without scheduling
docker-compose run --rm find-job python find_job.py
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run once
python find_job.py

# Run scheduler
python scheduler.py
```

## Project Structure

```
find-job/
├── find_job.py             # Core job search and email logic
├── scheduler.py            # Scheduling system
├── requirements.txt        # Python dependencies
├── config.example.yaml     # Example configuration
├── .env.example           # Example environment variables
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose orchestration
└── README.md             # This file
```

## Troubleshooting

### Email Not Sending

- Check SMTP credentials in `.env`
- For Gmail, ensure you're using an app password, not your regular password
- Check firewall rules allow outbound SMTP connections

### OpenAI API Errors

- Verify your API key is correct in `.env`
- Check your OpenAI account has available credits
- Ensure the model name is correct (e.g., `gpt-4` or `gpt-3.5-turbo`)

### Scheduler Not Running

- Check Docker container is running: `docker ps`
- View logs: `docker-compose logs -f`
- Verify timezone is set correctly: `TZ=America/New_York` in `.env`

## Customization

### Change OpenAI Model

Edit `config.yaml`:
```yaml
openai_model: gpt-3.5-turbo  # Cheaper alternative to gpt-4
max_tokens: 2000
```

### Custom Email Template

Modify the `format_email()` method in `find_job.py` to customize the HTML template.

### Add More Features

The codebase is designed to be extensible. Key areas:
- `find_job.py`: Core logic for job search and email
- `scheduler.py`: Scheduling and automation
- `config.yaml`: User configuration

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use and modify as needed.

## Support

For issues or questions, please open an issue on GitHub.