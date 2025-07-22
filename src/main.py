"""
Σ-Builder FastAPI Application - O3 Prompt via Sonnet Model
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    # Try absolute import first (when running from root with PYTHONPATH set)
    from src.synthesized_agent import (
        ΣBuilderOrchestrator,
        TaskRequest,
        TaskResponse,
        ΣBuilderPhase,
        ResearchDigestionAgent,
        SynthesisReportAgent,
        ImplementationPlanAgent,
        process_sigma_builder_request,
    )
except ImportError:
    # Fall back to relative import (when running from src directory)
    from synthesized_agent import (
        ΣBuilderOrchestrator,
        TaskRequest,
        TaskResponse,
        ΣBuilderPhase,
        ResearchDigestionAgent,
        SynthesisReportAgent,
        ImplementationPlanAgent,
        process_sigma_builder_request,
    )


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    print("Initializing Σ-Builder application...")
    app.state.orchestrator = ΣBuilderOrchestrator()
    app.state.active_tasks = {}
    yield
    print("Shutting down Σ-Builder application...")


# Create FastAPI app
app = FastAPI(
    title="Σ-Builder Multi-Model Research Synthesis",
    description="O3 Prompt interpreted through Sonnet's synthesis approach",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure app state is initialized
if not hasattr(app.state, "active_tasks"):
    app.state.active_tasks = {}
if not hasattr(app.state, "orchestrator"):
    app.state.orchestrator = ΣBuilderOrchestrator()


class WorkflowStatus(BaseModel):
    """Status of workflow execution"""

    workflow_id: str
    status: str
    phases_completed: List[str]
    current_phase: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    error: Optional[str] = None


class PhaseRequest(BaseModel):
    """Request for executing a specific phase"""

    phase: str = Field(..., description="Phase to execute")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Σ-Builder API",
        "description": "Multi-model research synthesis and implementation",
        "implementation": "O3 prompt via Sonnet model",
        "phases": [phase.value for phase in ΣBuilderPhase],
        "endpoints": {
            "/workflow/start": "Start full workflow",
            "/workflow/{workflow_id}/status": "Get workflow status",
            "/phase/execute": "Execute specific phase",
            "/research/digest": "Digest research files",
            "/synthesis/report": "Generate synthesis report",
            "/implementation/plan": "Create implementation plan",
            "/health": "Health check",
        },
    }


@app.post("/workflow/start", response_model=WorkflowStatus)
async def start_workflow(background_tasks: BackgroundTasks):
    """Start the complete Σ-Builder workflow"""
    workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    status = WorkflowStatus(
        workflow_id=workflow_id,
        status="running",
        phases_completed=[],
        current_phase=ΣBuilderPhase.RESEARCH_DIGESTION.value,
        start_time=datetime.now(),
    )

    app.state.active_tasks[workflow_id] = status

    # Run workflow in background
    background_tasks.add_task(
        run_workflow_background, workflow_id, app.state.orchestrator
    )

    return status


async def run_workflow_background(workflow_id: str, orchestrator: ΣBuilderOrchestrator):
    """Run workflow in background"""
    status = app.state.active_tasks[workflow_id]

    try:
        result = await orchestrator.execute_workflow()

        status.status = "completed"
        status.phases_completed = result.get("phases_executed", [])
        status.current_phase = None
        status.end_time = datetime.now()

    except Exception as e:
        status.status = "failed"
        status.error = str(e)
        status.end_time = datetime.now()


@app.get("/workflow/{workflow_id}/status", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str):
    """Get status of a workflow"""
    if workflow_id not in app.state.active_tasks:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return app.state.active_tasks[workflow_id]


@app.post("/phase/execute", response_model=TaskResponse)
async def execute_phase(request: PhaseRequest):
    """Execute a specific phase"""
    task_request = TaskRequest(
        description=f"Execute {request.phase} phase",
        phase=request.phase,
        config=request.context,
    )

    response = await process_sigma_builder_request(task_request)
    return response


@app.post("/research/digest")
async def digest_research():
    """Execute research digestion phase"""
    agent = ResearchDigestionAgent()
    result = await agent.execute({})

    return {
        "status": "completed",
        "insights_count": result.get("insights_count", 0),
        "files_processed": result.get("files_processed", 0),
        "consensus_patterns": len(result.get("consensus_patterns", [])),
        "divergences": len(result.get("divergences", [])),
    }


@app.post("/synthesis/report")
async def generate_synthesis_report(knowledge_graph: Optional[Dict[str, Any]] = None):
    """Generate synthesis report"""
    agent = SynthesisReportAgent()

    context = {}
    if knowledge_graph:
        context["knowledge_graph"] = knowledge_graph

    try:
        result = await agent.execute(context)
        return {
            "status": "completed",
            "report_path": result.get("report_path"),
            "sections": result.get("sections_generated", []),
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/implementation/plan")
async def create_implementation_plan():
    """Create implementation plan"""
    agent = ImplementationPlanAgent()
    result = await agent.execute({})

    return {
        "status": "completed",
        "plan_path": result.get("plan_path"),
        "plan": result.get("plan", {}),
    }


@app.get("/agents")
async def list_agents():
    """List available agents and their phases"""
    return {
        "agents": [
            {
                "name": "ResearchDigestionAgent",
                "phase": ΣBuilderPhase.RESEARCH_DIGESTION.value,
                "description": "Digests research files and builds knowledge graph",
            },
            {
                "name": "SynthesisReportAgent",
                "phase": ΣBuilderPhase.SYNTHESIS_REPORT.value,
                "description": "Generates synthesis report from knowledge graph",
            },
            {
                "name": "ImplementationPlanAgent",
                "phase": ΣBuilderPhase.IMPLEMENTATION_PLAN.value,
                "description": "Creates implementation plan based on synthesis",
            },
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_workflows": len(app.state.active_tasks),
        "implementation": "o3-prompt-sonnet-model",
    }

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI HTML"""
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


