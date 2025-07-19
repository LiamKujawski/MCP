# Codebase Generation Prompt Structure Design

## Hierarchical Prompt Architecture

### Master Prompt Framework

#### System-Level Orchestration Prompt
```python
class SystemOrchestrationPrompt:
    """
    Master prompt template for coordinating entire codebase generation process
    """
    
    SYSTEM_PROMPT = """
    # Codebase Generation System
    
    You are an expert software architect and full-stack developer tasked with generating 
    a complete, production-ready codebase. Your expertise spans:
    
    ## Core Competencies
    - **Architecture Design**: Microservices, monoliths, serverless, and hybrid architectures
    - **Technology Integration**: Modern frameworks, databases, cloud services, and DevOps tools
    - **Quality Assurance**: Testing strategies, security best practices, and performance optimization
    - **Developer Experience**: Tooling, documentation, and maintainable code organization
    
    ## Generation Principles
    1. **Scalability First**: Design for growth and changing requirements
    2. **Security by Design**: Implement security best practices from the ground up
    3. **Developer Productivity**: Optimize for team efficiency and code maintainability
    4. **Performance Optimization**: Build with performance considerations integrated
    5. **Documentation Excellence**: Generate comprehensive, useful documentation
    
    ## Code Quality Standards
    - Follow language-specific best practices and style guides
    - Implement comprehensive error handling and logging
    - Write self-documenting code with clear naming conventions
    - Include extensive test coverage (unit, integration, and e2e)
    - Apply SOLID principles and appropriate design patterns
    
    ## Generation Workflow
    1. **Architecture Planning**: Design system architecture and component relationships
    2. **Technology Selection**: Choose optimal technology stack for requirements
    3. **Component Generation**: Create individual system components
    4. **Integration Layer**: Build connections between components
    5. **Testing Suite**: Generate comprehensive test coverage
    6. **Documentation**: Create developer and user documentation
    7. **Deployment**: Set up CI/CD and deployment configurations
    """
    
    def generate_orchestration_prompt(self, project_requirements: ProjectRequirements) -> str:
        return f"""
        {self.SYSTEM_PROMPT}
        
        # Project Specification
        
        ## Project Overview
        - **Name**: {project_requirements.name}
        - **Type**: {project_requirements.type}
        - **Domain**: {project_requirements.domain}
        - **Scale**: {project_requirements.scale}
        - **Timeline**: {project_requirements.timeline}
        
        ## Functional Requirements
        {self._format_requirements(project_requirements.functional_requirements)}
        
        ## Non-Functional Requirements
        {self._format_requirements(project_requirements.non_functional_requirements)}
        
        ## Technology Constraints
        {self._format_constraints(project_requirements.technology_constraints)}
        
        ## Quality Requirements
        {self._format_quality_requirements(project_requirements.quality_requirements)}
        
        # Generation Instructions
        
        ## Phase 1: Architecture Design
        1. Analyze requirements and identify system boundaries
        2. Design high-level architecture and select architectural patterns
        3. Identify major system components and their responsibilities
        4. Define component interfaces and data flow
        5. Create architecture documentation
        
        ## Phase 2: Technology Stack Selection
        1. Evaluate technology options against requirements
        2. Select optimal frameworks, libraries, and tools
        3. Consider integration complexity and team expertise
        4. Document technology decisions and rationale
        
        ## Phase 3: Implementation Generation
        1. Generate project structure and configuration
        2. Implement core system components
        3. Create integration layers and APIs
        4. Generate comprehensive test suites
        5. Set up development tooling and workflows
        
        ## Phase 4: Quality Assurance
        1. Implement security measures and scanning
        2. Set up performance monitoring and optimization
        3. Generate documentation and deployment guides
        4. Create CI/CD pipelines and deployment automation
        
        Begin with Phase 1: Architecture Design. Provide a comprehensive architectural plan 
        before proceeding to implementation.
        """
```

### Component-Level Prompt Templates

