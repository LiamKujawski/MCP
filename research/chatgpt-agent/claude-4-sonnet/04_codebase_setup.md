---
topic: "chatgpt-agent"
model: "claude-4-sonnet"
stage: research
version: 1
---

# ChatGPT Agent Codebase Setup - Claude 4 Sonnet Analysis

## Project Structure Overview

### Monorepo Organization
```
chatgpt-agent/
├── services/                 # Core microservices
│   ├── task-orchestrator/   # Central coordination service
│   ├── virtual-computer/    # Containerized execution environment
│   ├── tool-registry/       # Tool management and discovery
│   ├── safety-monitor/      # Real-time safety oversight
│   └── session-manager/     # User session management
├── libs/                    # Shared libraries and utilities
│   ├── common/              # Common utilities and types
│   ├── security/            # Security and authentication
│   ├── monitoring/          # Observability and metrics
│   └── messaging/           # Inter-service communication
├── tools/                   # Agent tools and integrations
│   ├── browser/             # Web browsing capabilities
│   ├── code-interpreter/    # Code execution environment
│   ├── file-system/         # File management operations
│   └── external-apis/       # Third-party API integrations
├── infrastructure/          # Infrastructure as Code
│   ├── kubernetes/          # K8s deployment manifests
│   ├── terraform/           # Cloud infrastructure
│   ├── docker/              # Container definitions
│   └── monitoring/          # Observability stack
├── docs/                    # Documentation
│   ├── architecture/        # System design documentation
│   ├── api/                 # API specifications
│   ├── deployment/          # Deployment guides
│   └── development/         # Development setup
├── tests/                   # Test suites
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   ├── e2e/                 # End-to-end tests
│   └── load/                # Performance tests
└── scripts/                 # Build and deployment scripts
    ├── build/               # Build automation
    ├── deploy/              # Deployment scripts
    └── dev/                 # Development utilities
```

## Development Environment Setup

### Prerequisites Installation Script
```bash
#!/bin/bash
# setup-dev-environment.sh

set -euo pipefail

echo "Setting up ChatGPT Agent development environment..."

# Install required tools
install_prerequisites() {
    echo "Installing prerequisites..."
    
    # Docker and Docker Compose
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
    
    # Kubernetes tools
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    
    # Helm
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    sudo apt-get install helm
    
    # Development tools
    sudo apt-get update
    sudo apt-get install -y \
        git \
        jq \
        curl \
        wget \
        unzip \
        build-essential \
        python3 \
        python3-pip \
        nodejs \
        npm \
        go
    
    # Install language-specific package managers
    pip3 install --upgrade pip poetry
    npm install -g yarn pnpm
    
    echo "Prerequisites installed successfully!"
}

# Setup local development cluster
setup_local_cluster() {
    echo "Setting up local Kubernetes cluster..."
    
    # Install kind (Kubernetes in Docker)
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
    
    # Create development cluster
    kind create cluster --name chatgpt-agent-dev --config=infrastructure/kind/cluster-config.yaml
    
    # Install required operators and tools
    kubectl apply -f infrastructure/kubernetes/operators/
    
    # Setup monitoring stack
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update
    
    helm install prometheus prometheus-community/kube-prometheus-stack \
        --namespace monitoring \
        --create-namespace \
        --values infrastructure/helm/prometheus-values.yaml
    
    echo "Local cluster setup complete!"
}

# Configure development tools
configure_dev_tools() {
    echo "Configuring development tools..."
    
    # Setup pre-commit hooks
    pip3 install pre-commit
    pre-commit install
    
    # Configure IDE settings
    mkdir -p .vscode
    cp .vscode-templates/* .vscode/
    
    # Setup environment variables
    cp .env.example .env.local
    echo "Please edit .env.local with your configuration"
    
    echo "Development tools configured!"
}

# Main execution
main() {
    install_prerequisites
    setup_local_cluster
    configure_dev_tools
    
    echo "Development environment setup complete!"
    echo "Run 'make dev-up' to start local development stack"
}

main "$@"
```