# Research Topic Management
class ResearchTopic(BaseModel):
    name: str = Field(..., description="Name of the research topic")
    description: str = Field(..., description="Description of the research topic")
    content: str = Field(..., description="Initial markdown content")


@app.post("/research/topics")
async def create_research_topic(topic: ResearchTopic):
    """Create a new research topic with initial content."""
    import os
    from pathlib import Path
    
    # Sanitize topic name for directory
    safe_name = topic.name.lower().replace(" ", "-").replace("/", "-")
    topic_dir = Path(f"research/{safe_name}")
    
    try:
        # Create directory if it doesn't exist
        topic_dir.mkdir(parents=True, exist_ok=True)
        
        # Create initial markdown file with front matter
        front_matter = f"""---
topic: "{topic.name}"
description: "{topic.description}"
stage: research
version: 1
created: {datetime.now().isoformat()}
---

# {topic.name}

{topic.description}

"""
        
        # Write the initial content
        initial_file = topic_dir / "01_overview.md"
        with open(initial_file, "w") as f:
            f.write(front_matter + topic.content)
        
        return {
            "status": "success",
            "topic": topic.name,
            "path": str(topic_dir),
            "files": ["01_overview.md"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/research/topics")
async def list_research_topics():
    """List all research topics."""
    from pathlib import Path
    import os
    
    research_dir = Path("research")
    topics = []
    
    if research_dir.exists():
        for topic_dir in research_dir.iterdir():
            if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
                # Get files in the topic directory
                files = [f.name for f in topic_dir.iterdir() if f.suffix == '.md']
                files.sort()
                
                # Try to read description from first file
                description = ""
                if files:
                    try:
                        with open(topic_dir / files[0], 'r') as f:
                            content = f.read()
                            # Extract description from front matter if present
                            if content.startswith('---'):
                                front_matter = content.split('---')[1]
                                for line in front_matter.split('\n'):
                                    if line.startswith('description:'):
                                        description = line.split(':', 1)[1].strip().strip('"')
                                        break
                    except:
                        pass
                
                topics.append({
                    "name": topic_dir.name.replace('-', ' ').title(),
                    "path": str(topic_dir),
                    "description": description,
                    "files": files,
                    "file_count": len(files)
                })
    
    return {"topics": topics, "total": len(topics)}


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    import os

    # Make bind address configurable, default to loopback for security
    host = os.getenv("BIND_HOST", "127.0.0.1")  # nosec B104

    uvicorn.run("main:app", host=host, port=8000, reload=True, log_level="info")
