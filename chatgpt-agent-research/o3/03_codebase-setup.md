# ChatGPT Agent Codebase Setup and Organization

## Repository Structure

### Monorepo Architecture
```
chatgpt-agent/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── deploy-staging.yml
│   │   ├── deploy-production.yml
│   │   ├── security-scan.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
├── services/
│   ├── task-orchestrator/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/
│   │   │   │   │   └── com/openai/agent/orchestrator/
│   │   │   │   │       ├── controller/
│   │   │   │   │       ├── service/
│   │   │   │   │       ├── model/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── Application.java
│   │   │   │   └── resources/
│   │   │   │       ├── application.yml
│   │   │   │       └── logback-spring.xml
│   │   │   └── test/
│   │   ├── Dockerfile
│   │   ├── pom.xml
│   │   └── README.md
│   ├── virtual-computer/
│   │   ├── runtime/
│   │   │   ├── src/
│   │   │   │   ├── container/
│   │   │   │   ├── security/
│   │   │   │   ├── filesystem/
│   │   │   │   └── main.py
│   │   │   ├── requirements.txt
│   │   │   └── Dockerfile
│   │   ├── api/
│   │   │   ├── handlers/
│   │   │   ├── middleware/
│   │   │   ├── models/
│   │   │   └── app.py
│   │   └── tests/
│   ├── tool-integration/
│   │   ├── browser/
│   │   │   ├── src/
│   │   │   │   ├── driver/
│   │   │   │   ├── security/
│   │   │   │   └── index.ts
│   │   │   ├── package.json
│   │   │   ├── tsconfig.json
│   │   │   └── Dockerfile
│   │   ├── code-interpreter/
│   │   │   ├── src/
│   │   │   ├── sandbox/
│   │   │   └── runtime/
│   │   └── filesystem/
│   ├── safety-monitor/
│   │   ├── content-filter/
│   │   ├── action-validator/
│   │   ├── audit-logger/
│   │   └── rate-limiter/
│   ├── api-gateway/
│   │   ├── src/
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   ├── auth/
│   │   │   └── app.go
│   │   ├── go.mod
│   │   ├── go.sum
│   │   └── Dockerfile
│   └── session-manager/
├── libs/
│   ├── shared-models/
│   │   ├── src/
│   │   │   ├── types/
│   │   │   ├── events/
│   │   │   └── schemas/
│   │   └── package.json
│   ├── common-utils/
│   │   ├── src/
│   │   │   ├── logging/
│   │   │   ├── metrics/
│   │   │   ├── config/
│   │   │   └── validation/
│   │   └── setup.py
│   └── security/
│       ├── src/
│       │   ├── encryption/
│       │   ├── authentication/
│       │   └── authorization/
│       └── Cargo.toml
├── infrastructure/
│   ├── kubernetes/
│   │   ├── base/
│   │   │   ├── namespace.yml
│   │   │   ├── configmap.yml
│   │   │   ├── secret.yml
│   │   │   └── kustomization.yml
│   │   ├── staging/
│   │   │   ├── deployment.yml
│   │   │   ├── service.yml
│   │   │   ├── ingress.yml
│   │   │   └── kustomization.yml
│   │   └── production/
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── eks-cluster/
│   │   │   ├── rds/
│   │   │   ├── redis/
│   │   │   └── monitoring/
│   │   ├── environments/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── main.tf
│   ├── helm/
│   │   ├── chatgpt-agent/
│   │   │   ├── templates/
│   │   │   ├── values.yaml
│   │   │   ├── values-staging.yaml
│   │   │   ├── values-production.yaml
│   │   │   └── Chart.yaml
│   │   └── monitoring/
│   └── docker-compose/
│       ├── development.yml
│       ├── testing.yml
│       └── local.yml
├── tools/
│   ├── cli/
│   │   ├── src/
│   │   │   ├── commands/
│   │   │   ├── utils/
│   │   │   └── main.py
│   │   ├── setup.py
│   │   └── requirements.txt
│   ├── monitoring/
│   │   ├── dashboards/
│   │   ├── alerts/
│   │   └── scripts/
│   └── migration/
├── docs/
│   ├── architecture/
│   │   ├── system-overview.md
│   │   ├── component-design.md
│   │   └── data-flow.md
│   ├── api/
│   │   ├── openapi.yml
│   │   ├── authentication.md
│   │   └── rate-limiting.md
│   ├── deployment/
│   │   ├── getting-started.md
│   │   ├── configuration.md
│   │   └── troubleshooting.md
│   └── development/
│       ├── contributing.md
│       ├── testing.md
│       └── coding-standards.md
├── scripts/
│   ├── build/
│   │   ├── build-all.sh
│   │   ├── test-all.sh
│   │   └── lint-all.sh
│   ├── deployment/
│   │   ├── deploy-staging.sh
│   │   ├── deploy-production.sh
│   │   └── rollback.sh
│   └── utilities/
├── .gitignore
├── .dockerignore
├── Makefile
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── SECURITY.md
```

