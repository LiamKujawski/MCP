#!/usr/bin/env python3
"""
Generate varied implementations based on model and prompt type.

This creates functional but differentiated implementations to simulate
what real AI models would generate.
"""

import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Model-specific characteristics
MODEL_TRAITS = {
    "o3": {
        "style": "comprehensive",
        "features": ["advanced_monitoring", "distributed_tracing", "multi_stage_pipeline"],
        "libraries": ["prometheus_client", "opentelemetry-api", "celery"],
        "complexity": "high"
    },
    "claude-4-sonnet": {
        "style": "balanced",
        "features": ["websocket_support", "rate_limiting", "caching"],
        "libraries": ["python-socketio", "slowapi", "redis"],
        "complexity": "medium"
    },
    "claude-4-opus": {
        "style": "elegant",
        "features": ["graphql_api", "auth_system", "data_validation"],
        "libraries": ["strawberry-graphql", "python-jose[cryptography]", "pydantic[email]"],
        "complexity": "medium-high"
    }
}

# Prompt type variations
PROMPT_VARIATIONS = {
    "baseline": {
        "focus": "standard_implementation",
        "extra_features": []
    },
    "synthesized": {
        "focus": "enhanced_implementation",
        "extra_features": ["experiment_tracking", "a_b_testing", "feature_flags"]
    }
}


def generate_requirements(model: str, prompt_type: str) -> str:
    """Generate requirements.txt based on model and prompt type."""
    base_requirements = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "pydantic==2.5.0",
        "python-multipart==0.0.6",
        "httpx==0.25.1",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "pytest-cov==4.1.0",
        "networkx==3.2"
    ]
    
    # Add model-specific libraries
    model_libs = MODEL_TRAITS.get(model, {}).get("libraries", [])
    
    # Add extra libraries for synthesized prompts
    if prompt_type == "synthesized":
        model_libs.extend(["mlflow", "python-dotenv", "structlog"])
    
    all_requirements = base_requirements + model_libs
    return "\n".join(all_requirements) + "\n"


def generate_main_py(model: str, prompt_type: str) -> str:
    """Generate main.py with model-specific features."""
    traits = MODEL_TRAITS.get(model, {})
    features = traits.get("features", [])
    
    if prompt_type == "synthesized":
        features.extend(PROMPT_VARIATIONS["synthesized"]["extra_features"])
    
    # Base imports
    imports = [
        "from fastapi import FastAPI, HTTPException, Depends, Request",
        "from fastapi.middleware.cors import CORSMiddleware",
        "from pydantic import BaseModel, Field, validator",
        "from typing import List, Optional, Dict, Any",
        "import asyncio",
        "import logging",
        "import json",
        "from datetime import datetime",
        "import uuid"
    ]
    
    # Add model-specific imports
    if "websocket_support" in features:
        imports.append("from fastapi import WebSocket")
    if "rate_limiting" in features:
        imports.append("from slowapi import Limiter, _rate_limit_exceeded_handler")
        imports.append("from slowapi.util import get_remote_address")
    if "distributed_tracing" in features:
        imports.append("from opentelemetry import trace")
        imports.append("from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor")
    if "graphql_api" in features:
        imports.append("import strawberry")
        imports.append("from strawberry.fastapi import GraphQLRouter")
    
    # Generate the main application code
    code = f'''"""
Generated implementation for {model} with {prompt_type} prompt.
Created on {datetime.now().isoformat()}

Model Style: {traits.get('style', 'standard')}
Features: {', '.join(features)}
"""

{chr(10).join(imports)}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

'''

    # Add rate limiter if needed
    if "rate_limiting" in features:
        code += '''limiter = Limiter(key_func=get_remote_address)

'''

    # Create FastAPI app
    code += f'''app = FastAPI(
    title="{model.upper()} Agent API",
    description="Implementation using {prompt_type} prompt with {traits.get('style', 'standard')} style",
    version="2.0.0"
)
'''

    # Add middleware
    code += '''
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

    # Add rate limiting middleware if needed
    if "rate_limiting" in features:
        code += '''
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
'''

    # Add tracing if needed
    if "distributed_tracing" in features:
        code += '''
# Setup tracing
tracer = trace.get_tracer(__name__)
FastAPIInstrumentor.instrument_app(app)
'''

    # Add data models
    code += '''

