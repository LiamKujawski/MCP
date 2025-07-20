"""
Main FastAPI application for Claude-4-Opus ChatGPT Agent implementation.
Emphasizes practical unified agent system with comprehensive capabilities.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from contextlib import asynccontextmanager
import logging
from datetime import datetime
import uuid

from src.unified_agent import (
    AgentFactory, AgentCapability, TaskContext,
    ExecutionResult
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskRequest(BaseModel):
    """Request model for task submission."""
    objective: str
    requirements: Dict[str, Any] = {}
    constraints: Dict[str, Any] = {}
    priority: int = 5
    agent_type: str = "planner"


class PipelineRequest(BaseModel):
    """Request model for pipeline execution."""
    name: str
    stages: List[Dict[str, Any]]
    parallel: bool = False


class AgentCapabilityRequest(BaseModel):
    """Request model for agent capabilities."""
    name: str
    description: str
    required_tools: List[str] = []
    confidence: float = 0.9


class TaskStatusResponse(BaseModel):
    """Response model for task status."""
    task_id: str
    status: str
    result: Optional[ExecutionResult] = None
    error: Optional[str] = None
    timestamp: str


# Global registry
agent_factory = AgentFactory()
active_agents = {}
task_results = {}


def create_default_agents():
    """Create default agents with standard capabilities."""
    # Planner agent
    planner_caps = [
        AgentCapability("task_decomposition", "Decompose complex tasks", ["analyzer"], 0.95),
        AgentCapability("dependency_analysis", "Analyze dependencies", ["graph_tool"], 0.9),
        AgentCapability("time_estimation", "Estimate execution time", ["predictor"], 0.85)
    ]
    active_agents["default_planner"] = agent_factory.create_agent(
        "planner", "default_planner", planner_caps
    )
    
    # Executor agent
    executor_caps = [
        AgentCapability("task_execution", "Execute planned tasks", ["runtime"], 0.95),
        AgentCapability("parallel_processing", "Parallel execution", ["thread_pool"], 0.9),
        AgentCapability("error_recovery", "Recover from errors", ["retry_handler"], 0.85)
    ]
    active_agents["default_executor"] = agent_factory.create_agent(
        "executor", "default_executor", executor_caps
    )
    
    # Validator agent
    validator_caps = [
        AgentCapability("result_validation", "Validate results", ["validator"], 0.95),
        AgentCapability("quality_assurance", "QA checks", ["qa_tools"], 0.9)
    ]
    active_agents["default_validator"] = agent_factory.create_agent(
        "validator", "default_validator", validator_caps
    )
    
    # Synthesizer agent
    synthesizer_caps = [
        AgentCapability("information_synthesis", "Synthesize information", ["nlp_tools"], 0.9),
        AgentCapability("pattern_recognition", "Identify patterns", ["ml_tools"], 0.85)
    ]
    active_agents["default_synthesizer"] = agent_factory.create_agent(
        "synthesizer", "default_synthesizer", synthesizer_caps
    )
    
    logger.info(f"Created {len(active_agents)} default agents")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup."""
    logger.info("Initializing ChatGPT Agent - Opus Implementation")
    
    # Create default agents
    create_default_agents()
    
    logger.info("Application initialized successfully")
    
    yield
    
    # Cleanup
    logger.info("Shutting down application")
    active_agents.clear()
    task_results.clear()


app = FastAPI(
    title="ChatGPT Agent - Claude-4-Opus Implementation",
    description="Unified agent system with practical implementation focus",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "ChatGPT Agent - Claude-4-Opus Implementation",
        "version": "1.0.0",
        "approach": "Unified agent system with comprehensive synthesis",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_active": len(active_agents),
        "tasks_completed": len([r for r in task_results.values() if r.success])
    }


