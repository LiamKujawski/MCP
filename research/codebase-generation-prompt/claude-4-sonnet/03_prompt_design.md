---
topic: "codebase-generation-prompt"
model: "claude-4-sonnet"
stage: research
version: 1
---

# Codebase Generation Prompt Structure - Claude 4 Sonnet Analysis

## Master Orchestration Prompts

### Project-Level Generation Prompt
```
# Codebase Generation Master Prompt

## Project Overview
You are an expert software architect and full-stack developer tasked with generating a complete, production-ready codebase. Your role is to create a comprehensive software project that meets all specified requirements while following industry best practices.

## Generation Principles
1. **Architecture-First**: Begin with solid architectural foundation
2. **Quality Assurance**: Integrate testing and validation throughout
3. **Documentation**: Create comprehensive documentation alongside code
4. **Security**: Implement security best practices from the ground up
5. **Performance**: Optimize for efficiency and scalability
6. **Maintainability**: Write clean, readable, and maintainable code

## Multi-Stage Generation Process
### Stage 1: Architecture Design
- Analyze requirements and constraints
- Design system architecture and component structure
- Define technology stack and dependencies
- Create data models and API specifications

### Stage 2: Project Scaffolding
- Generate project structure and configuration files
- Set up build systems and development tools
- Create base components and utilities
- Establish coding standards and guidelines

### Stage 3: Core Implementation
- Implement business logic and core features
- Create database schemas and migrations
- Develop API endpoints and services
- Build user interfaces and interactions

### Stage 4: Quality Assurance
- Generate comprehensive test suites
- Implement security measures and validation
- Add monitoring and logging capabilities
- Perform code quality checks and optimization

### Stage 5: Documentation and Deployment
- Create technical and user documentation
- Generate deployment configurations
- Set up CI/CD pipelines
- Provide maintenance and upgrade guides

## Context Awareness Requirements
- Maintain consistency across all generated files
- Ensure proper inter-component dependencies
- Apply framework-specific patterns and conventions
- Consider scalability and performance implications
- Integrate security and error handling throughout

## Quality Standards
- Follow language-specific best practices
- Implement comprehensive error handling
- Include proper logging and monitoring
- Ensure test coverage above 80%
- Apply security scanning and validation
- Optimize for performance and resource usage
```

### Component-Level Generation Templates

