.PHONY: help setup start stop logs test restart clean

help:
	@echo "Job Searcher - Available Commands"
	@echo ""
	@echo "  make setup     - Create config files from examples"
	@echo "  make start     - Start the job searcher scheduler"
	@echo "  make stop      - Stop the job searcher"
	@echo "  make logs      - View logs"
	@echo "  make test      - Run a one-time job search"
	@echo "  make restart   - Restart the service"
	@echo "  make clean     - Remove Docker containers and images"
	@echo ""

setup:
	@if [ ! -f config.yaml ]; then \
		cp config.example.yaml config.yaml; \
		echo "✓ Created config.yaml - please edit it with your preferences"; \
	else \
		echo "⚠ config.yaml already exists, skipping"; \
	fi
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ Created .env - please edit it with your credentials"; \
	else \
		echo "⚠ .env already exists, skipping"; \
	fi
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit .env with your API keys and credentials"
	@echo "  2. Edit config.yaml with your job search preferences"
	@echo "  3. Run 'make test' to test your configuration"
	@echo "  4. Run 'make start' to start the scheduler"

start:
	docker compose up -d
	@echo "✓ Job Searcher started"
	@echo "  View logs: make logs"

stop:
	docker compose down
	@echo "✓ Job Searcher stopped"

logs:
	docker compose logs -f

test:
	docker compose run --rm job-searcher python job_searcher.py

restart:
	docker compose restart
	@echo "✓ Job Searcher restarted"

clean:
	docker compose down -v
	docker rmi job-toolkit-job-searcher 2>/dev/null || true
	@echo "✓ Cleaned up Docker containers and images"
