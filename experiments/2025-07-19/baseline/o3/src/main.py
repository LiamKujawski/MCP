"""
Main FastAPI application for o3 ChatGPT Agent implementation.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import asyncio
from contextlib import asynccontextmanager

from src.core.base_agent import (
    AgentConfig, PlannerAgent, ExecutorAgent, 
    VerifierAgent, TaskResult
)


class TaskRequest(BaseModel):
    """Request model for task submission."""
    objective: str
    steps: List[str] = []
    dependencies: List[str] = []
    safety_critical: bool = False


class TaskResponse(BaseModel):
    """Response model for task execution."""
    success: bool
    plan: List[Dict[str, Any]] = []
    results: List[Dict[str, Any]] = []
    verification: Dict[str, Any] = {}
    execution_time: float = 0.0
    error: str = None


# Global agent instances
agents = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup."""
    # Initialize agents
    agents["planner"] = PlannerAgent(AgentConfig(
        name="main_planner",
        capabilities=["planning", "decomposition", "optimization"]
    ))
    
    agents["executor"] = ExecutorAgent(AgentConfig(
        name="main_executor", 
        capabilities=["execution", "tool_use", "parallel_processing"]
    ))
    
    agents["verifier"] = VerifierAgent(AgentConfig(
        name="main_verifier",
        capabilities=["verification", "validation", "quality_assurance"]
    ))
    
    yield
    
    # Cleanup
    agents.clear()


app = FastAPI(
    title="ChatGPT Agent - O3 Implementation",
    description="Multi-agent orchestration system based on o3 research synthesis",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "ChatGPT Agent - O3 Implementation",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": {
            name: "active" for name in agents.keys()
        }
    }


@app.post("/tasks", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """Execute a task through the agent pipeline."""
    try:
        # Phase 1: Planning
        planner = agents.get("planner")
        if not planner:
            raise HTTPException(status_code=500, detail="Planner agent not initialized")
            
        task_dict = {
            "objective": request.objective,
            "steps": request.steps,
            "dependencies": request.dependencies,
            "safety_critical": request.safety_critical
        }
        
        plan_result = await planner.process({"task": task_dict})
        
        if not plan_result.success:
            return TaskResponse(
                success=False,
                error=plan_result.error or "Planning failed"
            )
        
        # Phase 2: Execution
        executor = agents.get("executor")
        if not executor:
            raise HTTPException(status_code=500, detail="Executor agent not initialized")
            
        exec_result = await executor.process({"plan": plan_result.data["plan"]})
        
        if not exec_result.success:
            return TaskResponse(
                success=False,
                plan=plan_result.data["plan"],
                error=exec_result.error or "Execution failed"
            )
        
        # Phase 3: Verification
        verifier = agents.get("verifier")
        if not verifier:
            raise HTTPException(status_code=500, detail="Verifier agent not initialized")
            
        verify_result = await verifier.process({"results": exec_result.data["results"]})
        
        # Calculate total execution time
        total_time = (
            plan_result.execution_time + 
            exec_result.execution_time + 
            verify_result.execution_time
        )
        
        return TaskResponse(
            success=verify_result.success,
            plan=plan_result.data["plan"],
            results=exec_result.data["results"],
            verification=verify_result.data,
            execution_time=total_time,
            error=verify_result.error if not verify_result.success else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents")
async def list_agents():
    """List all active agents."""
    return {
        "agents": [
            {
                "name": agent.config.name,
                "capabilities": agent.config.capabilities,
                "type": type(agent).__name__
            }
            for agent in agents.values()
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Get system metrics."""
    # In a real implementation, this would connect to Prometheus
    return {
        "total_tasks": 0,
        "successful_tasks": 0,
        "failed_tasks": 0,
        "average_execution_time": 0.0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 