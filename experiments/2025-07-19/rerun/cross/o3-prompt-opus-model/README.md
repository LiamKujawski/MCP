# Σ-Builder: O3 Prompt via Opus Model

This implementation represents a cross-model experiment where the O3 Σ-Builder prompt is interpreted through Claude Opus's unified and pragmatic approach.

## Overview

The Σ-Builder (Sigma-Builder) is a multi-model research ingestion and implementation agent that:
- Processes all workflow phases in a single unified execution
- Emphasizes practical end-to-end processing
- Streamlines the research → synthesis → implementation pipeline
- Follows Opus's pragmatic single-agent architecture

## Key Features

- **Unified Agent Architecture**: Single agent handles all phases
- **Streamlined Workflow**: All phases execute in one continuous flow
- **Pragmatic Focus**: Emphasis on getting results efficiently
- **Comprehensive Metrics**: Detailed tracking of all operations
- **Async Processing**: Built on FastAPI with full async support

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd experiments/2025-07-19/cross/o3-prompt-opus-model

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
docker build -t sigma-builder-o3-opus .
docker run -p 8000:8000 sigma-builder-o3-opus
```

## API Endpoints

- `GET /` - API information and characteristics
- `POST /workflow/execute` - Execute complete workflow
- `GET /workflow/{workflow_id}` - Get workflow status
- `GET /metrics` - System and performance metrics
- `POST /simulate` - Run simulation workflow
- `GET /health` - Health check

## Architecture

This implementation follows Opus's unified approach to the O3 workflow:

```
┌─────────────────────────────────────────────┐
│           Unified Σ Agent                    │
│                                             │
│  ┌─────────────┐  ┌──────────────┐         │
│  │  Research   │→ │  Synthesis   │         │
│  │  Digestion  │  │   Report     │         │
│  └─────────────┘  └──────────────┘         │
│          ↓               ↓                  │
│  ┌─────────────────────────────┐           │
│  │   Implementation Plan        │           │
│  └─────────────────────────────┘           │
└─────────────────────────────────────────────┘
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_unified_agent.py -v
```

## Configuration

The application uses environment variables for configuration:

- `LOG_LEVEL` - Logging level (default: INFO)
- `API_HOST` - API host (default: 0.0.0.0)
- `API_PORT` - API port (default: 8000)

## Cross-Model Experiment Details

This implementation demonstrates how the O3 prompt's structured multi-phase approach can be simplified through Opus's unified architecture:
- Single agent manages all phases
- Streamlined execution flow
- Pragmatic focus on results over process
- Efficient resource utilization

## Performance Characteristics

- **Execution Model**: Single continuous workflow
- **Phase Handling**: All phases in one execution
- **Error Recovery**: Unified error handling
- **Resource Usage**: Optimized for single-agent operation

## License

MIT License - See LICENSE file for details 