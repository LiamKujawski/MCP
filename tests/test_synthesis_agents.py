"""
Test suite for Σ-Builder agents (O3 prompt via Sonnet model)
"""

import sys
import os
from pathlib import Path
from unittest.mock import patch

# Add src to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

from src.synthesized_agent import (
    ResearchPerspective,
    InsightType,
    ResearchInsight,
    KnowledgeGraph,
    ΣBuilderPhase,
    ResearchDigestionAgent,
    SynthesisReportAgent,
    ImplementationPlanAgent,
    ΣBuilderOrchestrator,
    TaskRequest,
    process_sigma_builder_request,
)
from src.main import app


class TestKnowledgeGraph:
    """Test knowledge graph functionality"""

    def test_add_insight(self):
        """Test adding insights to knowledge graph"""
        graph = KnowledgeGraph()

        insight = ResearchInsight(
            id="test_1",
            source_file="test.md",
            perspective=ResearchPerspective.O3,
            type=InsightType.ARCHITECTURE,
            content="Test insight",
        )

        graph.add_insight(insight)

        assert "test_1" in graph.insights
        assert graph.insights["test_1"] == insight
        assert "test_1" in graph.graph.nodes

    def test_identify_consensus(self):
        """Test consensus pattern identification"""
        graph = KnowledgeGraph()

        # Add insights from multiple perspectives on same type
        for i, perspective in enumerate(
            [ResearchPerspective.O3, ResearchPerspective.CLAUDE_4_SONNET]
        ):
            insight = ResearchInsight(
                id=f"insight_{i}",
                source_file=f"file_{i}.md",
                perspective=perspective,
                type=InsightType.ARCHITECTURE,
                content=f"Architecture insight from {perspective.value}",
            )
            graph.add_insight(insight)

        consensus = graph.identify_consensus()

        assert len(consensus) == 1
        assert consensus[0]["type"] == InsightType.ARCHITECTURE.value
        assert len(consensus[0]["perspectives"]) == 2

    def test_identify_divergences(self):
        """Test divergence identification"""
        graph = KnowledgeGraph()

        # Add unique insight for O3
        insight1 = ResearchInsight(
            id="o3_unique",
            source_file="o3.md",
            perspective=ResearchPerspective.O3,
            type=InsightType.SAFETY,
            content="O3 unique safety insight",
        )

        # Add different insight for Sonnet
        insight2 = ResearchInsight(
            id="sonnet_unique",
            source_file="sonnet.md",
            perspective=ResearchPerspective.CLAUDE_4_SONNET,
            type=InsightType.PERFORMANCE,
            content="Sonnet unique performance insight",
        )

        graph.add_insight(insight1)
        graph.add_insight(insight2)

        divergences = graph.identify_divergences()

        assert len(divergences) >= 1
        assert any(
            d["perspective"] == ResearchPerspective.O3.value for d in divergences
        )


class TestResearchDigestionAgent:
    """Test research digestion agent"""

    @pytest.mark.asyncio
    async def test_execute(self):
        """Test research digestion execution"""
        agent = ResearchDigestionAgent()

        with patch.object(Path, "exists", return_value=True):
            result = await agent.execute({})

        assert "knowledge_graph" in result
        assert "insights_count" in result
        assert "files_processed" in result
        assert "consensus_patterns" in result
        assert "divergences" in result
        assert result["insights_count"] > 0

    @pytest.mark.asyncio
    async def test_process_research_file(self):
        """Test processing individual research file"""
        agent = ResearchDigestionAgent()

        file_path = Path("test/01_overview.md")
        insights = await agent._process_research_file(file_path, ResearchPerspective.O3)

        assert len(insights) == 1
        assert insights[0].perspective == ResearchPerspective.O3
        assert insights[0].type == InsightType.ARCHITECTURE


