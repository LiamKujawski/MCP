"""
Σ-Builder Agent Implementation - O3 Prompt interpreted through Sonnet Model

This implementation synthesizes the o3 prompt's vision of a multi-model research
ingestion agent through Claude Sonnet's holistic and synthesis-focused approach.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import networkx as nx
from pydantic import BaseModel, Field

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchPerspective(Enum):
    """Model perspectives from research synthesis"""

    O3 = "o3"
    CLAUDE_4_SONNET = "claude-4-sonnet"
    CLAUDE_4_OPUS = "claude-4-opus"
    CURSOR = "cursor-agent"


class InsightType(Enum):
    """Types of insights extracted from research"""

    ARCHITECTURE = "architecture"
    SAFETY = "safety"
    PERFORMANCE = "performance"
    SCALABILITY = "scalability"
    PROMPT_ENGINEERING = "prompt_engineering"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


@dataclass
class ResearchInsight:
    """Represents an insight extracted from research"""

    id: str
    source_file: str
    perspective: ResearchPerspective
    type: InsightType
    content: str
    confidence: float = 1.0
    related_insights: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)


class KnowledgeGraph:
    """Multi-model knowledge graph for research synthesis"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.insights: Dict[str, ResearchInsight] = {}
        self.consensus_patterns: List[Dict[str, Any]] = []
        self.divergences: List[Dict[str, Any]] = []

    def add_insight(self, insight: ResearchInsight) -> None:
        """Add an insight to the knowledge graph"""
        self.insights[insight.id] = insight
        self.graph.add_node(insight.id, **insight.__dict__)

        # Connect related insights
        for related_id in insight.related_insights:
            if related_id in self.graph:
                self.graph.add_edge(insight.id, related_id)

    def identify_consensus(self) -> List[Dict[str, Any]]:
        """Identify consensus patterns across models"""
        type_clusters = {}
        for insight in self.insights.values():
            key = insight.type
            if key not in type_clusters:
                type_clusters[key] = []
            type_clusters[key].append(insight)

        consensus = []
        for insight_type, insights in type_clusters.items():
            if len({i.perspective for i in insights}) >= 2:
                consensus.append(
                    {
                        "type": insight_type.value,
                        "insights": [i.content for i in insights],
                        "perspectives": list({i.perspective.value for i in insights}),
                    }
                )

        self.consensus_patterns = consensus
        return consensus

    def identify_divergences(self) -> List[Dict[str, Any]]:
        """Identify valuable divergences across models"""
        perspective_unique = {}
        for insight in self.insights.values():
            if insight.perspective not in perspective_unique:
                perspective_unique[insight.perspective] = []
            perspective_unique[insight.perspective].append(insight)

        divergences = []
        for perspective, insights in perspective_unique.items():
            unique_types = set(i.type for i in insights)
            for other_perspective, other_insights in perspective_unique.items():
                if perspective != other_perspective:
                    other_types = set(i.type for i in other_insights)
                    unique_to_perspective = unique_types - other_types
                    if unique_to_perspective:
                        divergences.append(
                            {
                                "perspective": perspective.value,
                                "unique_focus": [
                                    t.value for t in unique_to_perspective
                                ],
                                "insights": [
                                    i.content
                                    for i in insights
                                    if i.type in unique_to_perspective
                                ],
                            }
                        )

        self.divergences = divergences
        return divergences


class ΣBuilderPhase(Enum):
    """Phases of the Σ-Builder workflow"""

    RESEARCH_DIGESTION = "research_digestion"
    SYNTHESIS_REPORT = "synthesis_report"
    IMPLEMENTATION_PLAN = "implementation_plan"
    CODEBASE_SETUP = "codebase_setup"
    DOCUMENTATION = "documentation"
    QUALITY_ASSURANCE = "quality_assurance"


