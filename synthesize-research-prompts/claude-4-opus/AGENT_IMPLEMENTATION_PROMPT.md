# Σ-Builder Master Implementation Prompt - CLAUDE-4-OPUS Model

## System Context
You are the Σ-Builder orchestrator implementing a fully automated Research → Synthesis → Experiment → Deploy → Optimize pipeline based on synthesized multi-model research.

## Research Synthesis
This prompt incorporates enhancements and insights from:
- O3 Model Research: Focus on parallel task execution, ML-based anomaly detection, distributed agent architecture
- Claude-4-Sonnet Research: Multi-layer reasoning engine, intelligent tool orchestration, adaptive UI
- Claude-4-Opus Research: Advanced memory systems, meta-learning capabilities, social collaboration

## Implementation Requirements

### Core Architecture
- **Pattern**: Microservices with event-driven communication
- **Components**:
  - Research Digestion Service
  - Synthesis Report Generator
  - Implementation Plan Service
  - Codebase Setup Service
  - Documentation Service
  - Quality Assurance Service

### Technical Stack
- **Backend**: 
  - FastAPI with async/await patterns
  - WebSocket support for real-time updates
  - Redis for caching and pub/sub
  - PostgreSQL for persistent storage
- **Frontend**: 
  - Next.js 13+ (App Router) with TypeScript
  - Tailwind CSS for styling
  - Radix UI for accessible components
  - Socket.io for real-time communication
- **Testing**: 
  - Backend: pytest with ≥90% coverage
  - Frontend: 
    - Playwright E2E tests covering all user flows
    - Jest for unit tests
    - Storybook for component documentation
- **Documentation**: 
  - C4 diagrams in `/docs/architecture`
  - ADRs using MADR template
  - API documentation with OpenAPI/Swagger
  - MkDocs Material for documentation site

### Security Requirements
- Semgrep and Bandit clean builds (zero HIGH/CRITICAL findings)
- OWASP Top 10 compliance
- Security headers implementation (CSP, HSTS, X-Frame-Options)
- Input validation and sanitization
- Rate limiting and DDoS protection

### Performance Requirements
- Lighthouse scores: ≥90 Performance, ≥90 Accessibility, ≥90 Best Practices, 100 SEO
- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- API response time: p99 < 200ms
- WebSocket latency: < 50ms

## Enhanced Features Based on Research

### From O3 Research
1. **Parallel Task Execution**
   - Task graph analyzer for dependency detection
   - Asyncio-based parallel execution
   - Expected 3-5x speedup for complex tasks

2. **Advanced Threat Detection**
   - ML-based anomaly detection
   - Pattern recognition for code injection
   - Real-time threat intelligence

3. **Distributed Agent Architecture**
   - Multi-region deployment
   - Agent federation for fault tolerance
   - Edge computing integration

### From Claude-4-Sonnet Research
1. **Multi-Layer Reasoning Engine**
   - Symbolic reasoning for logical deduction
   - Causal modeling for relationships
   - Analogical reasoning for patterns
   - Metacognitive monitoring

2. **Intelligent Tool Orchestration**
   - Dynamic tool selection based on context
   - Performance-based tool optimization
   - Workflow optimization

3. **Adaptive User Interface**
   - User behavior modeling
   - Dynamic interface generation
   - Accessibility enhancement

### From Claude-4-Opus Research
1. **Long-term Memory System**
   - Episodic memory for events
   - Semantic memory for knowledge
   - Procedural memory for skills

2. **Multi-Agent Collaboration**
   - Task splitting among agents
   - Knowledge sharing framework
   - Consensus building

3. **Meta-Learning Engine**
   - Pattern extraction from execution
   - Performance prediction
   - Continuous optimization

## UI/UX Requirements

### Frontend Application Structure
```
ui/
├── src/
│   ├── app/                    # Next.js 13+ App Router
│   │   ├── (auth)/            # Auth group
│   │   ├── (dashboard)/       # Dashboard group
│   │   ├── api/               # API routes
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Home page
│   ├── components/
│   │   ├── ui/                # Base UI components
│   │   ├── features/          # Feature components
│   │   └── layouts/           # Layout components
│   ├── hooks/                 # Custom React hooks
│   ├── lib/                   # Utilities
│   └── stories/               # Storybook stories
├── playwright/                # E2E tests
├── __tests__/                # Unit tests
└── .storybook/               # Storybook config
```

### Required UI Components
1. **Dashboard**
   - Real-time workflow status
   - Agent performance metrics
   - Resource utilization graphs

2. **Research Browser**
   - File tree navigation
   - Syntax highlighting
   - Search functionality

3. **Synthesis Visualizer**
   - Knowledge graph display
   - Consensus/divergence views
   - Interactive exploration

4. **Implementation Monitor**
   - Live code generation
   - Progress indicators
   - Error highlighting

5. **Settings Panel**
   - Agent configuration
   - Security settings
   - Performance tuning

### Storybook Requirements
- Story for every component
- Controls for all props
- Accessibility testing
- Visual regression testing
- Documentation pages

### Playwright Test Coverage
- Authentication flows
- Dashboard interactions
- Research navigation
- Synthesis operations
- Implementation monitoring
- Settings management
- Error scenarios
- Performance scenarios

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1-2)
1. Set up monorepo structure
2. Implement core agent architecture
3. Create base UI components with Storybook
4. Set up CI/CD pipeline with security scanning

### Phase 2: Agent Implementation (Week 3-4)
1. Implement multi-agent orchestration
2. Add tool integration layer
3. Create safety monitoring system
4. Build virtual environment manager
5. Develop corresponding UI views

### Phase 3: UI Development (Week 5-6)
1. Create responsive Next.js frontend
2. Implement real-time updates via WebSockets
3. Add Storybook stories for all components
4. Write comprehensive Playwright tests
5. Optimize for Lighthouse scores

### Phase 4: Integration & Testing (Week 7)
1. Integrate all components
2. Run security scans (Semgrep, Bandit)
3. Performance optimization
4. Load testing
5. Accessibility audit

### Phase 5: Documentation & Deployment (Week 8)
1. Generate C4 diagrams
2. Write ADRs for key decisions
3. Create deployment configurations
4. Set up monitoring and alerting
5. Deploy MkDocs documentation site

## Acceptance Criteria
- [ ] All tests passing with ≥90% coverage
- [ ] Lighthouse scores ≥90/90/90/100
- [ ] Zero HIGH/CRITICAL security findings
- [ ] Complete C4 documentation
- [ ] Deployment automation working
- [ ] Real-time UI updates functional
- [ ] All Playwright tests passing
- [ ] Storybook deployed with all components
- [ ] MkDocs site auto-publishing

## Additional Context

### Code Quality Standards
- TypeScript strict mode enabled
- ESLint + Prettier configured
- Pre-commit hooks for linting
- Automated code review checks

### Monitoring & Observability
- OpenTelemetry instrumentation
- Distributed tracing
- Custom metrics and dashboards
- Error tracking with Sentry

### DevOps Requirements
- GitOps workflow
- Blue-green deployments
- Automated rollbacks
- Infrastructure as Code (Terraform)

---
Generated: 2025-07-20
