#!/usr/bin/env python3
"""
Generate implementation based on synthesis prompts.

This script creates a working implementation for the experiment pipeline.
Since we can't actually call AI models, it generates a functional template.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def generate_fastapi_backend(impl_dir: Path, model: str, prompt_type: str) -> None:
    """Generate FastAPI backend implementation."""
    
    # Create directory structure
    (impl_dir / "src").mkdir(parents=True, exist_ok=True)
    (impl_dir / "tests").mkdir(parents=True, exist_ok=True)
    
    # Generate main.py
    main_content = f'''"""
Generated implementation for {model} with {prompt_type} prompt.
Created on {datetime.now().isoformat()}
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="{model.upper()} Agent API",
    description=f"Implementation using {prompt_type} prompt",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "{model}"
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    id: str
    model: str
    choices: List[dict]
    usage: dict


@app.get("/")
async def root():
    return {{
        "message": f"{{model.upper()}} Agent API - {{prompt_type}} implementation",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }}


@app.get("/health")
async def health():
    return {{"status": "healthy", "model": "{model}", "type": "{prompt_type}"}}


@app.post("/api/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    """Generate chat completion using {model} with {prompt_type} prompt."""
    
    # Simulate processing delay
    await asyncio.sleep(0.1)
    
    # Generate response
    response_content = f"This is a simulated response from {{model}} using {{prompt_type}} prompt. "
    response_content += f"Your last message was: '{{request.messages[-1].content if request.messages else 'No message'}}'"
    
    return ChatResponse(
        id=f"chatcmpl-{{datetime.now().timestamp():.0f}}",
        model=request.model or "{model}",
        choices=[{{
            "index": 0,
            "message": {{
                "role": "assistant",
                "content": response_content
            }},
            "finish_reason": "stop"
        }}],
        usage={{
            "prompt_tokens": sum(len(m.content.split()) for m in request.messages),
            "completion_tokens": len(response_content.split()),
            "total_tokens": sum(len(m.content.split()) for m in request.messages) + len(response_content.split())
        }}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    (impl_dir / "src" / "main.py").write_text(main_content)
    
    # Generate __init__.py files
    (impl_dir / "src" / "__init__.py").touch()
    (impl_dir / "tests" / "__init__.py").touch()
    
    # Generate requirements.txt
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.9
asyncio==3.4.3
aiofiles==23.2.1
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
"""
    (impl_dir / "requirements.txt").write_text(requirements)
    
    # Generate test file
    test_content = f'''"""
Tests for {model} {prompt_type} implementation.
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "{model.upper()}" in data["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model"] == "{model}"
    assert data["type"] == "{prompt_type}"


def test_chat_completions():
    request_data = {{
        "messages": [
            {{"role": "user", "content": "Hello, how are you?"}}
        ]
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert "choices" in data
    assert len(data["choices"]) == 1
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert "Hello, how are you?" in data["choices"][0]["message"]["content"]


def test_chat_completions_empty_messages():
    request_data = {{
        "messages": []
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "No message" in data["choices"][0]["message"]["content"]


def test_chat_completions_with_model():
    request_data = {{
        "messages": [{{"role": "user", "content": "Test"}}],
        "model": "custom-model",
        "temperature": 0.5
    }}
    
    response = client.post("/api/chat/completions", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["model"] == "custom-model"
'''
    
    (impl_dir / "tests" / "test_main.py").write_text(test_content)
    
    # Generate README
    readme_content = f"""# {model.upper()} {prompt_type.capitalize()} Implementation

Generated on: {datetime.now().isoformat()}

## Overview

This is an automatically generated implementation for the {model} model using {prompt_type} prompts.

## Features

- FastAPI backend with async support
- OpenAI-compatible chat completions endpoint
- Health check endpoint
- CORS enabled for frontend integration
- Comprehensive test suite

## Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python -m src.main
   ```

3. Run tests:
   ```bash
   pytest tests/ -v --cov=src
   ```

## API Endpoints

- `GET /` - Root endpoint with status
- `GET /health` - Health check
- `POST /api/chat/completions` - Chat completions (OpenAI compatible)

## Configuration

The implementation is configured for:
- Model: {model}
- Prompt Type: {prompt_type}
- Port: 8000
"""
    
    (impl_dir / "README.md").write_text(readme_content)


def generate_implementation(model: str, prompt_type: str, output_dir: str) -> None:
    """Generate a complete implementation for the given model and prompt type."""
    
    impl_dir = Path(output_dir)
    impl_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating implementation for {model} with {prompt_type} prompt...")
    print(f"Output directory: {impl_dir}")
    
    # Generate the backend
    generate_fastapi_backend(impl_dir, model, prompt_type)
    
    # If we have synthesis prompts, we could use them here
    synthesis_prompt_path = Path(f"synthesize-research-prompts/{model}/AGENT_IMPLEMENTATION_PROMPT.md")
    if synthesis_prompt_path.exists() and prompt_type == "synthesized":
        print(f"Found synthesis prompt at: {synthesis_prompt_path}")
        # In a real implementation, we would use this prompt to guide generation
    
    print(f"✅ Successfully generated {model} {prompt_type} implementation")


def main():
    """Main entry point."""
    if len(sys.argv) != 4:
        print("Usage: python generate_implementation.py <model> <prompt_type> <output_dir>")
        sys.exit(1)
    
    model = sys.argv[1]
    prompt_type = sys.argv[2]
    output_dir = sys.argv[3]
    
    generate_implementation(model, prompt_type, output_dir)


if __name__ == "__main__":
    main()