#### Frontend Component Generation
```python
class FrontendComponentPrompt:
    """
    Specialized prompt template for frontend component generation
    """
    
    def __init__(self):
        self.framework_templates = {
            'react': ReactComponentTemplate(),
            'vue': VueComponentTemplate(),
            'angular': AngularComponentTemplate(),
            'svelte': SvelteComponentTemplate()
        }
    
    def generate_component_prompt(self, component_spec: ComponentSpec, 
                                framework: str, context: SystemContext) -> str:
        
        template = self.framework_templates[framework]
        
        return f"""
        # Frontend Component Generation: {component_spec.name}
        
        ## Component Specification
        - **Type**: {component_spec.type}
        - **Framework**: {framework}
        - **Complexity**: {component_spec.complexity}
        - **Reusability**: {component_spec.reusability_level}
        
        ## Functional Requirements
        {self._format_functional_requirements(component_spec)}
        
        ## UI/UX Requirements
        {self._format_ui_requirements(component_spec)}
        
        ## Integration Requirements
        {self._format_integration_requirements(component_spec, context)}
        
        ## Implementation Guidelines
        
        ### Component Structure
        {template.get_structure_guidelines()}
        
        ### State Management
        {template.get_state_management_guidelines(component_spec)}
        
        ### Styling Approach
        {template.get_styling_guidelines(component_spec)}
        
        ### Accessibility Requirements
        - Implement ARIA labels and roles
        - Ensure keyboard navigation support
        - Maintain color contrast ratios (WCAG 2.1 AA)
        - Support screen reader compatibility
        
        ### Performance Optimization
        - Implement React.memo() or equivalent optimization
        - Use lazy loading for heavy components
        - Optimize bundle size and rendering performance
        - Implement proper error boundaries
        
        ### Testing Requirements
        {template.get_testing_guidelines(component_spec)}
        
        ## Code Generation Instructions
        
        1. **Component Implementation**
           - Create main component with proper TypeScript types
           - Implement all required functionality with error handling
           - Apply consistent naming conventions and code style
           - Include comprehensive JSDoc documentation
        
        2. **Styling Implementation**
           - Create component-specific styles
           - Implement responsive design patterns
           - Follow design system guidelines
           - Ensure cross-browser compatibility
        
        3. **Test Implementation**
           - Write unit tests for all component logic
           - Create integration tests for user interactions
           - Include accessibility testing
           - Generate test fixtures and mock data
        
        4. **Documentation Generation**
           - Create Storybook stories or equivalent
           - Document component props and usage examples
           - Include design specifications and guidelines
        
        Generate a complete, production-ready component implementation.
        """

class ReactComponentTemplate:
    """
    React-specific component template and guidelines
    """
    
    def get_structure_guidelines(self) -> str:
        return """
        ### React Component Structure
        ```
        ComponentName/
        ├── index.ts                 # Export barrel
        ├── ComponentName.tsx        # Main component
        ├── ComponentName.module.css # Styles
        ├── ComponentName.test.tsx   # Tests
        ├── ComponentName.stories.tsx # Storybook
        ├── hooks/                   # Component-specific hooks
        ├── types.ts                 # TypeScript definitions
        └── utils.ts                 # Helper functions
        ```
        
        ### Component Implementation Pattern
        - Use functional components with hooks
        - Implement proper TypeScript interfaces for props
        - Use React.memo() for performance optimization
        - Implement proper error boundaries where needed
        """
    
    def get_state_management_guidelines(self, spec: ComponentSpec) -> str:
        if spec.complexity == 'high':
            return """
            ### State Management (Complex Component)
            - Use useReducer for complex state logic
            - Implement custom hooks for state management
            - Consider React Query for server state
            - Use React Context for component tree state sharing
            """
        else:
            return """
            ### State Management (Simple Component)
            - Use useState for local component state
            - Implement useEffect for side effects
            - Use custom hooks for reusable logic
            - Lift state up when needed for parent communication
            """
```

