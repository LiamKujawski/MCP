"""
Test suite for Unified Σ-Builder agent (O3 prompt via Opus model)
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.unified_sigma_agent import (
    WorkflowPhase,
    ResearchContext,
    UnifiedΣAgent,
    ΣTaskRequest,
    ΣTaskResponse,
    process_sigma_task
)
from src.main import app


class TestResearchContext:
    """Test research context dataclass"""
    
    def test_initialization(self):
        """Test context initialization with defaults"""
        context = ResearchContext()
        
        assert context.files_processed == 0
        assert context.insights == []
        assert context.consensus_patterns == []
        assert context.divergences == []
        assert context.knowledge_base == {}
    
    def test_custom_values(self):
        """Test context with custom values"""
        insights = [{"test": "insight"}]
        context = ResearchContext(
            files_processed=5,
            insights=insights
        )
        
        assert context.files_processed == 5
        assert context.insights == insights


class TestUnifiedΣAgent:
    """Test unified Sigma Builder agent"""
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self):
        """Test full workflow execution"""
        agent = UnifiedΣAgent()
        
        with patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "mkdir"), \
             patch.object(Path, "write_text"):
            result = await agent.execute_workflow()
        
        assert result["status"] == "completed"
        assert "phases_executed" in result
        assert len(result["phases_executed"]) == 3
        assert "metrics" in result
    
    @pytest.mark.asyncio
    async def test_digest_research(self):
        """Test research digestion phase"""
        agent = UnifiedΣAgent()
        
        with patch.object(Path, "exists", return_value=True):
            result = await agent._digest_research()
        
        assert "files_processed" in result
        assert "total_insights" in result
        assert "insights_by_model" in result
        assert "consensus_count" in result
        assert "divergence_count" in result
    
    def test_categorize_file(self):
        """Test file categorization"""
        agent = UnifiedΣAgent()
        
        assert agent._categorize_file("01_overview.md") == "overview"
        assert agent._categorize_file("02_architecture-deep-dive.md") == "architecture"
        assert agent._categorize_file("03_codebase-setup.md") == "setup"
        assert agent._categorize_file("04_prompt-structure.md") == "prompts"
        assert agent._categorize_file("05_enhancements.md") == "enhancements"
        assert agent._categorize_file("unknown.md") == "general"
    
    def test_analyze_patterns(self):
        """Test pattern analysis"""
        agent = UnifiedΣAgent()
        
        insights_by_model = {
            "o3": [
                {"type": "architecture", "content": "o3 architecture"},
                {"type": "safety", "content": "o3 safety"}
            ],
            "sonnet": [
                {"type": "architecture", "content": "sonnet architecture"},
                {"type": "performance", "content": "sonnet performance"}
            ]
        }
        
        agent._analyze_patterns(insights_by_model)
        
        # Should find consensus on architecture
        assert len(agent.context.consensus_patterns) >= 1
        assert any(p["type"] == "architecture" for p in agent.context.consensus_patterns)
        
        # Should find divergences
        assert len(agent.context.divergences) >= 1
    
    @pytest.mark.asyncio
    async def test_generate_synthesis_report(self):
        """Test synthesis report generation"""
        agent = UnifiedΣAgent()
        agent.context.files_processed = 10
        agent.context.insights = [{"test": "insight"}] * 5
        
        with patch.object(Path, "mkdir"), \
             patch.object(Path, "write_text"):
            result = await agent._generate_synthesis_report()
        
        assert "report_path" in result
        assert "sections" in result
        assert "word_count" in result
    
    @pytest.mark.asyncio
    async def test_create_implementation_plan(self):
        """Test implementation plan creation"""
        agent = UnifiedΣAgent()
        
        with patch.object(Path, "mkdir"), \
             patch.object(Path, "write_text"):
            result = await agent._create_implementation_plan()
        
        assert "plan_path" in result
        assert "components" in result
        assert "total_duration" in result
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        agent = UnifiedΣAgent()
        agent.context.files_processed = 15
        agent.context.insights = [{"test": "insight"}] * 20
        agent.context.consensus_patterns = [{"test": "pattern"}] * 5
        agent.context.divergences = [{"test": "divergence"}] * 3
        
        metrics = agent._calculate_metrics()
        
        assert metrics["files_processed"] == 15
        assert metrics["insights_extracted"] == 20
        assert metrics["consensus_patterns"] == 5
        assert metrics["divergences"] == 3
        assert metrics["success_rate"] == 1.0


class TestProcessSigmaTask:
    """Test task processing function"""
    
    @pytest.mark.asyncio
    async def test_process_full_workflow(self):
        """Test processing full workflow task"""
        request = ΣTaskRequest(
            description="Execute workflow"
        )
        
        with patch.object(Path, "exists", return_value=True), \
             patch.object(Path, "mkdir"), \
             patch.object(Path, "write_text"):
            response = await process_sigma_task(request)
        
        assert response.status == "completed"
        assert response.result is not None
        assert response.execution_time is not None
        assert response.error is None
    
    @pytest.mark.asyncio
    async def test_process_specific_phase_error(self):
        """Test that specific phase execution returns error"""
        request = ΣTaskRequest(
            description="Execute phase",
            phase=WorkflowPhase.RESEARCH_DIGESTION
        )
        
        response = await process_sigma_task(request)
        
        assert response.status == "error"
        assert response.error == "Unified agent executes all phases together"
    
    @pytest.mark.asyncio
    async def test_process_error_handling(self):
        """Test error handling in task processing"""
        request = ΣTaskRequest(
            description="Execute workflow"
        )
        
        with patch.object(UnifiedΣAgent, "execute_workflow", side_effect=Exception("Test error")):
            response = await process_sigma_task(request)
        
        assert response.status == "failed"
        assert response.error == "Test error"
        assert response.execution_time is not None


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
        assert data["name"] == "Unified Σ-Builder API"
        assert "workflow_phases" in data
        assert "endpoints" in data
        assert "characteristics" in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent_type"] == "unified"
    
    def test_execute_workflow_endpoint(self, client):
        """Test workflow execution endpoint"""
        request_data = {
            "description": "Test workflow",
            "config": {}
        }
        
        with patch("src.main.process_sigma_task") as mock_process:
            mock_process.return_value = ΣTaskResponse(
                task_id="test_123",
                status="completed",
                result={"test": "result"}
            )
            
            response = client.post("/workflow/execute", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "test_123"
        assert data["status"] == "completed"
    
    def test_get_metrics_endpoint(self, client):
        """Test metrics endpoint"""
        # Add a workflow to app state
        with client:
            # Simulate app startup
            client.app.state.active_workflows = {
                "test_workflow": {
                    "status": "completed",
                    "result": {
                        "metrics": {
                            "insights_extracted": 10,
                            "files_processed": 5
                        }
                    }
                }
            }
            
            response = client.get("/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert "workflows" in data
        assert "performance" in data
        assert "system" in data
    
    def test_simulate_endpoint(self, client):
        """Test simulation endpoint"""
        with patch("src.main.process_sigma_task") as mock_process:
            mock_process.return_value = ΣTaskResponse(
                task_id="sim_123",
                status="completed"
            )
            
            response = client.post("/simulate")
        
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == "sim_123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 