## Development Environment Setup

### Prerequisites Installation Script
```bash
#!/bin/bash
# setup-dev-env.sh

set -e

echo "Setting up ChatGPT Agent development environment..."

# Check system requirements
check_requirements() {
    echo "Checking system requirements..."
    
    # Check if running on supported OS
    if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
        echo "Error: Unsupported operating system. Use Linux or macOS."
        exit 1
    fi
    
    # Check available memory (minimum 8GB required)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    else
        MEMORY_GB=$(sysctl hw.memsize | awk '{print int($2/1024/1024/1024)}')
    fi
    
    if [[ $MEMORY_GB -lt 8 ]]; then
        echo "Warning: Less than 8GB RAM detected. Some services may not run properly."
    fi
}

# Install Docker and Docker Compose
install_docker() {
    echo "Installing Docker..."
    
    if command -v docker &> /dev/null; then
        echo "Docker already installed: $(docker --version)"
        return
    fi
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
    else
        echo "Please install Docker Desktop for macOS manually"
        exit 1
    fi
}

# Install Kubernetes CLI tools
install_k8s_tools() {
    echo "Installing Kubernetes tools..."
    
    # Install kubectl
    if ! command -v kubectl &> /dev/null; then
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/$(uname -s | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
        chmod +x kubectl
        sudo mv kubectl /usr/local/bin/
    fi
    
    # Install kind (Kubernetes in Docker)
    if ! command -v kind &> /dev/null; then
        curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-$(uname)-amd64
        chmod +x ./kind
        sudo mv ./kind /usr/local/bin/kind
    fi
    
    # Install Helm
    if ! command -v helm &> /dev/null; then
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    fi
}

# Install language-specific tools
install_language_tools() {
    echo "Installing language tools..."
    
    # Install Node.js and npm
    if ! command -v node &> /dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
    
    # Install Python and pip
    if ! command -v python3 &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    fi
    
    # Install Java (OpenJDK 17)
    if ! command -v java &> /dev/null; then
        sudo apt-get install -y openjdk-17-jdk
    fi
    
    # Install Go
    if ! command -v go &> /dev/null; then
        GO_VERSION="1.21.0"
        wget https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz
        sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
        echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
        rm go${GO_VERSION}.linux-amd64.tar.gz
    fi
    
    # Install Rust
    if ! command -v cargo &> /dev/null; then
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        source ~/.cargo/env
    fi
}

# Setup local development cluster
setup_local_cluster() {
    echo "Setting up local Kubernetes cluster..."
    
    # Create kind cluster configuration
    cat <<EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
- role: worker
EOF
    
    # Create cluster
    kind create cluster --config kind-config.yaml --name chatgpt-agent-dev
    
    # Install NGINX Ingress Controller
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
    
    # Wait for ingress controller to be ready
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=90s
}

# Main execution
main() {
    check_requirements
    install_docker
    install_k8s_tools
    install_language_tools
    setup_local_cluster
    
    echo "Development environment setup complete!"
    echo "Next steps:"
    echo "1. Clone the repository: git clone https://github.com/openai/chatgpt-agent.git"
    echo "2. Run: make dev-setup"
    echo "3. Run: make dev-start"
}

main "$@"
```