#### Backend Service Generation
```python
class BackendServicePrompt:
    """
    Specialized prompt template for backend service generation
    """
    
    def generate_service_prompt(self, service_spec: ServiceSpec, 
                              architecture: SystemArchitecture) -> str:
        return f"""
        # Backend Service Generation: {service_spec.name}
        
        ## Service Specification
        - **Type**: {service_spec.type}
        - **Framework**: {service_spec.framework}
        - **Database**: {service_spec.database_type}
        - **Scale**: {service_spec.expected_scale}
        
        ## Service Responsibilities
        {self._format_service_responsibilities(service_spec)}
        
        ## API Specification
        {self._format_api_specification(service_spec)}
        
        ## Data Model Requirements
        {self._format_data_model(service_spec)}
        
        ## Integration Requirements
        {self._format_service_integrations(service_spec, architecture)}
        
        ## Implementation Framework
        
        ### Service Architecture Pattern
        ```
        {service_spec.name}/
        ├── src/
        │   ├── controllers/         # HTTP request handlers
        │   ├── services/           # Business logic layer
        │   ├── repositories/       # Data access layer
        │   ├── models/             # Data models and schemas
        │   ├── middleware/         # Cross-cutting concerns
        │   ├── utils/              # Helper functions
        │   ├── config/             # Configuration management
        │   └── types/              # TypeScript definitions
        ├── tests/
        │   ├── unit/               # Unit tests
        │   ├── integration/        # Integration tests
        │   └── e2e/                # End-to-end tests
        ├── docs/                   # Service documentation
        └── deployment/             # Docker and K8s configs
        ```
        
        ### Implementation Guidelines
        
        #### 1. Controller Layer
        - Implement RESTful API endpoints
        - Apply proper HTTP status codes and error handling
        - Implement request validation and sanitization
        - Add comprehensive API documentation (OpenAPI/Swagger)
        
        #### 2. Service Layer
        - Implement business logic with single responsibility
        - Apply appropriate design patterns (Strategy, Factory, etc.)
        - Implement proper error handling and logging
        - Use dependency injection for testability
        
        #### 3. Repository Layer
        - Implement data access patterns
        - Use query optimization and caching strategies
        - Implement proper transaction management
        - Apply database migration and seeding strategies
        
        #### 4. Security Implementation
        - Implement authentication and authorization
        - Apply input validation and sanitization
        - Use secure coding practices (OWASP guidelines)
        - Implement rate limiting and abuse prevention
        
        #### 5. Performance Optimization
        - Implement caching strategies (Redis, in-memory)
        - Use connection pooling and resource management
        - Apply database query optimization
        - Implement proper monitoring and metrics
        
        #### 6. Testing Strategy
        - Write comprehensive unit tests (>90% coverage)
        - Implement integration tests for API endpoints
        - Create end-to-end tests for critical workflows
        - Use test fixtures and factories for data setup
        
        ## Code Generation Instructions
        
        1. **Project Setup**
           - Generate project structure and configuration files
           - Set up dependency management and build tools
           - Configure development and production environments
           - Implement logging and monitoring setup
        
        2. **Core Implementation**
           - Generate all controller, service, and repository classes
           - Implement data models with proper validation
           - Create middleware for cross-cutting concerns
           - Set up database connections and migrations
        
        3. **API Documentation**
           - Generate OpenAPI/Swagger specifications
           - Create comprehensive API documentation
           - Include usage examples and response schemas
           - Set up API testing tools (Postman collections)
        
        4. **Testing Suite**
           - Generate complete test suite with high coverage
           - Create test utilities and mock factories
           - Set up test database and fixtures
           - Implement CI/CD testing pipelines
        
        5. **Deployment Configuration**
           - Create Docker containers and compositions
           - Generate Kubernetes manifests
           - Set up environment-specific configurations
           - Implement health checks and monitoring
        
        Generate a complete, production-ready service implementation.
        """
```

### Advanced Prompt Techniques

#### Context-Aware Prompt Enhancement
```python
class ContextAwarePromptEnhancer:
    """
    Enhances prompts with contextual information and dynamic adaptations
    """
    
    def __init__(self):
        self.context_analyzers = {
            'codebase': CodebaseContextAnalyzer(),
            'dependencies': DependencyContextAnalyzer(),
            'patterns': PatternContextAnalyzer(),
            'performance': PerformanceContextAnalyzer()
        }
    
    def enhance_prompt(self, base_prompt: str, context: GenerationContext) -> EnhancedPrompt:
        """
        Enhance prompt with relevant contextual information
        """
        
        enhanced_sections = []
        
        # Add existing codebase context
        if context.existing_codebase:
            codebase_context = self.context_analyzers['codebase'].analyze(
                context.existing_codebase
            )
            enhanced_sections.append(self._format_codebase_context(codebase_context))
        
        # Add dependency context
        dependency_context = self.context_analyzers['dependencies'].analyze(
            context.project_dependencies
        )
        enhanced_sections.append(self._format_dependency_context(dependency_context))
        
        # Add pattern recommendations
        pattern_context = self.context_analyzers['patterns'].analyze(
            context.architectural_requirements
        )
        enhanced_sections.append(self._format_pattern_context(pattern_context))
        
        # Add performance considerations
        performance_context = self.context_analyzers['performance'].analyze(
            context.performance_requirements
        )
        enhanced_sections.append(self._format_performance_context(performance_context))
        
        return EnhancedPrompt(
            base_prompt=base_prompt,
            context_sections=enhanced_sections,
            full_prompt=self._merge_prompt_sections(base_prompt, enhanced_sections)
        )
    
    def _format_codebase_context(self, context: CodebaseContext) -> str:
        return f"""
        ## Existing Codebase Context
        
        ### Current Architecture
        - **Pattern**: {context.architectural_pattern}
        - **Languages**: {', '.join(context.languages)}
        - **Frameworks**: {', '.join(context.frameworks)}
        - **Database**: {context.database_systems}
        
        ### Code Style Guidelines
        {self._format_style_guidelines(context.style_guidelines)}
        
        ### Existing Components
        {self._format_existing_components(context.components)}
        
        ### Integration Points
        {self._format_integration_points(context.integration_points)}
        
        ### Consistency Requirements
        - Follow existing naming conventions: {context.naming_conventions}
        - Maintain architectural patterns: {context.architectural_patterns}
        - Use established error handling patterns: {context.error_handling_patterns}
        - Follow existing testing strategies: {context.testing_strategies}
        """
```

