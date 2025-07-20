# ChatGPT Agent - Multi-Model Implementation

[![CI/CD Pipeline](https://github.com/openai/chatgpt-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/openai/chatgpt-agent/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/openai/chatgpt-agent/branch/main/graph/badge.svg)](https://codecov.io/gh/openai/chatgpt-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This repository contains the auto-selected multi-agent scaffold implementation based on comprehensive research synthesis from multiple AI models (O3, Claude-4-Sonnet, Claude-4-Opus). The system implements a hierarchical agent architecture optimized for task decomposition, execution, and verification.

## Architecture

The system employs a three-agent architecture:

```
┌─────────────────────────────────────────────┐
│           API Gateway (FastAPI)             │
├─────────────────────────────────────────────┤
│         Task Orchestration Engine           │
│   ┌──────────┬──────────┬──────────┐      │
│   │ Planner  │ Executor │ Verifier │      │
│   │  Agent   │  Agent   │  Agent   │      │
│   └──────────┴──────────┴──────────┘      │
├─────────────────────────────────────────────┤
│         Virtual Execution Environment       │
└─────────────────────────────────────────────┘
```

## Features

- **Hierarchical Task Decomposition**: Breaks complex tasks into manageable subtasks
- **Asynchronous Processing**: Built on Python asyncio for scalable execution
- **Multi-Layer Safety**: Comprehensive validation and security measures
- **Modular Design**: Easy to extend with new agent types and capabilities
- **Production Ready**: Includes monitoring, logging, and deployment configurations

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Redis (for state management)

### Installation

```bash
# Clone the repository
git clone https://github.com/openai/chatgpt-agent.git
cd chatgpt-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running the Application

```bash
# Using Make
make run

# Or directly with uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Using Docker
docker-compose up
```

### API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests

```bash
# Run all tests with coverage
make test

# Run specific test suite
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Run all quality checks
make all
```

### Building Docker Image

```bash
make docker-build
```

## API Examples

### Submit a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "objective": "Analyze market trends for AI agents",
    "steps": ["Research current market", "Identify key players", "Analyze trends"],
    "safety_critical": false
  }'
```

### Check Health

```bash
curl http://localhost:8000/health
```

### List Agents

```bash
curl http://localhost:8000/agents
```

## Project Structure

```
.
├── src/                    # Source code
│   ├── core/              # Core agent implementations
│   │   └── base_agent.py  # Base agent classes
│   └── main.py           # FastAPI application
├── infra/                 # Infrastructure configurations
│   └── Dockerfile        # Container definition
├── prompts/              # Agent prompt templates
├── .github/              # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml       # CI/CD pipeline
├── experiments/          # Experiment results
├── scripts/              # Utility scripts
├── tests/               # Test suites
├── requirements.txt     # Python dependencies
├── setup.py            # Package configuration
├── Makefile            # Development commands
└── README.md           # This file
```

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline that:

- **Matrix Testing**: Tests across multiple Python versions and model configurations
- **Security Scanning**: Semgrep SAST analysis for security vulnerabilities
- **Code Quality**: Black formatting, Ruff linting, MyPy type checking
- **Coverage Reporting**: Automated coverage upload to Codecov
- **Docker Publishing**: Multi-platform image builds pushed to GitHub Container Registry
- **Automated Releases**: Creates releases on main branch merges

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Research Background

This implementation is based on synthesis of research from:
- **O3**: Hierarchical task decomposition and efficiency optimization
- **Claude-4-Sonnet**: Holistic multi-model integration and knowledge synthesis
- **Claude-4-Opus**: Practical unified agent system with comprehensive metrics

See [SYNTHESIS_REPORT.md](SYNTHESIS_REPORT.md) for detailed analysis.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Multi-model research synthesis approach
- FastAPI for the excellent web framework
- The open-source community for various tools and libraries

---

**Note**: This is an experimental implementation based on research synthesis. Use in production environments should be done with appropriate testing and security reviews. 