### Development Makefile
```makefile
# Makefile for ChatGPT Agent development

.PHONY: help dev-up dev-down build test lint format security-scan docs

# Default target
help: ## Show this help message
	@echo "ChatGPT Agent Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development environment
dev-up: ## Start local development environment
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Waiting for services to be ready..."
	./scripts/dev/wait-for-services.sh
	@echo "Development environment ready!"
	@echo "API Gateway: http://localhost:8080"
	@echo "Grafana: http://localhost:3000"
	@echo "Jaeger: http://localhost:16686"

dev-down: ## Stop local development environment
	docker-compose -f docker-compose.dev.yml down
	kind delete cluster --name chatgpt-agent-dev

# Build targets
build: ## Build all services
	@echo "Building all services..."
	docker-compose -f docker-compose.build.yml build
	@echo "Build complete!"

build-service: ## Build specific service (usage: make build-service SERVICE=task-orchestrator)
	@if [ -z "$(SERVICE)" ]; then echo "Usage: make build-service SERVICE=<service-name>"; exit 1; fi
	docker build -t chatgpt-agent/$(SERVICE):latest services/$(SERVICE)/

# Testing
test: ## Run all tests
	@echo "Running test suite..."
	./scripts/test/run-all-tests.sh

test-unit: ## Run unit tests
	@echo "Running unit tests..."
	pytest tests/unit/ -v --cov=services/ --cov-report=html

test-integration: ## Run integration tests
	@echo "Running integration tests..."
	pytest tests/integration/ -v --tb=short

test-e2e: ## Run end-to-end tests
	@echo "Running e2e tests..."
	./scripts/test/e2e-tests.sh

test-load: ## Run load tests
	@echo "Running load tests..."
	k6 run tests/load/agent-load-test.js

# Code quality
lint: ## Run linters on all code
	@echo "Running linters..."
	# Python services
	find services/ -name "*.py" | xargs flake8
	find services/ -name "*.py" | xargs black --check
	find services/ -name "*.py" | xargs isort --check-only
	# TypeScript/JavaScript
	find services/ -name "*.ts" -o -name "*.js" | xargs eslint
	# Go services
	find services/ -name "*.go" | xargs golangci-lint run
	# YAML/JSON
	find . -name "*.yaml" -o -name "*.yml" | xargs yamllint
	@echo "Linting complete!"

format: ## Format all code
	@echo "Formatting code..."
	# Python
	find services/ -name "*.py" | xargs black
	find services/ -name "*.py" | xargs isort
	# TypeScript/JavaScript
	find services/ -name "*.ts" -o -name "*.js" | xargs prettier --write
	# Go
	find services/ -name "*.go" | xargs gofmt -w
	@echo "Formatting complete!"

security-scan: ## Run security scans
	@echo "Running security scans..."
	# Container scanning
	trivy image chatgpt-agent/task-orchestrator:latest
	# Dependency scanning
	safety check -r requirements.txt
	# Secret scanning
	truffleHog git file://. --only-verified
	@echo "Security scan complete!"

# Documentation
docs: ## Generate documentation
	@echo "Generating documentation..."
	# API documentation
	swagger-codegen generate -i docs/api/openapi.yaml -l html2 -o docs/api/generated/
	# Architecture documentation
	plantuml -tpng docs/architecture/*.puml
	# Code documentation
	sphinx-build -b html docs/development/ docs/development/_build/
	@echo "Documentation generated!"

docs-serve: ## Serve documentation locally
	cd docs && python3 -m http.server 8000

# Deployment
deploy-local: ## Deploy to local cluster
	@echo "Deploying to local cluster..."
	kubectl apply -k infrastructure/kubernetes/overlays/local/
	@echo "Deployment complete!"

deploy-staging: ## Deploy to staging environment
	@echo "Deploying to staging..."
	kubectl apply -k infrastructure/kubernetes/overlays/staging/
	@echo "Staging deployment complete!"

# Database operations
db-migrate: ## Run database migrations
	@echo "Running database migrations..."
	./scripts/db/migrate.sh

db-seed: ## Seed database with test data
	@echo "Seeding database..."
	./scripts/db/seed-test-data.sh

# Utilities
logs: ## View logs from all services
	docker-compose -f docker-compose.dev.yml logs -f

logs-service: ## View logs from specific service (usage: make logs-service SERVICE=task-orchestrator)
	@if [ -z "$(SERVICE)" ]; then echo "Usage: make logs-service SERVICE=<service-name>"; exit 1; fi
	docker-compose -f docker-compose.dev.yml logs -f $(SERVICE)

shell: ## Open shell in service container (usage: make shell SERVICE=task-orchestrator)
	@if [ -z "$(SERVICE)" ]; then echo "Usage: make shell SERVICE=<service-name>"; exit 1; fi
	docker-compose -f docker-compose.dev.yml exec $(SERVICE) /bin/bash

clean: ## Clean up development artifacts
	@echo "Cleaning up..."
	docker system prune -f
	docker volume prune -f
	kind delete cluster --name chatgpt-agent-dev
	rm -rf .pytest_cache/ __pycache__/ *.egg-info/
	@echo "Cleanup complete!"
```