## Build System Configuration

### Root Makefile
```makefile
# Makefile for ChatGPT Agent monorepo

.PHONY: help dev-setup dev-start dev-stop test lint build deploy clean

# Default target
help:
	@echo "Available targets:"
	@echo "  dev-setup    - Set up development environment"
	@echo "  dev-start    - Start all services locally"
	@echo "  dev-stop     - Stop all local services"
	@echo "  test         - Run all tests"
	@echo "  lint         - Run linting on all code"
	@echo "  build        - Build all services"
	@echo "  deploy       - Deploy to staging environment"
	@echo "  clean        - Clean build artifacts"

# Development environment setup
dev-setup:
	@echo "Setting up development environment..."
	./scripts/build/setup-dev-env.sh
	$(MAKE) install-deps
	$(MAKE) generate-certs
	$(MAKE) setup-databases

# Install dependencies for all services
install-deps:
	@echo "Installing dependencies..."
	# Java services
	cd services/task-orchestrator && mvn clean install -DskipTests
	# Python services
	cd services/virtual-computer && pip install -r requirements.txt
	cd libs/common-utils && pip install -e .
	# Node.js services
	cd services/tool-integration/browser && npm install
	cd libs/shared-models && npm install
	# Go services
	cd services/api-gateway && go mod download
	# Rust services
	cd libs/security && cargo build

# Generate development certificates
generate-certs:
	@echo "Generating development certificates..."
	mkdir -p .certs
	openssl req -x509 -newkey rsa:4096 -keyout .certs/key.pem -out .certs/cert.pem -sha256 -days 365 -nodes -subj "/CN=localhost"

# Setup local databases
setup-databases:
	@echo "Setting up local databases..."
	docker-compose -f infrastructure/docker-compose/development.yml up -d postgres redis
	sleep 10
	# Run database migrations
	cd services/session-manager && python manage.py migrate

# Start all services in development mode
dev-start:
	@echo "Starting all services..."
	docker-compose -f infrastructure/docker-compose/development.yml up -d
	# Wait for services to be healthy
	./scripts/utilities/wait-for-services.sh

# Stop all local services
dev-stop:
	@echo "Stopping all services..."
	docker-compose -f infrastructure/docker-compose/development.yml down

# Run all tests
test:
	@echo "Running tests..."
	$(MAKE) test-unit
	$(MAKE) test-integration
	$(MAKE) test-e2e

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	# Java tests
	cd services/task-orchestrator && mvn test
	# Python tests
	cd services/virtual-computer && python -m pytest tests/unit/
	# Node.js tests
	cd services/tool-integration/browser && npm test
	# Go tests
	cd services/api-gateway && go test ./...
	# Rust tests
	cd libs/security && cargo test

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	cd tests/integration && python -m pytest -v

# Run end-to-end tests
test-e2e:
	@echo "Running end-to-end tests..."
	cd tests/e2e && npm run test

# Run linting on all code
lint:
	@echo "Running linting..."
	# Java
	cd services/task-orchestrator && mvn checkstyle:check
	# Python
	find . -name "*.py" -not -path "./venv/*" | xargs black --check
	find . -name "*.py" -not -path "./venv/*" | xargs flake8
	# Node.js/TypeScript
	cd services/tool-integration/browser && npm run lint
	# Go
	cd services/api-gateway && golangci-lint run
	# Rust
	cd libs/security && cargo clippy -- -D warnings

# Build all services
build:
	@echo "Building all services..."
	# Build Docker images
	docker build -t chatgpt-agent/task-orchestrator:latest services/task-orchestrator/
	docker build -t chatgpt-agent/virtual-computer:latest services/virtual-computer/
	docker build -t chatgpt-agent/browser-tool:latest services/tool-integration/browser/
	docker build -t chatgpt-agent/api-gateway:latest services/api-gateway/
	docker build -t chatgpt-agent/safety-monitor:latest services/safety-monitor/

# Deploy to staging environment
deploy:
	@echo "Deploying to staging..."
	./scripts/deployment/deploy-staging.sh

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	# Java
	cd services/task-orchestrator && mvn clean
	# Python
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	# Node.js
	find . -type d -name "node_modules" -not -path "./node_modules" -exec rm -rf {} +
	# Go
	cd services/api-gateway && go clean
	# Rust
	cd libs/security && cargo clean
	# Docker
	docker system prune -f
```