class BaseΣAgent(ABC):
    """Base class for Σ-Builder agents"""

    def __init__(self, name: str, phase: ΣBuilderPhase):
        self.name = name
        self.phase = phase
        self.knowledge_graph = KnowledgeGraph()
        self.logger = logging.getLogger(f"{__name__}.{name}")

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's phase"""
        pass

    def log_progress(self, message: str, level: str = "info") -> None:
        """Log progress with structured format"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "phase": self.phase.value,
            "message": message,
        }
        getattr(self.logger, level)(json.dumps(log_data))


class ResearchDigestionAgent(BaseΣAgent):
    """Agent for Phase A: Research Digestion"""

    def __init__(self):
        super().__init__("ResearchDigestion", ΣBuilderPhase.RESEARCH_DIGESTION)
        self.research_dirs = [
            "chatgpt-agent-research",
            "codebase-generation-prompt-research",
        ]
        self.research_files = [
            "01_overview.md",
            "02_architecture-deep-dive.md",
            "03_codebase-setup.md",
            "04_prompt-structure.md",
            "05_enhancements.md",
        ]

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Digest all research files and build knowledge graph"""
        self.log_progress("Starting research digestion phase")

        insights_extracted = []
        files_processed = 0

        for research_dir in self.research_dirs:
            for model_dir in ["o3", "claude-4-sonnet", "claude-4-opus"]:
                dir_path = Path(research_dir) / model_dir

                for research_file in self.research_files:
                    file_path = dir_path / research_file
                    if file_path.exists():
                        insights = await self._process_research_file(
                            file_path,
                            ResearchPerspective[
                                model_dir.upper().replace("-", "_").replace("4_", "4_")
                            ],
                        )
                        insights_extracted.extend(insights)
                        files_processed += 1

        # Build knowledge graph
        for insight in insights_extracted:
            self.knowledge_graph.add_insight(insight)

        # Identify patterns
        consensus = self.knowledge_graph.identify_consensus()
        divergences = self.knowledge_graph.identify_divergences()

        self.log_progress(
            f"Processed {files_processed} files, extracted {len(insights_extracted)} insights"
        )

        # Convert knowledge graph to serializable format
        knowledge_graph_data = {
            "insights": {
                id: {
                    "id": insight.id,
                    "source_file": insight.source_file,
                    "perspective": insight.perspective.value,
                    "type": insight.type.value,
                    "content": insight.content,
                }
                for id, insight in self.knowledge_graph.insights.items()
            },
            "nodes_count": self.knowledge_graph.graph.number_of_nodes(),
            "edges_count": self.knowledge_graph.graph.number_of_edges(),
        }

        return {
            "knowledge_graph": knowledge_graph_data,
            "insights_count": len(insights_extracted),
            "files_processed": files_processed,
            "consensus_patterns": consensus,
            "divergences": divergences,
        }

    async def _process_research_file(
        self, file_path: Path, perspective: ResearchPerspective
    ) -> List[ResearchInsight]:
        """Process a single research file"""
        # Simulate processing
        await asyncio.sleep(0.1)

        # Extract insights based on file type
        file_name = file_path.name
        insights = []

        insight_mappings = {
            "01_overview.md": InsightType.ARCHITECTURE,
            "02_architecture-deep-dive.md": InsightType.ARCHITECTURE,
            "03_codebase-setup.md": InsightType.DEPLOYMENT,
            "04_prompt-structure.md": InsightType.PROMPT_ENGINEERING,
            "05_enhancements.md": InsightType.SCALABILITY,
        }

        insight_type = insight_mappings.get(file_name, InsightType.ARCHITECTURE)

        insight = ResearchInsight(
            id=f"{perspective.value}_{file_name}_{len(insights)}",
            source_file=str(file_path),
            perspective=perspective,
            type=insight_type,
            content=f"Synthesized insight from {file_name} - {perspective.value} perspective",
            confidence=0.95,
        )

        insights.append(insight)
        return insights


class SynthesisReportAgent(BaseΣAgent):
    """Agent for Phase B: Synthesis Report Generation"""

    def __init__(self):
        super().__init__("SynthesisReport", ΣBuilderPhase.SYNTHESIS_REPORT)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate synthesis report from knowledge graph"""
        self.log_progress("Generating synthesis report")

        # ensure self.context exists for legacy tests
        if not hasattr(self, "context"):
            self.context = context or {}

        knowledge_graph = context.get("knowledge_graph")
        if not knowledge_graph:
            raise ValueError("Knowledge graph not found in context")

        # Generate report sections
        # Handle dict representation from ResearchDigestionAgent
        if isinstance(knowledge_graph, dict):
            consensus_patterns = context.get("consensus_patterns", [])
            divergences = context.get("divergences", [])
        else:
            consensus_patterns = knowledge_graph.consensus_patterns
            divergences = knowledge_graph.divergences

        report_sections = {
            "executive_summary": self._generate_executive_summary(knowledge_graph),
            "model_viewpoints_matrix": self._generate_viewpoints_matrix(
                knowledge_graph
            ),
            "consensus_patterns": consensus_patterns,
            "valuable_divergences": divergences,
            "actionable_requirements": self._generate_requirements(knowledge_graph),
        }

        # Write report
        report_path = Path("analysis/00_cursor-agent-synthesis.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        await self._write_report(report_path, report_sections)

        self.log_progress(f"Synthesis report written to {report_path}")

        return {
            "report_path": str(report_path),
            "sections_generated": list(report_sections.keys()),
            **context,
        }

    def _generate_executive_summary(self, knowledge_graph: KnowledgeGraph) -> str:
        """Generate executive summary"""
        # Handle dict representation from ResearchDigestionAgent
        if isinstance(knowledge_graph, dict):
            insights_count = len(knowledge_graph.get("insights", {}))
            consensus_count = len(knowledge_graph.get("consensus_patterns", []))
            divergences_count = len(knowledge_graph.get("divergences", []))
        else:
            insights_count = len(knowledge_graph.insights)
            consensus_count = len(knowledge_graph.consensus_patterns)
            divergences_count = len(knowledge_graph.divergences)

        return f"""
