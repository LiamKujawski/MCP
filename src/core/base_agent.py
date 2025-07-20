"""
Base agent implementation following o3's research synthesis approach.
Emphasizes hierarchical planning and multi-agent orchestration.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import asyncio
from dataclasses import dataclass
import logging
from datetime import datetime


@dataclass
class AgentConfig:
    """Configuration for agent initialization."""

    name: str
    capabilities: List[str]
    memory_size: int = 1000
    safety_level: str = "standard"


@dataclass
class TaskResult:
    """Result of a task execution."""

    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0


class BaseAgent(ABC):
    """
    Base agent incorporating insights from multi-model research.
    Implements o3's hierarchical task decomposition approach.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory = []
        self.state = {}
        self.logger = logging.getLogger(f"agent.{config.name}")

    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> TaskResult:
        """Process input according to agent's capabilities."""
        pass

    async def plan(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Hierarchical task planning following o3's approach.
        Decomposes complex tasks into executable subtasks.
        """
        subtasks = []

        # Analyze task complexity
        complexity = self._analyze_complexity(task)

        if complexity > 5:
            # Break down into smaller tasks
            subtasks = self._decompose_task(task)
        else:
            subtasks = [task]

        # Add dependencies
        for i, subtask in enumerate(subtasks):
            subtask["dependencies"] = self._identify_dependencies(subtask, subtasks[:i])

        return subtasks

    def _analyze_complexity(self, task: Dict[str, Any]) -> int:
        """Analyze task complexity on a scale of 1-10."""
        complexity = 1

        # Check for multiple steps
        if "steps" in task:
            complexity += len(task.get("steps", []))

        # Check for external dependencies
        if "dependencies" in task:
            complexity += 2

        # Check for safety requirements
        if task.get("safety_critical", False):
            complexity += 3

        return min(complexity, 10)

    def _decompose_task(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose complex task into subtasks."""
        subtasks = []

        # Extract main objective
        objective = task.get("objective", "")

        # Create planning subtask
        subtasks.append(
            {
                "type": "planning",
                "objective": f"Create detailed plan for: {objective}",
                "priority": 1,
            }
        )

        # Create execution subtasks
        for i, step in enumerate(task.get("steps", [])):
            subtasks.append({"type": "execution", "objective": step, "priority": i + 2})

        # Create verification subtask
        subtasks.append(
            {
                "type": "verification",
                "objective": f"Verify completion of: {objective}",
                "priority": len(subtasks) + 1,
            }
        )

        return subtasks

    def _identify_dependencies(
        self, subtask: Dict[str, Any], previous_tasks: List[Dict[str, Any]]
    ) -> List[int]:
        """Identify task dependencies."""
        dependencies = []

        # Planning tasks have no dependencies
        if subtask.get("type") == "planning":
            return dependencies

        # Execution tasks depend on planning
        if subtask.get("type") == "execution":
            for i, prev in enumerate(previous_tasks):
                if prev.get("type") == "planning":
                    dependencies.append(i)

        # Verification depends on all execution tasks
        if subtask.get("type") == "verification":
            for i, prev in enumerate(previous_tasks):
                if prev.get("type") in ["planning", "execution"]:
                    dependencies.append(i)

        return dependencies


class PlannerAgent(BaseAgent):
    """Agent specialized in task planning and decomposition."""

    async def process(self, input_data: Dict[str, Any]) -> TaskResult:
        """Process planning request."""
        start_time = datetime.now()

        try:
            # Extract task from input
            task = input_data.get("task", {})

            # Create execution plan
            plan = await self.plan(task)

            # Validate plan
            if not self._validate_plan(plan):
                return TaskResult(
                    success=False, data=None, error="Invalid plan generated"
                )

            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                success=True, data={"plan": plan}, execution_time=execution_time
            )

        except Exception as e:
            self.logger.error(f"Planning failed: {str(e)}")
            return TaskResult(success=False, data=None, error=str(e))

    def _validate_plan(self, plan: List[Dict[str, Any]]) -> bool:
        """Validate generated plan."""
        if not plan:
            return False

        # Check for circular dependencies
        for i, task in enumerate(plan):
            deps = task.get("dependencies", [])
            if i in deps:
                return False

        return True


class ExecutorAgent(BaseAgent):
    """Agent specialized in task execution."""

    async def process(self, input_data: Dict[str, Any]) -> TaskResult:
        """Execute task based on plan."""
        start_time = datetime.now()

        try:
            plan = input_data.get("plan", [])
            results = []

            # Execute tasks in order respecting dependencies
            for task in plan:
                # Wait for dependencies
                await self._wait_for_dependencies(task, results)

                # Execute task
                result = await self._execute_task(task)
                results.append(result)

            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                success=all(r["success"] for r in results),
                data={"results": results},
                execution_time=execution_time,
            )

        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            return TaskResult(success=False, data=None, error=str(e))

    async def _wait_for_dependencies(
        self, task: Dict[str, Any], results: List[Dict[str, Any]]
    ) -> None:
        """Wait for task dependencies to complete."""
        dependencies = task.get("dependencies", [])

        for dep_idx in dependencies:
            if dep_idx < len(results):
                # Dependency already completed
                continue
            else:
                # Wait a bit for dependency
                await asyncio.sleep(0.1)

    async def _execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute individual task."""
        # Simulate task execution
        await asyncio.sleep(0.1)

        return {
            "task": task,
            "success": True,
            "output": f"Completed: {task.get('objective', 'Unknown task')}",
        }


class VerifierAgent(BaseAgent):
    """Agent specialized in result verification."""

    async def process(self, input_data: Dict[str, Any]) -> TaskResult:
        """Verify task execution results."""
        start_time = datetime.now()

        try:
            results = input_data.get("results", [])
            verification_results = []

            for result in results:
                verified = self._verify_result(result)
                verification_results.append(verified)

            execution_time = (datetime.now() - start_time).total_seconds()

            return TaskResult(
                success=all(v["passed"] for v in verification_results),
                data={"verifications": verification_results},
                execution_time=execution_time,
            )

        except Exception as e:
            self.logger.error(f"Verification failed: {str(e)}")
            return TaskResult(success=False, data=None, error=str(e))

    def _verify_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Verify individual result."""
        # Check if result indicates success
        success = result.get("success", False)

        # Check if output exists
        has_output = "output" in result

        return {
            "result": result,
            "passed": success and has_output,
            "checks": {"success_flag": success, "has_output": has_output},
        }
