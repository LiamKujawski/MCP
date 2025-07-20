.PHONY: install test lint format clean run docker-build docker-run

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/
	mypy src/

format:
	black src/ tests/
	ruff check src/ tests/ --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .ruff_cache

run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t chatgpt-agent-sonnet:latest .

docker-run:
	docker run -p 8000:8000 chatgpt-agent-sonnet:latest

all: format lint test 