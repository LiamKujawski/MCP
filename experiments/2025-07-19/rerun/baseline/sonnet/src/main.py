"""
Main FastAPI application for Claude-4-Sonnet ChatGPT Agent implementation.
Emphasizes holistic integration and multi-model synthesis.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
from contextlib import asynccontextmanager
import structlog
from datetime import datetime

from src.agents.multi_model_agent import (
    ResearchSynthesizer, ImplementationAgent,
    QualityAssuranceAgent, ModelPerspective
)


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class ResearchRequest(BaseModel):
    """Request model for research synthesis."""
    domain: str
    synthesis_type: str = "comprehensive"
    models: List[str] = ["o3", "claude-4-sonnet", "claude-4-opus"]


class ImplementationRequest(BaseModel):
    """Request model for implementation tasks."""
    phase: str = "foundation"
    config: Dict[str, Any] = {}


class QARequest(BaseModel):
    """Request model for quality assurance."""
    qa_type: str = "comprehensive"
    targets: List[str] = []


class AgentResponse(BaseModel):
    """Unified response model for all agents."""
    agent_type: str
    task_type: str
    status: str
    results: Dict[str, Any]
    execution_time: float
    timestamp: str


# Global agent registry
agents = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup."""
    logger.info("Initializing ChatGPT Agent - Sonnet Implementation")
    
    # Initialize agents with holistic approach
    agents["research_synthesizer"] = ResearchSynthesizer("main_synthesizer")
    agents["implementation"] = ImplementationAgent("main_implementation")
    agents["quality_assurance"] = QualityAssuranceAgent("main_qa")
    
    # Load research data (in production, this would come from a database)
    research_data = {
        "chatgpt-agent": {},
        "codebase-generation": {}
    }
    
    # Digest research on startup
    await agents["research_synthesizer"].digest_research(research_data)
    
    logger.info("All agents initialized successfully")
    
    yield
    
    # Cleanup
    logger.info("Shutting down agents")
    agents.clear()


app = FastAPI(
    title="ChatGPT Agent - Claude-4-Sonnet Implementation",
    description="Holistic multi-model agent system with comprehensive integration",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "ChatGPT Agent - Claude-4-Sonnet Implementation",
        "version": "1.0.0",
        "approach": "Holistic multi-model integration",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": {}
    }
    
    for name, agent in agents.items():
        health_status["agents"][name] = {
            "type": type(agent).__name__,
            "status": "active",
            "knowledge_insights": len(agent.knowledge_graph.insights)
        }
    
    return health_status


@app.post("/research/synthesize", response_model=AgentResponse)
async def synthesize_research(request: ResearchRequest):
    """Synthesize research from multiple models."""
    start_time = datetime.utcnow()
    
    try:
        synthesizer = agents.get("research_synthesizer")
        if not synthesizer:
            raise HTTPException(status_code=500, detail="Research synthesizer not initialized")
        
        # Execute synthesis
        result = await synthesizer.execute_task({
            "type": request.synthesis_type,
            "domain": request.domain,
            "models": request.models
        })
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return AgentResponse(
            agent_type="ResearchSynthesizer",
            task_type=request.synthesis_type,
            status="completed",
            results=result,
            execution_time=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Research synthesis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/implementation/execute", response_model=AgentResponse)
async def execute_implementation(request: ImplementationRequest):
    """Execute implementation phase."""
    start_time = datetime.utcnow()
    
    try:
        implementation = agents.get("implementation")
        if not implementation:
            raise HTTPException(status_code=500, detail="Implementation agent not initialized")
        
        # Execute implementation phase
        result = await implementation.execute_task({
            "phase": request.phase,
            "config": request.config
        })
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return AgentResponse(
            agent_type="ImplementationAgent",
            task_type=request.phase,
            status=result.get("status", "unknown"),
            results=result,
            execution_time=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Implementation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/qa/validate", response_model=AgentResponse)
async def validate_quality(request: QARequest):
    """Perform quality assurance validation."""
    start_time = datetime.utcnow()
    
    try:
        qa_agent = agents.get("quality_assurance")
        if not qa_agent:
            raise HTTPException(status_code=500, detail="QA agent not initialized")
        
        # Execute QA validation
        result = await qa_agent.execute_task({
            "type": request.qa_type,
            "targets": request.targets
        })
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        return AgentResponse(
            agent_type="QualityAssuranceAgent",
            task_type=request.qa_type,
            status="passed" if result.get("overall_status") == "passed" else "failed",
            results=result,
            execution_time=execution_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"QA validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pipeline/execute")
async def execute_full_pipeline(background_tasks: BackgroundTasks):
    """Execute full agent pipeline asynchronously."""
    pipeline_id = f"pipeline_{datetime.utcnow().timestamp()}"
    
    # Add to background tasks
    background_tasks.add_task(run_pipeline, pipeline_id)
    
    return {
        "pipeline_id": pipeline_id,
        "status": "started",
        "message": "Pipeline execution started in background"
    }


async def run_pipeline(pipeline_id: str):
    """Run the full agent pipeline."""
    logger.info(f"Starting pipeline: {pipeline_id}")
    
    try:
        # Phase 1: Research synthesis
        synthesizer = agents["research_synthesizer"]
        synthesis = await synthesizer.execute_task({"type": "comprehensive"})
        
        # Phase 2: Implementation (all phases)
        implementation = agents["implementation"]
        for phase in ["foundation", "integration", "enhancement"]:
            await implementation.execute_task({"phase": phase})
        
        # Phase 3: Quality assurance
        qa = agents["quality_assurance"]
        qa_result = await qa.execute_task({"type": "comprehensive"})
        
        logger.info(f"Pipeline {pipeline_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline {pipeline_id} failed: {str(e)}")


@app.get("/agents")
async def list_agents():
    """List all active agents and their capabilities."""
    agent_info = []
    
    for name, agent in agents.items():
        info = {
            "name": name,
            "type": type(agent).__name__,
            "knowledge_insights": len(agent.knowledge_graph.insights),
            "convergent_patterns": len(agent.knowledge_graph.convergent_patterns),
            "divergent_approaches": len(agent.knowledge_graph.divergent_approaches)
        }
        agent_info.append(info)
    
    return {"agents": agent_info}


@app.get("/knowledge/insights")
async def get_knowledge_insights(category: Optional[str] = None):
    """Get knowledge insights from research synthesis."""
    synthesizer = agents.get("research_synthesizer")
    if not synthesizer:
        raise HTTPException(status_code=500, detail="Research synthesizer not initialized")
    
    insights = synthesizer.knowledge_graph.insights
    
    if category:
        insights = [i for i in insights if i.category == category]
    
    return {
        "total_insights": len(insights),
        "insights": [
            {
                "model": i.model.value,
                "category": i.category,
                "insight": i.insight,
                "confidence": i.confidence,
                "convergent": i.convergent
            }
            for i in insights
        ]
    }


@app.get("/metrics")
async def get_metrics():
    """Get system metrics."""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_count": len(agents),
        "total_insights": sum(
            len(agent.knowledge_graph.insights) 
            for agent in agents.values()
        ),
        "convergent_patterns": sum(
            len(agent.knowledge_graph.convergent_patterns)
            for agent in agents.values()
        )
    }


def main():
    """Main entry point for console script."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main() 