class TestSynthesisReportAgent:
    """Test synthesis report generation"""

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful synthesis report generation"""
        agent = SynthesisReportAgent()

        # Create mock knowledge graph
        knowledge_graph = KnowledgeGraph()
        insight = ResearchInsight(
            id="test",
            source_file="test.md",
            perspective=ResearchPerspective.O3,
            type=InsightType.ARCHITECTURE,
            content="Test",
        )
        knowledge_graph.add_insight(insight)

        with patch.object(Path, "mkdir"), patch.object(Path, "write_text"):
            result = await agent.execute({"knowledge_graph": knowledge_graph})

        assert "report_path" in result
        assert "sections_generated" in result
        assert len(result["sections_generated"]) == 5

    @pytest.mark.asyncio
    async def test_execute_no_knowledge_graph(self):
        """Test synthesis report without knowledge graph"""
        agent = SynthesisReportAgent()

        with pytest.raises(ValueError, match="Knowledge graph not found"):
            await agent.execute({})


class TestImplementationPlanAgent:
    """Test implementation plan generation"""

    @pytest.mark.asyncio
    async def test_execute(self):
        """Test implementation plan generation"""
        agent = ImplementationPlanAgent()

        with patch.object(Path, "mkdir"), patch.object(Path, "write_text"):
            result = await agent.execute({})

        assert "plan_path" in result
        assert "plan" in result

        plan = result["plan"]
        assert "directory_layout" in plan
        assert "technology_stack" in plan
        assert "milestones" in plan
        assert "risk_mitigation" in plan


class TestΣBuilderOrchestrator:
    """Test main orchestrator"""

    @pytest.mark.asyncio
    async def test_execute_workflow(self):
        """Test full workflow execution"""
        orchestrator = ΣBuilderOrchestrator()

        with patch.object(Path, "exists", return_value=True), patch.object(
            Path, "mkdir"
        ), patch.object(Path, "write_text"):
            result = await orchestrator.execute_workflow()

        assert result["status"] == "completed"
        assert len(result["phases_executed"]) == 3
        assert "final_context" in result


class TestProcessSigmaBuilderRequest:
    """Test request processing function"""

    @pytest.mark.asyncio
    async def test_process_full_workflow(self):
        """Test processing full workflow request"""
        request = TaskRequest(description="Execute full workflow")

        with patch.object(Path, "exists", return_value=True), patch.object(
            Path, "mkdir"
        ), patch.object(Path, "write_text"):
            response = await process_sigma_builder_request(request)

        assert response.status == "completed"
        assert response.result is not None
        assert response.error is None

    @pytest.mark.asyncio
    async def test_process_specific_phase(self):
        """Test processing specific phase request"""
        request = TaskRequest(
            description="Execute research digestion",
            phase=ΣBuilderPhase.RESEARCH_DIGESTION.value,
        )

        with patch.object(Path, "exists", return_value=True):
            response = await process_sigma_builder_request(request)

        assert response.status == "completed"
        assert response.result is not None

    @pytest.mark.asyncio
    async def test_process_error_handling(self):
        """Test error handling in request processing"""
        request = TaskRequest(
            description="Execute invalid phase", phase="invalid_phase"
        )

        response = await process_sigma_builder_request(request)

        assert response.status == "failed"
        assert response.error is not None


class TestFastAPIEndpoints:
    """Test FastAPI endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Σ-Builder API"
        assert "phases" in data
        assert "endpoints" in data

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_list_agents_endpoint(self, client):
        """Test list agents endpoint"""
        response = client.get("/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 3

    def test_start_workflow_endpoint(self, client):
        """Test workflow start endpoint"""
        with patch("src.main.run_workflow_background"):
            response = client.post("/workflow/start")

        assert response.status_code == 200
        data = response.json()
        assert "workflow_id" in data
        assert data["status"] == "running"

    def test_execute_phase_endpoint(self, client):
        """Test phase execution endpoint"""
        request_data = {
            "phase": "research_digestion",  # Use string directly
            "context": {},
        }

        with patch.object(Path, "exists", return_value=True):
            response = client.post("/phase/execute", json=request_data)

        # If we get a 400, print the error for debugging
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "completed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
