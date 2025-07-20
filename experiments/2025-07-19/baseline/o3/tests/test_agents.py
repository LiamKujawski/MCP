"""
Test suite for o3 agent implementation.
Tests hierarchical planning and multi-agent orchestration.
"""

import pytest
import asyncio
from src.core.base_agent import (
    AgentConfig, PlannerAgent, ExecutorAgent, 
    VerifierAgent, TaskResult
)


@pytest.fixture
def planner_config():
    """Configuration for planner agent."""
    return AgentConfig(
        name="test_planner",
        capabilities=["planning", "decomposition"],
        memory_size=1000
    )


@pytest.fixture
def executor_config():
    """Configuration for executor agent."""
    return AgentConfig(
        name="test_executor",
        capabilities=["execution", "tool_use"],
        memory_size=1000
    )


@pytest.fixture
def verifier_config():
    """Configuration for verifier agent."""
    return AgentConfig(
        name="test_verifier",
        capabilities=["verification", "validation"],
        memory_size=1000
    )


@pytest.mark.asyncio
async def test_planner_agent_simple_task(planner_config):
    """Test planner agent with simple task."""
    agent = PlannerAgent(planner_config)
    
    task = {
        "objective": "Test simple task",
        "steps": ["Step 1", "Step 2"]
    }
    
    result = await agent.process({"task": task})
    
    assert result.success is True
    assert "plan" in result.data
    assert len(result.data["plan"]) > 0


@pytest.mark.asyncio
async def test_planner_agent_complex_task(planner_config):
    """Test planner agent with complex task."""
    agent = PlannerAgent(planner_config)
    
    task = {
        "objective": "Complex multi-step task",
        "steps": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
        "dependencies": ["external_api", "database"],
        "safety_critical": True
    }
    
    result = await agent.process({"task": task})
    
    assert result.success is True
    assert "plan" in result.data
    plan = result.data["plan"]
    
    # Should decompose into subtasks
    assert len(plan) > 3
    
    # Should have planning task first
    assert plan[0]["type"] == "planning"
    
    # Should have verification task last
    assert plan[-1]["type"] == "verification"


@pytest.mark.asyncio
async def test_executor_agent(executor_config):
    """Test executor agent."""
    agent = ExecutorAgent(executor_config)
    
    plan = [
        {"type": "planning", "objective": "Plan task", "dependencies": []},
        {"type": "execution", "objective": "Execute step 1", "dependencies": [0]},
        {"type": "execution", "objective": "Execute step 2", "dependencies": [0]},
        {"type": "verification", "objective": "Verify results", "dependencies": [1, 2]}
    ]
    
    result = await agent.process({"plan": plan})
    
    assert result.success is True
    assert "results" in result.data
    assert len(result.data["results"]) == len(plan)


@pytest.mark.asyncio
async def test_verifier_agent(verifier_config):
    """Test verifier agent."""
    agent = VerifierAgent(verifier_config)
    
    results = [
        {"success": True, "output": "Task 1 completed"},
        {"success": True, "output": "Task 2 completed"},
        {"success": False, "output": "Task 3 failed"}
    ]
    
    result = await agent.process({"results": results})
    
    assert result.success is False  # One task failed
    assert "verifications" in result.data
    assert len(result.data["verifications"]) == 3


@pytest.mark.asyncio
async def test_full_agent_pipeline(planner_config, executor_config, verifier_config):
    """Test full agent pipeline from planning to verification."""
    planner = PlannerAgent(planner_config)
    executor = ExecutorAgent(executor_config)
    verifier = VerifierAgent(verifier_config)
    
    # Step 1: Planning
    task = {
        "objective": "Complete end-to-end task",
        "steps": ["Initialize", "Process data", "Generate report"]
    }
    
    plan_result = await planner.process({"task": task})
    assert plan_result.success is True
    
    # Step 2: Execution
    exec_result = await executor.process({"plan": plan_result.data["plan"]})
    assert exec_result.success is True
    
    # Step 3: Verification
    verify_result = await verifier.process({"results": exec_result.data["results"]})
    assert verify_result.success is True


@pytest.mark.asyncio
async def test_agent_error_handling(planner_config):
    """Test agent error handling."""
    agent = PlannerAgent(planner_config)
    
    # Invalid input
    result = await agent.process({})
    
    assert result.success is True  # Should handle gracefully
    assert "plan" in result.data


@pytest.mark.asyncio
async def test_task_decomposition(planner_config):
    """Test task decomposition logic."""
    agent = PlannerAgent(planner_config)
    
    # Simple task should not be decomposed
    simple_task = {"objective": "Simple task"}
    simple_plan = await agent.plan(simple_task)
    assert len(simple_plan) == 1
    
    # Complex task should be decomposed
    complex_task = {
        "objective": "Complex task",
        "steps": ["A", "B", "C", "D", "E", "F"],
        "dependencies": ["API", "DB"],
        "safety_critical": True
    }
    complex_plan = await agent.plan(complex_task)
    assert len(complex_plan) > 3


@pytest.mark.asyncio
async def test_dependency_resolution(planner_config):
    """Test dependency resolution in planning."""
    agent = PlannerAgent(planner_config)
    
    task = {
        "objective": "Task with dependencies",
        "steps": ["Setup", "Process", "Cleanup"]
    }
    
    plan = await agent.plan(task)
    
    # Check dependencies are properly set
    for i, subtask in enumerate(plan):
        if subtask["type"] == "execution":
            # Should depend on planning
            assert any(plan[dep]["type"] == "planning" for dep in subtask["dependencies"])
        elif subtask["type"] == "verification":
            # Should depend on all previous tasks
            assert len(subtask["dependencies"]) > 0


@pytest.mark.asyncio
async def test_memory_persistence(planner_config):
    """Test agent memory persistence."""
    agent = PlannerAgent(planner_config)
    
    # Process multiple tasks
    for i in range(3):
        task = {"objective": f"Task {i}"}
        result = await agent.process({"task": task})
        assert result.success is True
    
    # Agent should maintain state
    assert hasattr(agent, "memory")
    assert hasattr(agent, "state")


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 