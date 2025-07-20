# Σ-Builder: O3 Prompt via Sonnet Model

This implementation represents a cross-model experiment where the O3 Σ-Builder prompt is interpreted through Claude Sonnet's synthesis-focused approach.

## Overview

The Σ-Builder (Sigma-Builder) is a multi-model research ingestion and implementation agent that:
- Digests research from multiple model perspectives (O3, Claude-4-Sonnet, Claude-4-Opus)
- Builds a holistic knowledge graph synthesizing insights
- Generates implementation plans based on consensus patterns and valuable divergences
- Follows the structured workflow: Research → Synthesis → Planning → Implementation → QA

## Key Features

- **Knowledge Graph Construction**: NetworkX-based graph for insight relationships
- **Multi-Phase Workflow**: Structured progression through research digestion, synthesis, and planning
- **Consensus & Divergence Analysis**: Identifies shared patterns and unique perspectives
- **Async Architecture**: Built on FastAPI with full async/await support
- **Structured Logging**: JSON-formatted logs for observability

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd experiments/2025-07-19/cross/o3-prompt-sonnet-model

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```bash
# Run the FastAPI server
uvicorn src.main:app --reload

# Or use the Docker container
docker build -t sigma-builder-o3-sonnet .
docker run -p 8000:8000 sigma-builder-o3-sonnet
```

## API Endpoints

- `GET /` - API information and available endpoints
- `POST /workflow/start` - Start complete Σ-Builder workflow
- `GET /workflow/{workflow_id}/status` - Check workflow status
- `POST /phase/execute` - Execute specific phase
- `POST /research/digest` - Run research digestion
- `POST /synthesis/report` - Generate synthesis report
- `POST /implementation/plan` - Create implementation plan
- `GET /agents` - List available agents
- `GET /health` - Health check

## Architecture

This implementation emphasizes Sonnet's holistic synthesis approach while following O3's structured workflow:

```
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ Research Files  │ --> │ Research Digest  │ --> │ Knowledge Graph    │
└─────────────────┘     └──────────────────┘     └────────────────────┘
                                                            │
                                                            v
┌─────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│ Implementation  │ <-- │ Synthesis Report │ <-- │ Pattern Analysis   │
└─────────────────┘     └──────────────────┘     └────────────────────┘
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_synthesis_agents.py -v
```

## Configuration

The application uses environment variables for configuration:

- `LOG_LEVEL` - Logging level (default: INFO)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

## Cross-Model Experiment Details

This implementation demonstrates how the O3 prompt's structured approach to multi-model research synthesis can be enhanced with Sonnet's focus on:
- Holistic knowledge graph construction
- Deep synthesis of convergent and divergent insights
- Comprehensive pattern recognition across models

## License

MIT License - See LICENSE file for details 