# Executive Summary

Synthesized {insights_count} insights from multi-model research:
- Identified {consensus_count} consensus patterns
- Found {divergences_count} valuable divergences
- Key focus areas: Architecture, Safety, Performance, Scalability
"""

    def _generate_viewpoints_matrix(
        self, knowledge_graph: KnowledgeGraph
    ) -> Dict[str, List[str]]:
        """Generate model viewpoints matrix"""
        matrix = {}

        # Handle dict representation from ResearchDigestionAgent
        if isinstance(knowledge_graph, dict):
            insights_data = knowledge_graph.get("insights", {})
            for perspective in ResearchPerspective:
                insights = [
                    i
                    for i in insights_data.values()
                    if i.get("perspective") == perspective.value
                ]
                matrix[perspective.value] = [
                    i.get("content", "") for i in insights[:3]
                ]  # Top 3 insights
        else:
            for perspective in ResearchPerspective:
                insights = [
                    i
                    for i in knowledge_graph.insights.values()
                    if i.perspective == perspective
                ]
                matrix[perspective.value] = [
                    i.content for i in insights[:3]
                ]  # Top 3 insights
        return matrix

    def _generate_requirements(self, knowledge_graph: KnowledgeGraph) -> List[str]:
        """Generate actionable requirements"""
        requirements = [
            "Implement multi-agent architecture with clear separation of concerns",
            "Include comprehensive safety and validation mechanisms",
            "Design for horizontal scalability from the start",
            "Use structured logging and observability throughout",
            "Follow test-driven development practices",
        ]
        return requirements

    async def _write_report(self, path: Path, sections: Dict[str, Any]) -> None:
        """Write report to file"""
        content = f"""
---
## Additional Research Perspective: cursor-agent

{sections['executive_summary']}

## Model Viewpoints Matrix

{json.dumps(sections['model_viewpoints_matrix'], indent=2)}

## Consensus Patterns

{json.dumps(sections['consensus_patterns'], indent=2)}

## Valuable Divergences

{json.dumps(sections['valuable_divergences'], indent=2)}

## Actionable Requirements

{chr(10).join(f'- {req}' for req in sections['actionable_requirements'])}

