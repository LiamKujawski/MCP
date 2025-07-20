"""
Test suite for Claude-4-Opus unified agent implementation.
Tests practical implementation with comprehensive integration.
"""

import pytest
import asyncio
from datetime import datetime
from src.unified_agent import (
    AgentCapability, TaskContext, ExecutionResult,
    AgentFactory, PlannerAgent, ExecutorAgent,
    ValidatorAgent, SynthesizerAgent
)


@pytest.fixture
def agent_factory():
    """Create agent factory."""
    return AgentFactory()


@pytest.fixture
def planner_capabilities():
    """Planner agent capabilities."""
    return [
        AgentCapability(
            name="task_decomposition",
            description="Decompose complex tasks",
            required_tools=["analyzer"],
            confidence=0.95
        ),
        AgentCapability(
            name="dependency_analysis",
            description="Analyze task dependencies",
            required_tools=["graph_analyzer"],
            confidence=0.9
        )
    ]


@pytest.fixture
def executor_capabilities():
    """Executor agent capabilities."""
    return [
        AgentCapability(
            name="task_execution",
            description="Execute planned tasks",
            required_tools=["runtime"],
            confidence=0.95
        ),
        AgentCapability(
            name="parallel_processing",
            description="Execute tasks in parallel",
            required_tools=["thread_pool"],
            confidence=0.85
        )
    ]


@pytest.mark.asyncio
async def test_agent_factory_creation(agent_factory):
    """Test agent creation via factory."""
    planner = agent_factory.create_agent(
        "planner",
        "test_planner",
        [AgentCapability("planning", "Plan tasks", [], 0.9)]
    )
    
    assert isinstance(planner, PlannerAgent)
    assert planner.name == "test_planner"
    assert len(planner.capabilities) == 1


@pytest.mark.asyncio
async def test_planner_agent_execution(planner_capabilities):
    """Test planner agent task execution."""
    planner = PlannerAgent("test_planner", planner_capabilities)
    
    context = TaskContext(
        task_id="test_001",
        objective="Create comprehensive test plan",
        requirements={
            "test_coverage": "90%",
            "test_types": ["unit", "integration", "e2e"]
        },
        constraints={"time_limit": "2 hours"},
        priority=8
    )
    
    result = await planner.process_task(context)
    
    assert result.success is True
    assert result.task_id == "test_001"
    assert "plan" in result.output
    assert len(result.output["steps"]) > 0
    assert result.execution_time > 0


@pytest.mark.asyncio
async def test_executor_agent_with_plan(executor_capabilities):
    """Test executor agent with execution plan."""
    executor = ExecutorAgent("test_executor", executor_capabilities)
    
    # Create a plan
    plan = {
        "task_id": "test_002",
        "steps": [
            {"step_id": "step_0", "name": "Initialize", "type": "setup"},
            {"step_id": "step_1", "name": "Process", "type": "execution"},
            {"step_id": "step_2", "name": "Cleanup", "type": "teardown"}
        ]
    }
    
    context = TaskContext(
        task_id="test_002",
        objective="Execute test plan",
        requirements={"plan": plan},
        constraints={},
        priority=7
    )
    
    result = await executor.process_task(context)
    
    assert result.success is True
    assert result.output["status"] == "completed"
    assert len(result.output["results"]) == 3
    assert all(r["status"] == "success" for r in result.output["results"])


@pytest.mark.asyncio
async def test_validator_agent(agent_factory):
    """Test validator agent."""
    validator = agent_factory.create_agent(
        "validator",
        "test_validator",
        [AgentCapability("validation", "Validate results", [], 0.95)]
    )
    
    # Create test results to validate
    results = [
        {"step_id": "step_1", "status": "success", "output": "Data processed"},
        {"step_id": "step_2", "status": "success", "output": "Report generated"},
        {"step_id": "step_3", "status": "failed", "output": None}
    ]
    
    context = TaskContext(
        task_id="test_003",
        objective="Validate execution results",
        requirements={"results": results},
        constraints={}
    )
    
    result = await validator.process_task(context)
    
    assert result.success is True
    assert result.output["all_valid"] is False  # One step failed
    assert len(result.output["validations"]) == 3
    assert result.output["validations"][2]["valid"] is False


