# C4 Model - Context Diagram

## System Context for MCP Platform

The MCP (Multi-Agent Collaborative Platform) operates as an autonomous research-to-production pipeline that transforms AI model insights into deployable software without human intervention.

```mermaid
C4Context
    title System Context diagram for MCP Platform
    
    Person(researcher, "AI Researcher", "Contributes research and insights")
    Person(developer, "Developer", "Reviews and extends the system")
    Person(user, "End User", "Uses deployed applications")
    
    System_Boundary(mcp, "MCP Platform") {
        System(platform, "MCP Automation Platform", "Transforms research into production deployments")
    }
    
    System_Ext(github, "GitHub", "Source control and CI/CD")
    System_Ext(ghcr, "GitHub Container Registry", "Docker image storage")
    System_Ext(openai, "OpenAI API", "LLM services")
    System_Ext(anthropic, "Anthropic API", "Claude models")
    System_Ext(cloud, "Cloud Infrastructure", "Deployment target")
    
    Rel(researcher, platform, "Submits research", "Markdown files")
    Rel(developer, platform, "Configures and monitors", "Web UI / CLI")
    Rel(platform, user, "Delivers applications", "HTTPS")
    
    Rel(platform, github, "Stores code and triggers CI", "Git/HTTPS")
    Rel(platform, ghcr, "Pushes container images", "Docker Registry API")
    Rel(platform, openai, "Generates implementations", "API")
    Rel(platform, anthropic, "Generates implementations", "API")
    Rel(platform, cloud, "Deploys applications", "Kubernetes API")
```

## Key Actors

### Researchers
- Submit research findings in structured markdown format
- Define enhancements and future directions
- Contribute multi-model perspectives

### Developers
- Monitor system performance
- Review generated implementations
- Extend platform capabilities

### End Users
- Access deployed applications
- Benefit from continuous improvements
- Provide indirect feedback through usage metrics

## External Systems

### GitHub
- Hosts source code repository
- Runs GitHub Actions workflows
- Manages pull requests and issues

### Container Registries
- Stores multi-architecture Docker images
- Enables versioned deployments
- Supports rollback capabilities

### LLM Providers
- Generate code implementations
- Process synthesis prompts
- Provide model-specific insights

### Cloud Infrastructure
- Hosts production deployments
- Provides compute resources
- Enables global distribution

## Data Flows

1. **Research Input**: Markdown files → Git repository
2. **Synthesis**: Research files → Implementation prompts
3. **Generation**: Prompts → Code implementations
4. **Evaluation**: Implementations → Performance metrics
5. **Deployment**: Docker images → Production environment

---

## Next: [Container Diagram](./c4-container.md) 