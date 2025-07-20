.PHONY: help install test lint format clean run docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linters"
	@echo "  format       Format code"
	@echo "  clean        Clean up artifacts"
	@echo "  run          Run the application"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run Docker container"

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/
	mypy src/ --ignore-missing-imports
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov .pytest_cache .ruff_cache .mypy_cache

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t sigma-builder-o3-opus .

docker-run:
	docker run -p 8000:8000 --rm sigma-builder-o3-opus

# Development helpers
dev-setup:
	python -m venv venv
	@echo "Run: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
	@echo "Then: make install" 