#### Frontend Component Prompt Template
```python
class FrontendComponentPrompt:
    """Generates prompts for frontend component creation"""
    
    def __init__(self):
        self.framework_templates = {
            'react': self._react_template,
            'vue': self._vue_template,
            'angular': self._angular_template,
            'svelte': self._svelte_template
        }
    
    def generate_component_prompt(self, component_spec: ComponentSpec, 
                                 framework: str, project_context: ProjectContext) -> str:
        """Generate framework-specific component prompt"""
        
        template_func = self.framework_templates.get(framework)
        if not template_func:
            raise UnsupportedFrameworkError(f"Framework {framework} not supported")
        
        return template_func(component_spec, project_context)
    
    def _react_template(self, component_spec: ComponentSpec, 
                       project_context: ProjectContext) -> str:
        return f"""
        # React Component Generation Task
        
        ## Component Specification
        **Name**: {component_spec.name}
        **Type**: {component_spec.type}
        **Purpose**: {component_spec.description}
        
        ## Requirements
        {self._format_requirements(component_spec.requirements)}
        
        ## Project Context
        **Framework**: React {project_context.react_version}
        **State Management**: {project_context.state_management}
        **Styling**: {project_context.styling_solution}
        **Testing**: {project_context.testing_framework}
        
        ## Dependencies Available
        {self._format_dependencies(project_context.dependencies)}
        
        ## Implementation Guidelines
        1. **React Best Practices**:
           - Use functional components with hooks
           - Implement proper prop validation with TypeScript
           - Follow React naming conventions
           - Use React.memo for performance optimization when appropriate
        
        2. **Component Structure**:
           - Separate concerns (logic, presentation, styling)
           - Implement proper error boundaries
           - Add accessibility attributes (ARIA)
           - Include loading and error states
        
        3. **State Management**:
           - Use appropriate state management pattern
           - Implement optimistic updates where applicable
           - Handle asynchronous operations properly
           - Avoid unnecessary re-renders
        
        4. **Testing Requirements**:
           - Unit tests with {project_context.testing_framework}
           - Component integration tests
           - Accessibility tests
           - Visual regression tests
        
        5. **Performance Considerations**:
           - Lazy loading for heavy components
           - Memoization of expensive calculations
           - Proper dependency arrays in hooks
           - Image optimization and lazy loading
        
        ## Expected Deliverables
        - Component implementation with TypeScript
        - Comprehensive test suite
        - Storybook stories for documentation
        - Accessibility compliance
        - Performance optimizations
        
        Generate a complete, production-ready React component that follows all specified requirements and best practices.
        """

class BackendServicePrompt:
    """Generates prompts for backend service creation"""
    
    def __init__(self):
        self.framework_templates = {
            'fastapi': self._fastapi_template,
            'django': self._django_template,
            'express': self._express_template,
            'spring': self._spring_template
        }
    
    def generate_service_prompt(self, service_spec: ServiceSpec, 
                               framework: str, project_context: ProjectContext) -> str:
        """Generate framework-specific service prompt"""
        
        template_func = self.framework_templates.get(framework)
        if not template_func:
            raise UnsupportedFrameworkError(f"Framework {framework} not supported")
        
        return template_func(service_spec, project_context)
    
    def _fastapi_template(self, service_spec: ServiceSpec, 
                         project_context: ProjectContext) -> str:
        return f"""
        # FastAPI Service Generation Task
        
        ## Service Specification
        **Service Name**: {service_spec.name}
        **Domain**: {service_spec.domain}
        **Purpose**: {service_spec.description}
        
        ## API Requirements
        {self._format_api_requirements(service_spec.api_requirements)}
        
        ## Project Context
        **Framework**: FastAPI {project_context.fastapi_version}
        **Database**: {project_context.database}
        **Authentication**: {project_context.auth_method}
        **Caching**: {project_context.caching_solution}
        
        ## Implementation Guidelines
        1. **FastAPI Best Practices**:
           - Use Pydantic models for request/response validation
           - Implement proper dependency injection
           - Add comprehensive API documentation
           - Use async/await for I/O operations
        
        2. **Database Integration**:
           - Use SQLAlchemy for ORM operations
           - Implement proper migrations
           - Add database connection pooling
           - Include transaction management
        
        3. **Security Implementation**:
           - JWT token authentication
           - Role-based access control
           - Input validation and sanitization
           - Rate limiting and CORS configuration
        
        4. **Error Handling**:
           - Custom exception handlers
           - Structured error responses
           - Logging and monitoring integration
           - Graceful degradation strategies
        
        5. **Performance Optimization**:
           - Database query optimization
           - Caching strategies
           - Background task processing
           - Response compression
        
        ## Expected Deliverables
        - Complete FastAPI service implementation
        - Pydantic models for data validation
        - Database models and migrations
        - Comprehensive test suite
        - API documentation and examples
        - Docker configuration
        - Monitoring and logging setup
        
        Generate a production-ready FastAPI service that meets all requirements and follows industry best practices.
        """
```

## Context-Aware Prompt Enhancement

### Dynamic Context Integration
```python
class ContextAwarePromptEnhancer:
    """Enhances prompts with dynamic project context"""
    
    def __init__(self):
        self.context_analyzers = {
            'dependencies': DependencyAnalyzer(),
            'architecture': ArchitectureAnalyzer(),
            'conventions': ConventionAnalyzer(),
            'constraints': ConstraintAnalyzer()
        }
    
    async def enhance_prompt(self, base_prompt: str, 
                           project_context: ProjectContext) -> str:
        """Enhance prompt with relevant project context"""
        
        enhanced_prompt = base_prompt
        
        # Add dependency context
        dependency_context = await self._analyze_dependencies(project_context)
        enhanced_prompt += f"\n\n## Dependency Context\n{dependency_context}"
        
        # Add architectural context
        arch_context = await self._analyze_architecture(project_context)
        enhanced_prompt += f"\n\n## Architectural Context\n{arch_context}"
        
        # Add convention context
        convention_context = await self._analyze_conventions(project_context)
        enhanced_prompt += f"\n\n## Project Conventions\n{convention_context}"
        
        # Add constraint context
        constraint_context = await self._analyze_constraints(project_context)
        enhanced_prompt += f"\n\n## Technical Constraints\n{constraint_context}"
        
        return enhanced_prompt
    
    async def _analyze_dependencies(self, project_context: ProjectContext) -> str:
        """Analyze and format dependency information"""
        
        dependencies = project_context.dependencies
        context_items = []
        
        for dep_category, deps in dependencies.items():
            context_items.append(f"### {dep_category.title()} Dependencies")
            for dep_name, dep_info in deps.items():
                context_items.append(
                    f"- **{dep_name}** ({dep_info.version}): {dep_info.purpose}"
                )
        
        return '\n'.join(context_items)
    
    async def _analyze_architecture(self, project_context: ProjectContext) -> str:
        """Analyze and format architectural patterns"""
        
        architecture = project_context.architecture
        context_items = [
            f"- **Pattern**: {architecture.pattern}",
            f"- **Layers**: {', '.join(architecture.layers)}",
            f"- **Communication**: {architecture.communication_style}",
            f"- **Data Flow**: {architecture.data_flow_pattern}"
        ]
        
        if architecture.design_principles:
            context_items.append("- **Design Principles**:")
            for principle in architecture.design_principles:
                context_items.append(f"  - {principle}")
        
        return '\n'.join(context_items)
```