@pytest.mark.asyncio
async def test_synthesizer_agent(agent_factory):
    """Test synthesizer agent."""
    synthesizer = agent_factory.create_agent(
        "synthesizer",
        "test_synthesizer",
        [AgentCapability("synthesis", "Synthesize information", [], 0.9)]
    )
    
    # Create test sources
    sources = [
        {"id": "source_1", "type": "research", "quality": 0.9, "findings": 5},
        {"id": "source_2", "type": "analysis", "quality": 0.85, "findings": 3},
        {"id": "source_3", "type": "research", "quality": 0.95, "findings": 7}
    ]
    
    context = TaskContext(
        task_id="test_004",
        objective="Synthesize research findings",
        requirements={"sources": sources},
        constraints={}
    )
    
    result = await synthesizer.process_task(context)
    
    assert result.success is True
    assert result.output["total_sources"] == 3
    assert result.output["total_insights"] > 0
    assert len(result.output["patterns"]) > 0
    assert "summary" in result.output


@pytest.mark.asyncio
async def test_full_agent_pipeline(agent_factory):
    """Test full agent pipeline execution."""
    # Create agents
    planner = agent_factory.create_agent(
        "planner",
        "pipeline_planner",
        [AgentCapability("planning", "Plan tasks", [], 0.95)]
    )
    
    executor = agent_factory.create_agent(
        "executor",
        "pipeline_executor",
        [AgentCapability("execution", "Execute tasks", [], 0.95)]
    )
    
    validator = agent_factory.create_agent(
        "validator",
        "pipeline_validator",
        [AgentCapability("validation", "Validate results", [], 0.95)]
    )
    
    # Step 1: Planning
    plan_context = TaskContext(
        task_id="pipeline_001",
        objective="Complete data processing pipeline",
        requirements={"data_size": "1GB", "format": "JSON"},
        constraints={"memory_limit": "4GB"}
    )
    
    plan_result = await planner.process_task(plan_context)
    assert plan_result.success is True
    
    # Step 2: Execution
    exec_context = TaskContext(
        task_id="pipeline_002",
        objective="Execute pipeline plan",
        requirements={"plan": plan_result.output},
        constraints={}
    )
    
    exec_result = await executor.process_task(exec_context)
    assert exec_result.success is True
    
    # Step 3: Validation
    val_context = TaskContext(
        task_id="pipeline_003",
        objective="Validate pipeline results",
        requirements={"results": exec_result.output["results"]},
        constraints={}
    )
    
    val_result = await validator.process_task(val_context)
    assert val_result.success is True
    assert val_result.output["all_valid"] is True


@pytest.mark.asyncio
async def test_agent_metrics_tracking():
    """Test agent metrics tracking."""
    agent = PlannerAgent("metrics_test", [
        AgentCapability("planning", "Plan tasks", [], 0.9)
    ])
    
    # Process multiple tasks
    for i in range(3):
        context = TaskContext(
            task_id=f"metric_test_{i}",
            objective=f"Task {i}",
            requirements={},
            constraints={}
        )
        await agent.process_task(context)
    
    # Check metrics
    assert agent.metrics["tasks_processed"] == 3
    assert agent.metrics["average_execution_time"] > 0


@pytest.mark.asyncio
async def test_capability_matching():
    """Test capability matching for tasks."""
    agent = ExecutorAgent("capability_test", [
        AgentCapability("data_processing", "Process data", ["pandas"], 0.9),
        AgentCapability("report_generation", "Generate reports", ["matplotlib"], 0.85)
    ])
    
    # Task requiring data processing
    context = TaskContext(
        task_id="cap_test_001",
        objective="Process data and generate visualization",
        requirements={},
        constraints={}
    )
    
    result = await agent.process_task(context)
    
    # Should succeed as agent has required capabilities
    assert result.success is True


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in agents."""
    agent = ExecutorAgent("error_test", [])
    
    # Context with no plan
    context = TaskContext(
        task_id="error_001",
        objective="Execute without plan",
        requirements={},  # No plan provided
        constraints={}
    )
    
    result = await agent.process_task(context)
    
    # Should handle gracefully
    assert result.success is True
    assert "error" in result.output


@pytest.mark.asyncio
async def test_memory_persistence():
    """Test agent memory persistence."""
    planner = PlannerAgent("memory_test", [
        AgentCapability("planning", "Plan tasks", [], 0.9)
    ])
    
    context = TaskContext(
        task_id="memory_001",
        objective="Create plan with memory",
        requirements={"steps": 3},
        constraints={}
    )
    
    result = await planner.process_task(context)
    
    # Check memory storage
    assert f"plan_{context.task_id}" in planner.memory
    assert planner.memory[f"plan_{context.task_id}"]["task_id"] == context.task_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 