## Testing Framework Configuration

### Integration Test Setup
```python
# tests/integration/conftest.py
"""
Pytest configuration for integration tests
"""

import pytest
import asyncio
import docker
import requests
import time
from typing import Generator, Dict, Any

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def docker_client():
    """Docker client for managing test containers."""
    client = docker.from_env()
    yield client
    client.close()

@pytest.fixture(scope="session")
def test_environment(docker_client) -> Generator[Dict[str, Any], None, None]:
    """
    Set up a complete test environment with all services running.
    """
    # Start test infrastructure
    compose_file = "infrastructure/docker-compose/testing.yml"
    
    # Use docker-compose to start services
    import subprocess
    subprocess.run([
        "docker-compose", "-f", compose_file, "up", "-d"
    ], check=True)
    
    # Wait for services to be healthy
    wait_for_services([
        ("task-orchestrator", "http://localhost:8080/health"),
        ("api-gateway", "http://localhost:8000/health"),
        ("virtual-computer", "http://localhost:8001/health"),
    ])
    
    environment_info = {
        "api_base_url": "http://localhost:8000",
        "orchestrator_url": "http://localhost:8080",
        "virtual_computer_url": "http://localhost:8001",
    }
    
    yield environment_info
    
    # Cleanup
    subprocess.run([
        "docker-compose", "-f", compose_file, "down", "-v"
    ], check=True)

def wait_for_services(services: list, timeout: int = 300):
    """Wait for all services to be healthy."""
    start_time = time.time()
    
    for service_name, health_url in services:
        while time.time() - start_time < timeout:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ {service_name} is healthy")
                    break
            except requests.RequestException:
                time.sleep(2)
                continue
        else:
            raise TimeoutError(f"Service {service_name} did not become healthy within {timeout} seconds")

@pytest.fixture
def api_client(test_environment):
    """HTTP client configured for the test API."""
    from tests.utils.api_client import TestAPIClient
    
    return TestAPIClient(
        base_url=test_environment["api_base_url"],
        api_key="test-api-key"
    )
```

### End-to-End Test Framework
```javascript
// tests/e2e/playwright.config.js
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './specs',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['allure-playwright']
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Code Quality and Standards

### Pre-commit Hooks Configuration
```yaml
# .pre-commit-config.yaml
repos:
  # General
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-case-conflict

  # Python
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings, flake8-import-order]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.47.0
    hooks:
      - id: eslint
        files: \.(js|ts|jsx|tsx)$
        types: [file]
        additional_dependencies:
          - eslint@8.47.0
          - "@typescript-eslint/parser@6.4.1"
          - "@typescript-eslint/eslint-plugin@6.4.1"

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.3
    hooks:
      - id: prettier
        files: \.(js|ts|jsx|tsx|json|yaml|yml|md)$

  # Go
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet-mod
      - id: go-mod-tidy

  # Rust
  - repo: https://github.com/doublify/pre-commit-rust
    rev: v1.0
    hooks:
      - id: fmt
      - id: cargo-check
      - id: clippy

  # Security
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  # Documentation
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.36.0
    hooks:
      - id: markdownlint
```

### IDE Configuration
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.blackEnabled": true,
  "python.formatting.provider": "black",
  "go.formatTool": "goimports",
  "go.lintTool": "golangci-lint",
  "rust-analyzer.checkOnSave.command": "clippy",
  "eslint.workingDirectories": [
    "services/tool-integration/browser",
    "libs/shared-models"
  ],
  "typescript.preferences.importModuleSpecifier": "relative",
  "java.configuration.maven.userSettings": "maven-settings.xml",
  "java.compile.nullAnalysis.mode": "automatic"
}
```

This comprehensive codebase setup provides a solid foundation for developing, testing, and maintaining the ChatGPT Agent system with proper tooling, automation, and quality controls in place.