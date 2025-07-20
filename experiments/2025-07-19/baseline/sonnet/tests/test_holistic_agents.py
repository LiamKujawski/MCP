"""
Test suite for Claude-4-Sonnet's holistic agent implementation.
Tests multi-model integration and knowledge synthesis.
"""

import pytest
import asyncio
from src.agents.multi_model_agent import (
    ModelPerspective, ResearchInsight, KnowledgeGraph,
    ResearchSynthesizer, ImplementationAgent, 
    QualityAssuranceAgent
)


@pytest.fixture
def sample_research_data():
    """Sample research data from multiple models."""
    return {
        "chatgpt-agent": {
            "o3": {
                "architecture": "Hierarchical multi-agent system",
                "safety": "Permission-based safety gates"
            },
            "claude-4-sonnet": {
                "architecture": "Holistic integration framework",
                "safety": "Multi-layer validation"
            },
            "claude-4-opus": {
                "architecture": "Modular microservices",
                "safety": "Comprehensive monitoring"
            }
        },
        "codebase-generation": {
            "o3": {
                "approach": "Template-based generation",
                "quality": "Static analysis integration"
            },
            "claude-4-sonnet": {
                "approach": "Context-aware synthesis",
                "quality": "Comprehensive testing"
            }
        }
    }


@pytest.mark.asyncio
async def test_knowledge_graph_construction():
    """Test knowledge graph construction and pattern detection."""
    graph = KnowledgeGraph()
    
    # Add insights from different models
    graph.add_insight(ResearchInsight(
        model=ModelPerspective.O3,
        category="architecture",
        insight="Multi-agent system",
        confidence=0.9
    ))
    
    graph.add_insight(ResearchInsight(
        model=ModelPerspective.SONNET,
        category="architecture",
        insight="Holistic framework",
        confidence=0.95
    ))
    
    # Should detect convergent pattern
    assert len(graph.convergent_patterns) > 0
    assert graph.convergent_patterns[0]["category"] == "architecture"


@pytest.mark.asyncio
async def test_research_synthesizer(sample_research_data):
    """Test research synthesis capabilities."""
    synthesizer = ResearchSynthesizer("test_synthesizer")
    await synthesizer.digest_research(sample_research_data)
    
    # Test convergent synthesis
    convergent_result = await synthesizer.execute_task({"type": "convergent"})
    assert convergent_result["synthesis_type"] == "convergent"
    assert "patterns" in convergent_result
    
    # Test divergent synthesis
    divergent_result = await synthesizer.execute_task({"type": "divergent"})
    assert divergent_result["synthesis_type"] == "divergent"
    assert "divergent_approaches" in divergent_result
    
    # Test comprehensive synthesis
    comprehensive_result = await synthesizer.execute_task({"type": "comprehensive"})
    assert comprehensive_result["synthesis_type"] == "comprehensive"
    assert "unified_vision" in comprehensive_result
    assert "implementation_strategy" in comprehensive_result


@pytest.mark.asyncio
async def test_implementation_agent():
    """Test implementation agent phases."""
    agent = ImplementationAgent("test_implementation")
    
    # Test foundation phase
    foundation_result = await agent.execute_task({"phase": "foundation"})
    assert foundation_result["phase"] == "foundation"
    assert foundation_result["status"] == "completed"
    assert len(foundation_result["components_created"]) > 0
    
    # Test integration phase
    integration_result = await agent.execute_task({"phase": "integration"})
    assert integration_result["phase"] == "integration"
    assert integration_result["status"] == "completed"
    
    # Test enhancement phase
    enhancement_result = await agent.execute_task({"phase": "enhancement"})
    assert enhancement_result["phase"] == "enhancement"
    assert enhancement_result["deployment_ready"] is True


@pytest.mark.asyncio
async def test_quality_assurance_agent():
    """Test quality assurance agent."""
    agent = QualityAssuranceAgent("test_qa")
    
    # Test research alignment
    alignment_result = await agent.execute_task({"type": "alignment"})
    assert alignment_result["qa_type"] == "research_alignment"
    assert alignment_result["checks_passed"] is True
    
    # Test comprehensive testing
    testing_result = await agent.execute_task({"type": "testing"})
    assert testing_result["qa_type"] == "testing"
    assert testing_result["pass_rate"] == 100.0
    assert testing_result["total_tests"] > 150
    
    # Test security validation
    security_result = await agent.execute_task({"type": "security"})
    assert security_result["qa_type"] == "security"
    assert security_result["all_passed"] is True
    
    # Test comprehensive QA
    comprehensive_result = await agent.execute_task({"type": "comprehensive"})
    assert comprehensive_result["overall_status"] == "passed"


@pytest.mark.asyncio
async def test_multi_model_perspective_integration():
    """Test integration of multiple model perspectives."""
    synthesizer = ResearchSynthesizer("multi_model_test")
    
    # Create insights from each model
    for model in ModelPerspective:
        insight = ResearchInsight(
            model=model,
            category="testing",
            insight=f"{model.value} testing approach",
            confidence=0.8
        )
        synthesizer.knowledge_graph.add_insight(insight)
    
    # Should have insights from all models
    assert len(synthesizer.knowledge_graph.insights) == 3
    
    # Should identify convergent pattern
    assert len(synthesizer.knowledge_graph.convergent_patterns) > 0


@pytest.mark.asyncio
async def test_full_agent_pipeline(sample_research_data):
    """Test full agent pipeline from research to deployment."""
    # Phase 1: Research synthesis
    synthesizer = ResearchSynthesizer("pipeline_synthesizer")
    await synthesizer.digest_research(sample_research_data)
    synthesis = await synthesizer.execute_task({"type": "comprehensive"})
    
    assert synthesis["unified_vision"] is not None
    assert synthesis["implementation_strategy"] is not None
    
    # Phase 2: Implementation
    implementation = ImplementationAgent("pipeline_implementation")
    
    # Execute all phases
    for phase in ["foundation", "integration", "enhancement"]:
        result = await implementation.execute_task({"phase": phase})
        assert result["status"] == "completed"
    
    # Phase 3: Quality assurance
    qa = QualityAssuranceAgent("pipeline_qa")
    qa_result = await qa.execute_task({"type": "comprehensive"})
    
    assert qa_result["overall_status"] == "passed"


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in agents."""
    agent = ImplementationAgent("error_test")
    
    # Test invalid phase
    result = await agent.execute_task({"phase": "invalid"})
    assert "error" in result
    assert "Unknown phase" in result["error"]


@pytest.mark.asyncio
async def test_research_insight_citations():
    """Test research insight with citations."""
    insight = ResearchInsight(
        model=ModelPerspective.SONNET,
        category="performance",
        insight="Optimize using caching",
        confidence=0.85,
        citations=["paper1.pdf", "benchmark2.json"]
    )
    
    assert len(insight.citations) == 2
    assert insight.confidence == 0.85


@pytest.mark.asyncio
async def test_knowledge_graph_pattern_detection():
    """Test pattern detection in knowledge graph."""
    graph = KnowledgeGraph()
    
    # Add multiple insights in same category from different models
    for i, model in enumerate([ModelPerspective.O3, ModelPerspective.SONNET]):
        graph.add_insight(ResearchInsight(
            model=model,
            category="scalability",
            insight=f"Scalability approach {i}",
            confidence=0.9,
            convergent=True
        ))
    
    # Should detect convergent pattern
    assert len(graph.convergent_patterns) == 1
    pattern = graph.convergent_patterns[0]
    assert pattern["category"] == "scalability"
    assert len(pattern["models"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 