class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

    @validator('role')
    def validate_role(cls, v):
        if v not in ['system', 'user', 'assistant']:
            raise ValueError('Invalid role')
        return v


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = Field(default="{}", description="Model to use")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000)
    stream: Optional[bool] = Field(default=False)
'''.format(model)

    # Add feature flags if synthesized
    if "feature_flags" in features:
        code += '''    feature_flags: Optional[Dict[str, bool]] = Field(default_factory=dict)
'''

    code += '''

class ChatResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chat-{uuid.uuid4()}")
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]
    metadata: Optional[Dict[str, Any]] = None
'''

    # Add health check with model-specific info
    code += f'''

@app.get("/health")
async def health_check():
    """Health check endpoint with detailed status."""
    return {{
        "status": "healthy",
        "model": "{model}",
        "prompt_type": "{prompt_type}",
        "features": {features},
        "timestamp": datetime.now().isoformat()
    }}
'''

    # Add main chat endpoint with model-specific logic
    if "rate_limiting" in features:
        code += '''

@app.post("/api/chat/completions", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_completions(request: ChatRequest, req: Request):'''
    else:
        code += '''

@app.post("/api/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):'''
    
    code += '''
    """Main chat completions endpoint."""
    try:
        # Model-specific processing
'''
    
    if "distributed_tracing" in features:
        code += '''        with tracer.start_as_current_span("chat_completion"):
'''
        indent = "            "
    else:
        indent = "        "
    
    code += f'''{indent}messages = request.messages
{indent}if not messages:
{indent}    raise HTTPException(status_code=400, detail="No messages provided")
        
{indent}# Simulate model-specific processing
{indent}response_content = f"[{model.upper()}] "
'''
    
    if traits.get("complexity") == "high":
        code += f'''{indent}response_content += "Advanced analysis: "
'''
    elif traits.get("style") == "elegant":
        code += f'''{indent}response_content += "Thoughtful response: "
'''
    
    code += f'''{indent}response_content += f"Processed {{len(messages)}} messages"
        
{indent}# Add feature-specific information
'''
    
    if "experiment_tracking" in features:
        code += f'''{indent}experiment_id = str(uuid.uuid4())
{indent}response_content += f" (Experiment: {{experiment_id[:8]}})"
'''
    
    code += f'''
{indent}response = ChatResponse(
{indent}    model=request.model or "{model}",
{indent}    choices=[{{
{indent}        "index": 0,
{indent}        "message": {{
{indent}            "role": "assistant",
{indent}            "content": response_content
{indent}        }},
{indent}        "finish_reason": "stop"
{indent}    }}],
{indent}    usage={{
{indent}        "prompt_tokens": sum(len(m.content.split()) for m in messages),
{indent}        "completion_tokens": len(response_content.split()),
{indent}        "total_tokens": sum(len(m.content.split()) for m in messages) + len(response_content.split())
{indent}    }}
{indent})
        
{indent}return response
        
    except Exception as e:
        logger.error(f"Error in chat completion: {{str(e)}}")
        raise HTTPException(status_code=500, detail=str(e))
'''

    # Add WebSocket support if included
    if "websocket_support" in features:
        code += '''

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for streaming chat."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[{model}] Echo: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()
'''

    # Add GraphQL if included
    if "graphql_api" in features:
        code += '''

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return f"Hello from {model} GraphQL API"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
'''

    # Add metrics endpoint if monitoring included
    if "advanced_monitoring" in features:
        code += '''

@app.get("/metrics")
async def metrics():
    """Prometheus-compatible metrics endpoint."""
    return {
        "requests_total": 1000,
        "errors_total": 10,
        "latency_seconds": 0.05
    }
'''

    code += '''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

    return code


def generate_tests(model: str, prompt_type: str) -> str:
    """Generate comprehensive tests."""
    traits = MODEL_TRAITS.get(model, {})
    features = traits.get("features", [])
    
    test_code = f'''"""
Tests for {model} {prompt_type} implementation.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model"] == "{model}"
    assert data["prompt_type"] == "{prompt_type}"


def test_chat_completions_basic():
    """Test basic chat completion."""
    request_data = {{
        "messages": [{{"role": "user", "content": "Hello"}}]
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert data["model"] == "{model}"
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert "[{model.upper()}]" in data["choices"][0]["message"]["content"]


def test_chat_completions_empty_messages():
    """Test error handling for empty messages."""
    request_data = {{
        "messages": []
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 400


def test_chat_completions_with_parameters():
    """Test chat completion with custom parameters."""
    request_data = {{
        "messages": [{{"role": "user", "content": "Test"}}],
        "model": "custom-model",
        "temperature": 0.5,
        "max_tokens": 100
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["model"] == "custom-model"
'''

    # Add WebSocket test if feature is included
    if "websocket_support" in features:
        test_code += '''

def test_websocket():
    """Test WebSocket connection."""
    from fastapi.testclient import TestClient
    
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello WebSocket")
        data = websocket.receive_text()
        assert f"[{model}] Echo: Hello WebSocket" in data
'''

    # Add GraphQL test if included
    if "graphql_api" in features:
        test_code += '''

def test_graphql_query():
    """Test GraphQL endpoint."""
    query = '{ hello }'
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert f"{model}" in data["data"]["hello"]
'''

    # Add rate limiting test if included
    if "rate_limiting" in features:
        test_code += '''

def test_rate_limiting():
    """Test rate limiting."""
    request_data = {
        "messages": [{"role": "user", "content": "Test"}]
    }
    
    # Make multiple requests to trigger rate limit
    for i in range(15):
        response = client.post("/api/chat/completions", json=request_data)
        if i < 10:
            assert response.status_code == 200
        else:
            # Should be rate limited after 10 requests
            assert response.status_code == 429
'''

    # Add validation tests
    test_code += '''

def test_message_validation():
    """Test message validation."""
    request_data = {
        "messages": [{"role": "invalid_role", "content": "Test"}]
    }
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 422  # Validation error


def test_temperature_validation():
    """Test temperature parameter validation."""
    request_data = {
        "messages": [{"role": "user", "content": "Test"}],
        "temperature": 3.0  # Out of range
    }
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 422
'''

    # Add performance test for complex models
    if traits.get("complexity") == "high":
        test_code += '''

@pytest.mark.asyncio
async def test_performance():
    """Test response time for complex processing."""
    import time
    
    request_data = {
        "messages": [{"role": "user", "content": "Complex query"}]
    }
    
    start_time = time.time()
    response = client.post("/api/chat/completions", json=request_data)
    end_time = time.time()
    
    assert response.status_code == 200
    assert end_time - start_time < 1.0  # Should respond within 1 second
'''

    return test_code


def generate_dockerfile(model: str, prompt_type: str) -> str:
    """Generate Dockerfile for the implementation."""
    traits = MODEL_TRAITS.get(model, {})
    
    dockerfile = f'''# Dockerfile for {model} {prompt_type} implementation
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/

# Expose port
EXPOSE 8000

# Set environment variables
ENV MODEL={model}
ENV PROMPT_TYPE={prompt_type}
'''

    # Add monitoring setup for complex models
    if "advanced_monitoring" in traits.get("features", []):
        dockerfile += '''ENV ENABLE_MONITORING=true
'''

    dockerfile += '''
# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    return dockerfile


def generate_readme(model: str, prompt_type: str) -> str:
    """Generate comprehensive README."""
    traits = MODEL_TRAITS.get(model, {})
    features = traits.get("features", [])
    
    readme = f"""# {model.upper()} {prompt_type.capitalize()} Implementation

Generated on: {datetime.now().isoformat()}

## Overview

This is an automatically generated implementation for the {model} model using {prompt_type} prompts.

**Model Style**: {traits.get('style', 'standard')}  
**Complexity**: {traits.get('complexity', 'medium')}  
**Features**: {', '.join(features)}

## Architecture

This implementation follows a {traits.get('style', 'standard')} architecture pattern with the following key components:

"""

    # Add architecture details based on features
    if "distributed_tracing" in features:
        readme += """- **Distributed Tracing**: OpenTelemetry integration for request tracking
"""
    if "websocket_support" in features:
        readme += """- **WebSocket Support**: Real-time bidirectional communication
"""
    if "rate_limiting" in features:
        readme += """- **Rate Limiting**: Request throttling to prevent abuse
"""
    if "graphql_api" in features:
        readme += """- **GraphQL API**: Alternative query interface with schema introspection
"""
    if "advanced_monitoring" in features:
        readme += """- **Advanced Monitoring**: Prometheus-compatible metrics endpoint
"""

    readme += f"""
## API Endpoints

### Core Endpoints

- `GET /health` - Health check endpoint
- `POST /api/chat/completions` - Main chat completions endpoint
"""

    if "websocket_support" in features:
        readme += """- `WS /ws` - WebSocket endpoint for streaming
"""
    if "graphql_api" in features:
        readme += """- `POST /graphql` - GraphQL API endpoint
"""
    if "advanced_monitoring" in features:
        readme += """- `GET /metrics` - Prometheus metrics endpoint
"""

    readme += """
## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

3. Access the API documentation at http://localhost:8000/docs

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t {}-{} .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 {}-{}
   ```

## Testing

Run the test suite:
```bash
pytest tests/ -v --cov=src --cov-report=html
```

## Configuration

The following environment variables can be set:

- `MODEL` - Model identifier (default: {})
- `PROMPT_TYPE` - Prompt type (default: {})
""".format(model, prompt_type, model, prompt_type, model, prompt_type)

    if "advanced_monitoring" in features:
        readme += """- `ENABLE_MONITORING` - Enable Prometheus metrics (default: true)
"""
    if "rate_limiting" in features:
        readme += """- `RATE_LIMIT` - Requests per minute (default: 10)
"""

    readme += f"""
## Performance Characteristics

Based on the {model} model with {prompt_type} prompts:

- **Response Time**: {"< 100ms" if traits.get('complexity') != 'high' else "< 200ms"}
- **Throughput**: {"High" if traits.get('complexity') != 'high' else "Medium"}
- **Memory Usage**: {"Low" if traits.get('complexity') != 'high' else "Medium"}

## License

MIT License
"""

    return readme


def generate_implementation(model: str, prompt_type: str, output_dir: str) -> None:
    """Generate a complete implementation for the given model and prompt type."""
    
    impl_dir = Path(output_dir)
    impl_dir.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    (impl_dir / "src").mkdir(exist_ok=True)
    (impl_dir / "tests").mkdir(exist_ok=True)
    
    print(f"Generating implementation for {model} with {prompt_type} prompt...")
    print(f"Output directory: {impl_dir}")
    
    # Generate all files
    files_to_generate = [
        ("requirements.txt", generate_requirements(model, prompt_type)),
        ("src/main.py", generate_main_py(model, prompt_type)),
        ("src/__init__.py", ""),
        ("tests/test_main.py", generate_tests(model, prompt_type)),
        ("tests/__init__.py", ""),
        ("Dockerfile", generate_dockerfile(model, prompt_type)),
        ("README.md", generate_readme(model, prompt_type))
    ]
    
    for filename, content in files_to_generate:
        filepath = impl_dir / filename
        filepath.write_text(content)
        print(f"  ✓ Generated {filename}")
    
    # Check if we have synthesis prompts and log it
    synthesis_prompt_path = Path(f"synthesize-research-prompts/{model}/AGENT_IMPLEMENTATION_PROMPT.md")
    if synthesis_prompt_path.exists() and prompt_type == "synthesized":
        print(f"  ℹ️  Found synthesis prompt at: {synthesis_prompt_path}")
        # In a real implementation with AI, we would use this prompt
    
    print(f"✅ Successfully generated {model} {prompt_type} implementation")


def main():
    """Main entry point."""
    if len(sys.argv) != 4:
        print("Usage: python generate_implementation_v2.py <model> <prompt_type> <output_dir>")
        sys.exit(1)
    
    model = sys.argv[1]
    prompt_type = sys.argv[2]
    output_dir = sys.argv[3]
    
    if model not in MODEL_TRAITS:
        print(f"Error: Unknown model '{model}'. Valid models: {list(MODEL_TRAITS.keys())}")
        sys.exit(1)
    
    if prompt_type not in PROMPT_VARIATIONS:
        print(f"Error: Unknown prompt type '{prompt_type}'. Valid types: {list(PROMPT_VARIATIONS.keys())}")
        sys.exit(1)
    
    generate_implementation(model, prompt_type, output_dir)


if __name__ == "__main__":
    main()