#### Multi-Stage Prompt Orchestration
```python
class MultiStagePromptOrchestrator:
    """
    Orchestrates complex generation tasks across multiple prompt stages
    """
    
    def __init__(self):
        self.stage_managers = {
            'planning': PlanningStageManager(),
            'architecture': ArchitectureStageManager(),
            'implementation': ImplementationStageManager(),
            'testing': TestingStageManager(),
            'documentation': DocumentationStageManager()
        }
    
    def orchestrate_generation(self, project_spec: ProjectSpecification) -> GenerationPlan:
        """
        Create multi-stage generation plan with dependent prompts
        """
        
        stages = []
        
        # Stage 1: Project Planning
        planning_stage = self.stage_managers['planning'].create_stage(
            project_spec=project_spec,
            inputs=[],
            outputs=['project_plan', 'technology_stack', 'architecture_outline']
        )
        stages.append(planning_stage)
        
        # Stage 2: Architecture Design
        architecture_stage = self.stage_managers['architecture'].create_stage(
            project_spec=project_spec,
            inputs=['project_plan', 'technology_stack'],
            outputs=['system_architecture', 'component_specifications', 'api_definitions']
        )
        stages.append(architecture_stage)
        
        # Stage 3: Implementation
        implementation_stage = self.stage_managers['implementation'].create_stage(
            project_spec=project_spec,
            inputs=['system_architecture', 'component_specifications', 'api_definitions'],
            outputs=['source_code', 'configuration_files', 'build_scripts']
        )
        stages.append(implementation_stage)
        
        # Stage 4: Testing
        testing_stage = self.stage_managers['testing'].create_stage(
            project_spec=project_spec,
            inputs=['source_code', 'component_specifications'],
            outputs=['test_suites', 'test_data', 'testing_documentation']
        )
        stages.append(testing_stage)
        
        # Stage 5: Documentation
        documentation_stage = self.stage_managers['documentation'].create_stage(
            project_spec=project_spec,
            inputs=['source_code', 'system_architecture', 'api_definitions'],
            outputs=['technical_documentation', 'user_guides', 'deployment_guides']
        )
        stages.append(documentation_stage)
        
        return GenerationPlan(
            stages=stages,
            dependencies=self._build_dependency_graph(stages),
            execution_strategy=self._determine_execution_strategy(stages)
        )

class ArchitectureStageManager:
    """
    Manages architecture design stage with specialized prompts
    """
    
    def create_stage(self, project_spec: ProjectSpecification, 
                    inputs: List[str], outputs: List[str]) -> GenerationStage:
        
        stage_prompt = f"""
        # Architecture Design Stage
        
        ## Inputs from Previous Stages
        {self._format_stage_inputs(inputs)}
        
        ## Architecture Design Requirements
        
        ### System Requirements Analysis
        Based on the project plan, analyze and design:
        
        1. **System Boundaries and Context**
           - Define system scope and external interfaces
           - Identify system actors and their interactions
           - Map system context and environment dependencies
        
        2. **Architectural Pattern Selection**
           - Evaluate architectural patterns against requirements
           - Select primary and supporting patterns
           - Document pattern selection rationale
        
        3. **Component Identification and Design**
           - Identify major system components
           - Define component responsibilities and interfaces
           - Design component interaction patterns
        
        4. **Data Architecture**
           - Design data models and relationships
           - Select appropriate data storage solutions
           - Define data flow and transformation patterns
        
        5. **Integration Architecture**
           - Design API specifications and contracts
           - Define integration patterns and protocols
           - Plan for third-party service integrations
        
        ## Output Requirements
        Generate comprehensive architecture documentation including:
        
        ### System Architecture Document
        - High-level system overview and context
        - Component diagram with relationships
        - Data flow diagrams
        - Deployment architecture
        
        ### Component Specifications
        - Detailed component descriptions
        - Interface definitions and contracts
        - Performance and scalability requirements
        - Security and compliance considerations
        
        ### API Definitions
        - RESTful API specifications (OpenAPI format)
        - GraphQL schemas (if applicable)
        - Message queue and event specifications
        - Authentication and authorization schemes
        
        ## Design Principles to Follow
        - **Scalability**: Design for horizontal and vertical scaling
        - **Maintainability**: Create modular, loosely coupled components
        - **Security**: Implement security by design principles
        - **Performance**: Consider performance implications in design decisions
        - **Reliability**: Design for fault tolerance and resilience
        
        Proceed with systematic architecture design following these guidelines.
        """
        
        return GenerationStage(
            name='architecture_design',
            prompt=stage_prompt,
            inputs=inputs,
            outputs=outputs,
            validation_criteria=self._define_architecture_validation_criteria(),
            success_metrics=self._define_architecture_success_metrics()
        )
```

This comprehensive prompt structure design provides a robust framework for generating high-quality codebases through carefully orchestrated, context-aware prompt engineering that ensures consistency, quality, and maintainability across all generated components.