@app.post("/tasks/submit", response_model=TaskStatusResponse)
async def submit_task(request: TaskRequest):
    """Submit a task for processing."""
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    
    try:
        # Select agent
        agent_name = f"default_{request.agent_type}"
        agent = active_agents.get(agent_name)
        
        if not agent:
            raise HTTPException(
                status_code=400,
                detail=f"Agent type '{request.agent_type}' not available"
            )
        
        # Create task context
        context = TaskContext(
            task_id=task_id,
            objective=request.objective,
            requirements=request.requirements,
            constraints=request.constraints,
            priority=request.priority
        )
        
        # Process task
        result = await agent.process_task(context)
        
        # Store result
        task_results[task_id] = result
        
        return TaskStatusResponse(
            task_id=task_id,
            status="completed" if result.success else "failed",
            result=result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Task submission failed: {str(e)}")
        return TaskStatusResponse(
            task_id=task_id,
            status="error",
            error=str(e),
            timestamp=datetime.utcnow().isoformat()
        )


@app.get("/tasks/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get status of a submitted task."""
    result = task_results.get(task_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatusResponse(
        task_id=task_id,
        status="completed" if result.success else "failed",
        result=result,
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/pipeline/execute")
async def execute_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """Execute a multi-stage pipeline."""
    pipeline_id = f"pipeline_{uuid.uuid4().hex[:8]}"
    
    # Add to background tasks
    background_tasks.add_task(run_pipeline, pipeline_id, request)
    
    return {
        "pipeline_id": pipeline_id,
        "status": "started",
        "stages": len(request.stages),
        "message": "Pipeline execution started"
    }


async def run_pipeline(pipeline_id: str, request: PipelineRequest):
    """Run pipeline stages."""
    logger.info(f"Starting pipeline: {pipeline_id}")
    
    try:
        results = []
        
        for i, stage in enumerate(request.stages):
            logger.info(f"Executing stage {i+1}/{len(request.stages)}")
            
            # Create task context
            context = TaskContext(
                task_id=f"{pipeline_id}_stage_{i}",
                objective=stage.get("objective", f"Stage {i+1}"),
                requirements=stage.get("requirements", {}),
                constraints=stage.get("constraints", {}),
                priority=stage.get("priority", 5)
            )
            
            # Select agent
            agent_type = stage.get("agent_type", "executor")
            agent = active_agents.get(f"default_{agent_type}")
            
            if agent:
                result = await agent.process_task(context)
                results.append(result)
                
                # Pass results to next stage if needed
                if i < len(request.stages) - 1:
                    request.stages[i+1]["requirements"]["previous_result"] = result.output
        
        logger.info(f"Pipeline {pipeline_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline {pipeline_id} failed: {str(e)}")


@app.get("/agents")
async def list_agents():
    """List all active agents and their capabilities."""
    agents_info = []
    
    for name, agent in active_agents.items():
        info = {
            "name": name,
            "type": type(agent).__name__,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "confidence": cap.confidence
                }
                for cap in agent.capabilities.values()
            ],
            "metrics": agent.metrics
        }
        agents_info.append(info)
    
    return {"agents": agents_info}


@app.post("/agents/create")
async def create_agent(agent_type: str, name: str, capabilities: List[AgentCapabilityRequest]):
    """Create a new agent with specified capabilities."""
    try:
        # Convert capability requests to AgentCapability objects
        agent_caps = [
            AgentCapability(
                name=cap.name,
                description=cap.description,
                required_tools=cap.required_tools,
                confidence=cap.confidence
            )
            for cap in capabilities
        ]
        
        # Create agent
        agent = agent_factory.create_agent(agent_type, name, agent_caps)
        active_agents[name] = agent
        
        return {
            "status": "created",
            "agent_name": name,
            "agent_type": agent_type,
            "capabilities": len(agent_caps)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get system-wide metrics."""
    total_tasks = sum(agent.metrics["tasks_processed"] for agent in active_agents.values())
    avg_time = sum(
        agent.metrics["average_execution_time"] * agent.metrics["tasks_processed"]
        for agent in active_agents.values()
    ) / max(total_tasks, 1)
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "total_agents": len(active_agents),
        "total_tasks_processed": total_tasks,
        "average_execution_time": avg_time,
        "completed_tasks": len([r for r in task_results.values() if r.success]),
        "failed_tasks": len([r for r in task_results.values() if not r.success])
    }


@app.get("/tasks/results")
async def get_task_results(limit: int = 10):
    """Get recent task results."""
    # Get most recent results
    sorted_results = sorted(
        task_results.items(),
        key=lambda x: x[1].execution_time,
        reverse=True
    )[:limit]
    
    return {
        "results": [
            {
                "task_id": task_id,
                "success": result.success,
                "execution_time": result.execution_time,
                "metrics": result.metrics,
                "errors": result.errors
            }
            for task_id, result in sorted_results
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 