### Multi-Stage Prompt Orchestration
```python
class MultiStagePromptOrchestrator:
    """Orchestrates prompts across multiple generation stages"""
    
    def __init__(self):
        self.stage_generators = {
            'architecture': ArchitecturePromptGenerator(),
            'scaffolding': ScaffoldingPromptGenerator(),
            'implementation': ImplementationPromptGenerator(),
            'testing': TestingPromptGenerator(),
            'documentation': DocumentationPromptGenerator()
        }
    
    async def orchestrate_generation(self, project_requirements: ProjectRequirements) -> GenerationPlan:
        """Create orchestrated generation plan with stage-specific prompts"""
        
        generation_plan = GenerationPlan()
        
        # Stage 1: Architecture Design
        arch_prompt = await self.stage_generators['architecture'].generate_prompt(
            project_requirements
        )
        generation_plan.add_stage('architecture', arch_prompt)
        
        # Stage 2: Project Scaffolding
        scaffolding_prompt = await self.stage_generators['scaffolding'].generate_prompt(
            project_requirements, dependencies=['architecture']
        )
        generation_plan.add_stage('scaffolding', scaffolding_prompt)
        
        # Stage 3: Implementation
        for component in project_requirements.components:
            impl_prompt = await self.stage_generators['implementation'].generate_prompt(
                component, dependencies=['architecture', 'scaffolding']
            )
            generation_plan.add_stage(f'implementation_{component.name}', impl_prompt)
        
        # Stage 4: Testing
        test_prompt = await self.stage_generators['testing'].generate_prompt(
            project_requirements, dependencies=['implementation']
        )
        generation_plan.add_stage('testing', test_prompt)
        
        # Stage 5: Documentation
        doc_prompt = await self.stage_generators['documentation'].generate_prompt(
            project_requirements, dependencies=['implementation', 'testing']
        )
        generation_plan.add_stage('documentation', doc_prompt)
        
        return generation_plan

class ArchitecturePromptGenerator:
    """Generates architecture-specific prompts"""
    
    async def generate_prompt(self, project_requirements: ProjectRequirements) -> str:
        """Generate architecture design prompt"""
        
        return f"""
        # System Architecture Design Task
        
        ## Project Requirements
        **Name**: {project_requirements.name}
        **Type**: {project_requirements.type}
        **Scale**: {project_requirements.expected_scale}
        **Users**: {project_requirements.user_base}
        
        ## Functional Requirements
        {self._format_functional_requirements(project_requirements.functional_requirements)}
        
        ## Non-Functional Requirements
        {self._format_nonfunctional_requirements(project_requirements.nonfunctional_requirements)}
        
        ## Technical Constraints
        {self._format_constraints(project_requirements.constraints)}
        
        ## Architecture Design Process
        1. **System Analysis**:
           - Analyze requirements and identify core domains
           - Determine system boundaries and interfaces
           - Identify key architectural drivers
           - Assess technical and business constraints
        
        2. **Architecture Selection**:
           - Choose appropriate architectural pattern (microservices, monolith, etc.)
           - Select technology stack based on requirements
           - Design data storage and management strategy
           - Plan integration and communication patterns
        
        3. **Component Design**:
           - Define major system components and their responsibilities
           - Design component interfaces and contracts
           - Plan data flow and processing pipelines
           - Identify shared services and utilities
        
        4. **Quality Attributes**:
           - Design for scalability and performance requirements
           - Plan security architecture and access control
           - Design for reliability and fault tolerance
           - Plan monitoring and observability strategy
        
        ## Expected Deliverables
        - High-level system architecture diagram
        - Component decomposition and responsibilities
        - Technology stack recommendations with justifications
        - Data architecture and storage strategy
        - API design guidelines and standards
        - Security architecture and threat model
        - Deployment and infrastructure recommendations
        - Development and testing strategy
        
        Design a comprehensive system architecture that meets all requirements while following industry best practices for scalability, security, and maintainability.
        """
```

