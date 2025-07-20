"""
Σ-Builder FastAPI Application - O3 Prompt via Opus Model
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from unified_sigma_agent import (
    UnifiedΣAgent,
    ΣTaskRequest,
    ΣTaskResponse,
    WorkflowPhase,
    process_sigma_task
)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    print("Initializing Unified Σ-Builder application...")
    app.state.agent = UnifiedΣAgent()
    app.state.active_workflows = {}
    yield
    print("Shutting down Unified Σ-Builder application...")


# Create FastAPI app
app = FastAPI(
    title="Σ-Builder Unified Implementation",
    description="O3 Prompt interpreted through Opus's unified approach",
    version="1.0.0",
    lifespan=lifespan
)


class WorkflowRequest(BaseModel):
    """Request to start a workflow"""
    description: str = Field(..., description="Workflow description")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class WorkflowResponse(BaseModel):
    """Response for workflow operations"""
    workflow_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    phases_executed: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Unified Σ-Builder API",
        "description": "O3 prompt through Opus's pragmatic unified approach",
        "implementation": "o3-prompt-opus-model",
        "workflow_phases": [phase.value for phase in WorkflowPhase],
        "endpoints": {
            "/workflow/execute": "Execute complete workflow",
            "/workflow/{workflow_id}": "Get workflow status",
            "/metrics": "Get system metrics",
            "/health": "Health check"
        },
        "characteristics": {
            "approach": "Unified single-agent",
            "execution": "All phases in one workflow",
            "focus": "Pragmatic end-to-end processing"
        }
    }


@app.post("/workflow/execute", response_model=ΣTaskResponse)
async def execute_workflow(request: WorkflowRequest):
    """Execute the complete Σ-Builder workflow"""
    task_request = ΣTaskRequest(
        description=request.description,
        config=request.config
    )
    
    # Store workflow info
    workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    app.state.active_workflows[workflow_id] = {
        "status": "running",
        "start_time": datetime.now()
    }
    
    # Execute workflow
    response = await process_sigma_task(task_request)
    
    # Update workflow info
    app.state.active_workflows[workflow_id].update({
        "status": response.status,
        "end_time": datetime.now(),
        "result": response.result
    })
    
    return response


@app.get("/workflow/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow_status(workflow_id: str):
    """Get status of a specific workflow"""
    if workflow_id not in app.state.active_workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = app.state.active_workflows[workflow_id]
    
    return WorkflowResponse(
        workflow_id=workflow_id,
        status=workflow["status"],
        start_time=workflow["start_time"],
        end_time=workflow.get("end_time"),
        phases_executed=workflow.get("result", {}).get("phases_executed"),
        metrics=workflow.get("result", {}).get("metrics")
    )


@app.get("/metrics")
async def get_metrics():
    """Get system metrics"""
    total_workflows = len(app.state.active_workflows)
    completed = sum(1 for w in app.state.active_workflows.values() if w["status"] == "completed")
    failed = sum(1 for w in app.state.active_workflows.values() if w["status"] == "failed")
    running = sum(1 for w in app.state.active_workflows.values() if w["status"] == "running")
    
    # Aggregate metrics from completed workflows
    all_metrics = []
    for workflow in app.state.active_workflows.values():
        if workflow.get("result", {}).get("metrics"):
            all_metrics.append(workflow["result"]["metrics"])
    
    avg_insights = sum(m.get("insights_extracted", 0) for m in all_metrics) / len(all_metrics) if all_metrics else 0
    avg_files = sum(m.get("files_processed", 0) for m in all_metrics) / len(all_metrics) if all_metrics else 0
    
    return {
        "workflows": {
            "total": total_workflows,
            "completed": completed,
            "failed": failed,
            "running": running
        },
        "performance": {
            "avg_insights_per_workflow": avg_insights,
            "avg_files_per_workflow": avg_files,
            "success_rate": completed / total_workflows if total_workflows > 0 else 0
        },
        "system": {
            "implementation": "unified-agent",
            "uptime": datetime.now().isoformat()
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "implementation": "o3-prompt-opus-model",
        "agent_type": "unified",
        "active_workflows": len([w for w in app.state.active_workflows.values() if w["status"] == "running"])
    }


@app.post("/simulate")
async def simulate_workflow():
    """Simulate a workflow execution for testing"""
    request = WorkflowRequest(
        description="Simulated Σ-Builder workflow",
        config={"simulation": True}
    )
    
    return await execute_workflow(request)


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle value errors"""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 