## Testing Framework Configuration

### Pytest Configuration
```ini
# pytest.ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra
    --strict-markers
    --strict-config
    --cov=services
    --cov-branch
    --cov-report=term-missing:skip-covered
    --cov-report=html:htmlcov
    --cov-report=xml
    --cov-fail-under=80
    --tb=short
    --maxfail=5
python_files = tests/*.py test_*.py *_test.py
python_classes = Test*
python_functions = test_*
testpaths = tests
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    security: Security tests
    performance: Performance tests
    requires_external: Tests requiring external services
filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning
```

### Test Utilities and Fixtures
```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

from services.common.config import Config
from services.common.database import Database
from services.common.messaging import MessageBroker
from tests.factories import TaskFactory, UserFactory, SessionFactory

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def config() -> Config:
    """Test configuration."""
    return Config(
        database_url="sqlite:///:memory:",
        redis_url="redis://localhost:6379/1",
        environment="test",
        debug=True
    )

@pytest.fixture
async def database(config: Config) -> AsyncGenerator[Database, None]:
    """Test database connection."""
    db = Database(config.database_url)
    await db.connect()
    await db.create_tables()
    yield db
    await db.disconnect()

@pytest.fixture
def message_broker() -> MessageBroker:
    """Mock message broker."""
    broker = AsyncMock(spec=MessageBroker)
    return broker

@pytest.fixture
def task_factory() -> TaskFactory:
    """Task factory for creating test tasks."""
    return TaskFactory()

@pytest.fixture
def user_factory() -> UserFactory:
    """User factory for creating test users."""
    return UserFactory()

@pytest.fixture
def session_factory() -> SessionFactory:
    """Session factory for creating test sessions."""
    return SessionFactory()

# Service-specific fixtures
@pytest.fixture
async def task_orchestrator(database, message_broker, config):
    """Task orchestrator service instance."""
    from services.task_orchestrator.app import create_app
    app = create_app(config, database, message_broker)
    yield app
    await app.cleanup()

@pytest.fixture
async def virtual_computer_service(config):
    """Virtual computer service instance."""
    from services.virtual_computer.app import create_app
    app = create_app(config)
    yield app
    await app.cleanup()
```

