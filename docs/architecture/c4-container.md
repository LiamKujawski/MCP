# C4 Model - Container Diagram

## Container View of MCP Platform

This diagram shows the high-level containers (applications, databases, file systems) that make up the MCP Platform.

```mermaid
C4Container
    title Container diagram for MCP Platform
    
    Person(researcher, "AI Researcher", "Contributes research")
    Person(developer, "Developer", "Monitors system")
    Person(user, "End User", "Uses applications")
    
    System_Boundary(mcp, "MCP Platform") {
        Container(ui, "Web UI", "Next.js, TypeScript", "Provides monitoring and control interface")
        Container(api, "API Gateway", "FastAPI, Python", "Handles all API requests")
        Container(orchestrator, "Σ-Builder Orchestrator", "Python", "Coordinates the automation pipeline")
        
        Container_Boundary(research, "Research Layer") {
            Container(normalizer, "Research Normalizer", "Python", "Standardizes research format")
            Container(synthesizer, "Prompt Synthesizer", "Python", "Generates implementation prompts")
        }
        
        Container_Boundary(experiment, "Experiment Layer") {
            Container(runner, "Experiment Runner", "Python", "Executes model experiments")
            Container(evaluator, "Result Evaluator", "Python", "Scores and selects implementations")
        }
        
        Container_Boundary(deploy, "Deployment Layer") {
            Container(builder, "Image Builder", "Docker", "Creates container images")
            Container(deployer, "Deploy Manager", "Python", "Manages deployments")
        }
        
        ContainerDb(postgres, "Database", "PostgreSQL", "Stores application data")
        ContainerDb(redis, "Cache", "Redis", "Session and cache storage")
        ContainerDb(storage, "Object Storage", "S3-compatible", "Stores artifacts and logs")
    }
    
    System_Ext(github, "GitHub", "Version control")
    System_Ext(ghcr, "Container Registry", "Image storage")
    System_Ext(llm, "LLM APIs", "AI models")
    
    Rel(researcher, ui, "Submits research via", "HTTPS")
    Rel(developer, ui, "Monitors system", "HTTPS")
    Rel(user, api, "Uses API", "HTTPS/WSS")
    
    Rel(ui, api, "Makes API calls", "HTTPS/WSS")
    Rel(api, orchestrator, "Triggers workflows", "gRPC")
    Rel(orchestrator, normalizer, "Processes research", "Async")
    Rel(normalizer, synthesizer, "Sends normalized data", "Queue")
    Rel(synthesizer, runner, "Provides prompts", "Queue")
    Rel(runner, evaluator, "Submits results", "Queue")
    Rel(evaluator, builder, "Triggers build", "Event")
    Rel(builder, deployer, "Notifies completion", "Event")
    
    Rel(api, postgres, "Reads/writes data", "SQL")
    Rel(api, redis, "Caches data", "Redis protocol")
    Rel(runner, storage, "Stores artifacts", "S3 API")
    
    Rel(runner, llm, "Generates code", "HTTPS")
    Rel(builder, ghcr, "Pushes images", "Docker Registry API")
    Rel(orchestrator, github, "Commits code", "Git")
```

## Container Descriptions

### Frontend Layer

#### Web UI
- **Technology**: Next.js 13+ with TypeScript
- **Purpose**: Monitoring dashboard and control interface
- **Features**:
  - Real-time pipeline status
  - Research submission interface
  - Deployment management
  - Performance metrics visualization

### API Layer

#### API Gateway
- **Technology**: FastAPI with async Python
- **Purpose**: Central API endpoint for all services
- **Features**:
  - RESTful endpoints
  - WebSocket support for real-time updates
  - Authentication and authorization
  - Rate limiting and caching

### Orchestration Layer

#### Σ-Builder Orchestrator
- **Technology**: Python with Celery
- **Purpose**: Coordinates the entire automation pipeline
- **Responsibilities**:
  - Workflow management
  - Task scheduling
  - State management
  - Error handling and retries

### Research Processing

#### Research Normalizer
- **Technology**: Python
- **Purpose**: Standardizes research input format
- **Functions**:
  - File validation
  - Front-matter parsing
  - Content extraction
  - Structure normalization

#### Prompt Synthesizer
- **Technology**: Python with Jinja2
- **Purpose**: Generates model-specific implementation prompts
- **Features**:
  - Multi-model synthesis
  - Enhancement extraction
  - Requirement compilation
  - Prompt optimization

### Experiment Execution

#### Experiment Runner
- **Technology**: Python with asyncio
- **Purpose**: Executes experiments on different models
- **Capabilities**:
  - Parallel execution
  - Resource management
  - Progress tracking
  - Error recovery

#### Result Evaluator
- **Technology**: Python with NumPy/Pandas
- **Purpose**: Analyzes and scores experiment results
- **Metrics**:
  - Code quality scores
  - Test coverage
  - Performance benchmarks
  - Security scan results

### Deployment Management

#### Image Builder
- **Technology**: Docker Buildx
- **Purpose**: Creates multi-architecture container images
- **Features**:
  - Multi-stage builds
  - Layer caching
  - Security scanning
  - Size optimization

#### Deploy Manager
- **Technology**: Python with Kubernetes client
- **Purpose**: Manages production deployments
- **Functions**:
  - Blue-green deployments
  - Health monitoring
  - Rollback management
  - Traffic shifting

### Data Storage

#### PostgreSQL Database
- **Purpose**: Primary data storage
- **Stores**:
  - User data
  - Experiment results
  - Deployment history
  - System configuration

#### Redis Cache
- **Purpose**: High-speed caching and queuing
- **Uses**:
  - Session storage
  - API response caching
  - Task queue backend
  - Real-time data

#### Object Storage
- **Purpose**: Large file and artifact storage
- **Stores**:
  - Generated code
  - Docker images
  - Logs and metrics
  - Research documents

## Communication Patterns

### Synchronous
- HTTP/HTTPS for API calls
- WebSocket for real-time updates
- gRPC for service-to-service

### Asynchronous
- Message queues for task distribution
- Event bus for system notifications
- Webhooks for external integrations

---

## Next: [Component Diagram](./c4-component.md) 