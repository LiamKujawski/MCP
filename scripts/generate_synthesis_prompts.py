#!/usr/bin/env python3
"""
Generate synthesis prompts from research enhancements files.
"""
import os
import re
from pathlib import Path
from datetime import datetime

PROMPT_TEMPLATE = """# Σ-Builder Master Implementation Prompt - {model} Model

## System Context
You are the Σ-Builder orchestrator implementing a fully automated Research → Synthesis → Experiment → Deploy → Optimize pipeline based on synthesized multi-model research.

## Research Synthesis
This prompt incorporates enhancements and insights from:
- O3 Model Research
- Claude-4-Sonnet Research  
- Claude-4-Opus Research

## Implementation Requirements

### Core Architecture
{architecture_requirements}

### Technical Stack
- **Backend**: FastAPI with async/await patterns, WebSocket support
- **Frontend**: Next.js 13+ (App Router) with TypeScript, Tailwind CSS
- **Testing**: 
  - Backend: pytest with ≥90% coverage
  - Frontend: Playwright E2E tests, Storybook component tests
- **Documentation**: 
  - C4 diagrams in `/docs/architecture`
  - ADRs using MADR template
  - API documentation with OpenAPI/Swagger

### Security Requirements
- Semgrep and Bandit clean builds
- OWASP Top 10 compliance
- Security headers implementation
- Input validation and sanitization

## Enhanced Features Based on Research

{enhanced_features}

## Implementation Phases

### Phase 1: Core Infrastructure
1. Set up monorepo structure
2. Implement core agent architecture
3. Create base UI components
4. Set up CI/CD pipeline

### Phase 2: Agent Implementation
1. Implement multi-agent orchestration
2. Add tool integration layer
3. Create safety monitoring system
4. Build virtual environment manager

### Phase 3: UI Development
1. Create responsive Next.js frontend
2. Implement real-time updates via WebSockets
3. Add Storybook stories for all components
4. Write comprehensive Playwright tests

### Phase 4: Integration & Testing
1. Integrate all components
2. Run security scans
3. Performance optimization
4. Load testing

### Phase 5: Documentation & Deployment
1. Generate C4 diagrams
2. Write ADRs for key decisions
3. Create deployment configurations
4. Set up monitoring and alerting

## Acceptance Criteria
- [ ] All tests passing with ≥90% coverage
- [ ] Lighthouse performance score ≥90
- [ ] Zero HIGH/CRITICAL security findings
- [ ] Complete C4 documentation
- [ ] Deployment automation working
- [ ] Real-time UI updates functional

## Additional Context
{additional_context}

---
Generated: {timestamp}
"""

def extract_enhancements(file_path):
    """Extract enhancement content from a research file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract sections after "Enhancements" or similar headers
    enhancement_pattern = r'##\s+(?:Enhancements?|Future Work|Improvements?)(.*?)(?=##\s+DocOps Footer|---|\Z)'
    matches = re.findall(enhancement_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if matches:
        return '\n'.join(matches).strip()
    return ""

def extract_architecture_insights(research_dir):
    """Extract architecture insights from all research files."""
    insights = []
    
    for model_dir in ["o3", "claude-4-sonnet", "claude-4-opus"]:
        arch_file = Path(research_dir) / model_dir / "02_architecture.md"
        if arch_file.exists():
            with open(arch_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract key architecture points
                if "multi-agent" in content.lower():
                    insights.append(f"- Multi-agent architecture emphasized by {model_dir}")
                if "microservice" in content.lower():
                    insights.append(f"- Microservices pattern recommended by {model_dir}")
                if "event-driven" in content.lower():
                    insights.append(f"- Event-driven architecture suggested by {model_dir}")
    
    return '\n'.join(insights)

def generate_synthesis_prompt(research_type, model):
    """Generate a synthesis prompt for a specific model."""
    research_dir = f"{research_type}-research"
    
    # Collect enhancements from all models
    all_enhancements = []
    for model_name in ["o3", "claude-4-sonnet", "claude-4-opus"]:
        enhancement_file = Path(research_dir) / model_name / "05_enhancements.md"
        if enhancement_file.exists():
            enhancements = extract_enhancements(enhancement_file)
            if enhancements:
                all_enhancements.append(f"### {model_name.upper()} Enhancements\n{enhancements}")
    
    # Extract architecture requirements
    architecture_requirements = extract_architecture_insights(research_dir)
    
    # Prepare additional context based on research type
    if research_type == "chatgpt-agent":
        additional_context = """
- Focus on autonomous agent capabilities
- Implement comprehensive tool integration
- Ensure robust safety mechanisms
- Support for long-running tasks
"""
    else:
        additional_context = """
- Focus on code generation quality
- Implement multi-stage validation
- Support multiple programming languages
- Ensure generated code is production-ready
"""
    
    # Generate the prompt
    prompt = PROMPT_TEMPLATE.format(
        model=model.upper(),
        architecture_requirements=architecture_requirements or "- Follow best practices for distributed systems",
        enhanced_features='\n\n'.join(all_enhancements),
        additional_context=additional_context,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    return prompt

def main():
    """Generate all synthesis prompts."""
    research_types = ["chatgpt-agent", "codebase-generation-prompt"]
    models = ["o3", "claude-4-sonnet", "claude-4-opus"]
    
    for research_type in research_types:
        for model in models:
            # Create output directory
            output_dir = Path("synthesize-research-prompts") / model
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate prompt
            prompt = generate_synthesis_prompt(research_type, model)
            
            # Save prompt
            output_file = output_dir / "AGENT_IMPLEMENTATION_PROMPT.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            
            print(f"Generated: {output_file}")
    
    print("\nSynthesis prompt generation complete!")

if __name__ == "__main__":
    main() 