### End-to-End Test Framework
```python
# tests/e2e/test_agent_workflow.py
import pytest
import asyncio
from typing import Dict, Any

from tests.e2e.client import AgentAPIClient
from tests.e2e.assertions import assert_task_completed, assert_safety_compliance

class TestAgentWorkflow:
    """End-to-end tests for ChatGPT Agent workflows."""
    
    @pytest.fixture
    async def api_client(self) -> AgentAPIClient:
        """API client for testing."""
        client = AgentAPIClient(base_url="http://localhost:8080")
        await client.authenticate()
        yield client
        await client.close()
    
    @pytest.mark.e2e
    async def test_research_workflow(self, api_client: AgentAPIClient):
        """Test complete research workflow."""
        
        # Create research task
        task_request = {
            "type": "research",
            "description": "Research the latest developments in quantum computing",
            "requirements": {
                "sources": ["academic", "news", "industry"],
                "depth": "comprehensive",
                "format": "report"
            }
        }
        
        # Submit task
        task_id = await api_client.create_task(task_request)
        assert task_id is not None
        
        # Monitor execution
        task_status = await api_client.wait_for_completion(
            task_id, 
            timeout=300  # 5 minutes
        )
        
        # Verify completion
        assert_task_completed(task_status)
        assert task_status["result"]["type"] == "research_report"
        assert len(task_status["result"]["sources"]) >= 5
        assert task_status["result"]["word_count"] >= 1000
        
        # Verify safety compliance
        assert_safety_compliance(task_status["audit_log"])
    
    @pytest.mark.e2e
    async def test_code_development_workflow(self, api_client: AgentAPIClient):
        """Test code development workflow."""
        
        task_request = {
            "type": "development",
            "description": "Create a REST API for user management with authentication",
            "requirements": {
                "language": "python",
                "framework": "fastapi",
                "features": ["CRUD operations", "JWT authentication", "input validation"],
                "testing": True,
                "documentation": True
            }
        }
        
        task_id = await api_client.create_task(task_request)
        task_status = await api_client.wait_for_completion(task_id, timeout=600)
        
        # Verify code generation
        assert_task_completed(task_status)
        assert "source_code" in task_status["result"]
        assert "tests" in task_status["result"]
        assert "documentation" in task_status["result"]
        
        # Verify code quality
        code_quality = task_status["result"]["quality_metrics"]
        assert code_quality["test_coverage"] >= 80
        assert code_quality["linting_score"] >= 8.0
        assert len(code_quality["security_issues"]) == 0
    
    @pytest.mark.e2e
    @pytest.mark.slow
    async def test_multi_tool_workflow(self, api_client: AgentAPIClient):
        """Test workflow requiring multiple tools."""
        
        task_request = {
            "type": "analysis",
            "description": "Analyze website performance and create optimization recommendations",
            "requirements": {
                "url": "https://example.com",
                "metrics": ["load_time", "lighthouse_score", "accessibility"],
                "tools": ["browser", "code_interpreter", "file_system"]
            }
        }
        
        task_id = await api_client.create_task(task_request)
        task_status = await api_client.wait_for_completion(task_id, timeout=180)
        
        # Verify multi-tool execution
        assert_task_completed(task_status)
        tools_used = task_status["execution_log"]["tools_used"]
        assert "browser" in tools_used
        assert "code_interpreter" in tools_used
        assert "file_system" in tools_used
        
        # Verify analysis results
        result = task_status["result"]
        assert "performance_metrics" in result
        assert "recommendations" in result
        assert len(result["recommendations"]) >= 3
```

## Pre-commit Hooks Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: check-case-conflict
      - id: check-executables-have-shebangs
      - id: check-shebang-scripts-are-executable

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
        files: ^services/.*\.py$

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        files: ^services/.*\.py$
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        files: ^services/.*\.py$
        args: ["--max-line-length=88", "--extend-ignore=E203,W503"]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        files: ^services/.*\.py$
        additional_dependencies: [types-requests, types-redis]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        files: ^services/.*\.py$
        args: ["-r", "-x", "tests/"]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.43.0
    hooks:
      - id: eslint
        files: \.(js|ts|jsx|tsx)$
        additional_dependencies:
          - eslint@8.43.0
          - "@typescript-eslint/eslint-plugin@5.59.9"
          - "@typescript-eslint/parser@5.59.9"

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0
    hooks:
      - id: prettier
        files: \.(js|ts|jsx|tsx|json|yaml|yml|md)$

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.32.0
    hooks:
      - id: yamllint
        args: [-d, relaxed]

  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint
        files: Dockerfile.*

  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.2
    hooks:
      - id: python-safety-dependencies-check
        files: requirements.*\.txt$

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

## IDE Configuration

### VS Code Settings
```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/node_modules": true,
        "**/.coverage": true,
        "**/htmlcov": true
    },
    "yaml.schemas": {
        "https://raw.githubusercontent.com/instrumenta/kubernetes-json-schema/master/v1.18.0-standalone-strict/all.json": [
            "infrastructure/kubernetes/**/*.yaml",
            "infrastructure/kubernetes/**/*.yml"
        ]
    },
    "go.gopath": "${workspaceFolder}",
    "go.goroot": "/usr/local/go",
    "go.formatTool": "goimports",
    "go.lintTool": "golangci-lint",
    "typescript.preferences.importModuleSpecifier": "relative",
    "eslint.workingDirectories": ["services"],
    "docker.defaultRegistryPath": "chatgpt-agent"
}
```

This comprehensive setup provides a robust foundation for developing, testing, and maintaining the ChatGPT Agent codebase with modern development practices and tools.