## Quality Assurance Integration

### Testing Strategy Prompts
```python
class TestingPromptGenerator:
    """Generates comprehensive testing strategy prompts"""
    
    async def generate_testing_prompt(self, codebase_context: CodebaseContext) -> str:
        """Generate comprehensive testing strategy prompt"""
        
        return f"""
        # Comprehensive Testing Strategy Implementation
        
        ## Codebase Context
        **Architecture**: {codebase_context.architecture_pattern}
        **Components**: {len(codebase_context.components)} components
        **Technology Stack**: {', '.join(codebase_context.tech_stack)}
        **Testing Framework**: {codebase_context.testing_framework}
        
        ## Testing Pyramid Implementation
        
        ### Unit Testing (70% of tests)
        **Scope**: Individual functions, methods, and classes
        **Framework**: {codebase_context.unit_testing_framework}
        **Coverage Target**: 90%+ for business logic
        
        **Requirements**:
        - Test all public methods and functions
        - Cover edge cases and error conditions
        - Mock external dependencies
        - Use parameterized tests for multiple scenarios
        - Include performance benchmarks for critical functions
        
        ### Integration Testing (20% of tests)
        **Scope**: Component interactions and external integrations
        **Framework**: {codebase_context.integration_testing_framework}
        **Coverage Target**: 80%+ for integration points
        
        **Requirements**:
        - Test database interactions and transactions
        - Validate API contract compliance
        - Test external service integrations
        - Verify data transformation pipelines
        - Include failure scenario testing
        
        ### End-to-End Testing (10% of tests)
        **Scope**: Complete user workflows and business processes
        **Framework**: {codebase_context.e2e_testing_framework}
        **Coverage Target**: 100% of critical user journeys
        
        **Requirements**:
        - Test complete user workflows
        - Validate business rule enforcement
        - Test cross-browser compatibility (if applicable)
        - Include performance and load testing
        - Verify security controls and access restrictions
        
        ## Specialized Testing Categories
        
        ### Security Testing
        - Input validation and sanitization
        - Authentication and authorization
        - SQL injection and XSS prevention
        - API security and rate limiting
        - Data encryption and privacy
        
        ### Performance Testing
        - Load testing for expected traffic
        - Stress testing for peak conditions
        - Database query performance
        - API response time validation
        - Resource utilization monitoring
        
        ### Accessibility Testing
        - WCAG 2.1 compliance validation
        - Screen reader compatibility
        - Keyboard navigation testing
        - Color contrast verification
        - Focus management validation
        
        ## Test Data Management
        - Synthetic test data generation
        - Database seeding and cleanup
        - Test environment isolation
        - Data privacy and anonymization
        - Version-controlled test fixtures
        
        ## Continuous Testing Integration
        - Pre-commit hook validation
        - CI/CD pipeline integration
        - Automated test execution
        - Test result reporting
        - Quality gate enforcement
        
        ## Expected Deliverables
        Generate a complete testing suite that includes:
        - Comprehensive unit test coverage
        - Integration tests for all component interactions
        - End-to-end tests for critical user journeys
        - Performance and load tests
        - Security vulnerability tests
        - Accessibility compliance tests
        - Test data management utilities
        - CI/CD integration configuration
        - Test documentation and maintenance guides
        
        Ensure all tests are maintainable, reliable, and provide meaningful feedback for development teams.
        """
```

This comprehensive prompt structure framework enables the generation of high-quality, production-ready codebases through sophisticated prompt engineering and context-aware generation strategies.