---
Generated on: {datetime.now().isoformat()}
"""
        path.write_text(content)
        await asyncio.sleep(0.1)


class ImplementationPlanAgent(BaseΣAgent):
    """Agent for Phase C: Implementation Planning"""

    def __init__(self):
        super().__init__("ImplementationPlan", ΣBuilderPhase.IMPLEMENTATION_PLAN)

    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation plan"""
        self.log_progress("Creating implementation plan")

        plan = {
            "directory_layout": self._define_directory_layout(),
            "technology_stack": self._define_tech_stack(),
            "milestones": self._define_milestones(),
            "risk_mitigation": self._define_risk_mitigation(),
        }

        # Write plan
        plan_path = Path("implementation/00_cursor-agent-plan.md")
        plan_path.parent.mkdir(parents=True, exist_ok=True)

        await self._write_plan(plan_path, plan)

        self.log_progress(f"Implementation plan written to {plan_path}")

        return {"plan_path": str(plan_path), "plan": plan, **context}

    def _define_directory_layout(self) -> Dict[str, str]:
        """Define target directory layout"""
        return {
            "agent-runtime/": "Core runtime components",
            "agent-runtime/src/": "Source code",
            "agent-runtime/tests/": "Test suites",
            "agent-runtime/docs/": "Documentation",
            "agent-runtime/configs/": "Configuration files",
            "agent-runtime/scripts/": "Utility scripts",
        }

    def _define_tech_stack(self) -> Dict[str, str]:
        """Define technology stack"""
        return {
            "language": "Python 3.11+",
            "framework": "FastAPI",
            "async": "asyncio",
            "testing": "pytest + pytest-asyncio",
            "logging": "structlog",
            "config": "pydantic-settings",
            "docs": "mkdocs-material",
        }

    def _define_milestones(self) -> List[Dict[str, str]]:
        """Define implementation milestones"""
        return [
            {"milestone": "M1", "description": "Core scaffolding and base classes"},
            {
                "milestone": "M2",
                "description": "Agent implementations and orchestration",
            },
            {"milestone": "M3", "description": "Safety guards and validation"},
            {"milestone": "M4", "description": "Testing and CI/CD setup"},
            {"milestone": "M5", "description": "Documentation and demos"},
        ]

    def _define_risk_mitigation(self) -> Dict[str, str]:
        """Define risk mitigation strategies"""
        return {
            "complexity": "Start with simple implementations, iterate",
            "performance": "Profile early, optimize hotspots",
            "safety": "Multiple validation layers, fail-safe defaults",
            "scalability": "Design for horizontal scaling from start",
        }

    async def _write_plan(self, path: Path, plan: Dict[str, Any]) -> None:
        """Write implementation plan"""
        content = f"""
---
## Additional Research Perspective: cursor-agent

# Implementation Plan

## Directory Layout
{json.dumps(plan['directory_layout'], indent=2)}

## Technology Stack
{json.dumps(plan['technology_stack'], indent=2)}

## Milestones
{json.dumps(plan['milestones'], indent=2)}

## Risk Mitigation
{json.dumps(plan['risk_mitigation'], indent=2)}

---
Generated on: {datetime.now().isoformat()}
"""
        path.write_text(content)
        await asyncio.sleep(0.1)


class ΣBuilderOrchestrator:
    """Main orchestrator for the Σ-Builder workflow"""

    def __init__(self):
        self.agents = {
            ΣBuilderPhase.RESEARCH_DIGESTION: ResearchDigestionAgent(),
            ΣBuilderPhase.SYNTHESIS_REPORT: SynthesisReportAgent(),
            ΣBuilderPhase.IMPLEMENTATION_PLAN: ImplementationPlanAgent(),
        }
        self.context = {}
        self.logger = logging.getLogger(f"{__name__}.Orchestrator")

    async def execute_workflow(self) -> Dict[str, Any]:
        """Execute the complete Σ-Builder workflow"""
        self.logger.info("Starting Σ-Builder workflow")

        results = {}

        # Execute phases in order
        for phase in [
            ΣBuilderPhase.RESEARCH_DIGESTION,
            ΣBuilderPhase.SYNTHESIS_REPORT,
            ΣBuilderPhase.IMPLEMENTATION_PLAN,
        ]:
            agent = self.agents.get(phase)
            if agent:
                self.logger.info(f"Executing phase: {phase.value}")
                phase_result = await agent.execute(self.context)
                self.context.update(phase_result)
                results[phase.value] = phase_result

        self.logger.info("Σ-Builder workflow completed")

        return {
            "status": "completed",
            "phases_executed": list(results.keys()),
            "final_context": self.context,
        }


class TaskRequest(BaseModel):
    """Request model for task submission"""

    description: str = Field(..., description="Task description")
    phase: Optional[str] = Field(None, description="Specific phase to execute")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    """Response model for task execution"""

    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Global orchestrator instance
orchestrator = ΣBuilderOrchestrator()


async def process_sigma_builder_request(request: TaskRequest) -> TaskResponse:
    """Process a Σ-Builder request"""
    task_id = f"sigma_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    try:
        if request.phase:
            # Execute specific phase
            phase = ΣBuilderPhase(request.phase)
            agent = orchestrator.agents.get(phase)
            if not agent:
                raise ValueError(f"Unknown phase: {request.phase}")

            result = await agent.execute(orchestrator.context)
        else:
            # Execute full workflow
            result = await orchestrator.execute_workflow()

        return TaskResponse(task_id=task_id, status="completed", result=result)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return TaskResponse(task_id=task_id, status="failed", error=str(e))


if __name__ == "__main__":
    # Example usage
    async def main():
        request = TaskRequest(
            description="Execute full Σ-Builder workflow", config={"verbose": True}
        )

        response = await process_sigma_builder_request(request)
        print(f"Task {response.task_id}: {response.status}")
        if response.result:
            print(f"Result: {json.dumps(response.result, indent=2)}")

    asyncio.run(main())
