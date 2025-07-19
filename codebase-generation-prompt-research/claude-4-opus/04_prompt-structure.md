# Codebase Generation Prompt Structure Research (Claude 4 Opus)

## Overview

This document details optimal prompt structures for codebase generation using Claude 4 Opus, focusing on producing production-ready, maintainable code.

## Hierarchical Prompt Architecture

### 1. System-Level Context

```yaml
system_context:
  role: "Expert software architect and full-stack developer"
  expertise:
    - "Clean architecture principles"
    - "Design patterns"
    - "Performance optimization"
    - "Security best practices"
  
  generation_principles:
    - "Write production-ready code"
    - "Include comprehensive error handling"
    - "Follow SOLID principles"
    - "Ensure type safety"
```

### 2. Project-Level Context

```typescript
interface ProjectContext {
  metadata: {
    name: string;
    type: 'web' | 'api' | 'mobile' | 'desktop';
    version: string;
    license: string;
  };
  
  architecture: {
    pattern: 'microservices' | 'monolithic' | 'serverless';
    layers: Layer[];
    components: Component[];
  };
  
  technology: {
    languages: string[];
    frameworks: Framework[];
    databases: Database[];
    tools: Tool[];
  };
  
  standards: {
    coding: CodingStandard;
    testing: TestingStandard;
    documentation: DocStandard;
  };
}
```

### 3. Feature-Level Prompting

```python
class FeaturePrompt:
    def __init__(self, feature_spec: FeatureSpecification):
        self.spec = feature_spec
        self.context = self.load_project_context()
        
    def generate_prompt(self) -> str:
        return f"""
        Generate a complete implementation for: {self.spec.name}
        
        Requirements:
        {self.format_requirements(self.spec.requirements)}
        
        Technical Constraints:
        {self.format_constraints(self.spec.constraints)}
        
        Integration Points:
        {self.format_integrations(self.spec.integrations)}
        
        Expected Deliverables:
        1. Data models with validation
        2. Business logic services
        3. API endpoints with documentation
        4. Comprehensive test suite
        5. Database migrations
        6. Error handling and logging
        """
```

## Advanced Prompt Patterns

### 1. Specification-Driven Generation

```yaml
specification_prompt:
  input:
    type: "OpenAPI"
    schema: |
      openapi: 3.0.0
      paths:
        /users:
          post:
            summary: Create user
            requestBody:
              required: true
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/UserCreate'
  
  output_requirements:
    - "Generate complete API implementation"
    - "Include validation middleware"
    - "Add authentication/authorization"
    - "Create integration tests"
    - "Generate API documentation"
```

### 2. Example-Driven Generation

```typescript
const exampleDrivenPrompt = {
  task: "Generate a real-time notification system",
  
  examples: [
    {
      description: "WebSocket connection handler",
      code: `
        class WebSocketManager {
          private connections: Map<string, WebSocket>;
          
          async handleConnection(ws: WebSocket, userId: string) {
            this.connections.set(userId, ws);
            await this.sendPendingNotifications(userId);
          }
        }
      `
    }
  ],
  
  requirements: [
    "Support multiple notification channels",
    "Implement retry logic",
    "Add rate limiting",
    "Ensure message ordering"
  ]
};
```

### 3. Incremental Generation Strategy

```python
class IncrementalGenerator:
    def __init__(self):
        self.generation_phases = [
            "data_models",
            "repository_layer",
            "service_layer",
            "api_layer",
            "test_suite",
            "documentation"
        ]
        
    async def generate_codebase(self, spec: Specification):
        generated_code = {}
        context = {"spec": spec}
        
        for phase in self.generation_phases:
            prompt = self.build_phase_prompt(phase, context)
            code = await self.generate_phase(prompt)
            
            # Validate before proceeding
            if not self.validate_phase(code, phase):
                code = await self.fix_and_regenerate(code, phase)
            
            generated_code[phase] = code
            context[phase] = code  # Add to context for next phases
            
        return self.assemble_codebase(generated_code)
```

## Optimization Techniques

### 1. Context Window Management

```typescript
class ContextOptimizer {
  private readonly MAX_TOKENS = 100000;
  private readonly PRIORITY_WEIGHTS = {
    requirements: 0.3,
    examples: 0.25,
    existing_code: 0.25,
    patterns: 0.2
  };
  
  optimize(context: Context): OptimizedContext {
    const prioritized = this.prioritizeContent(context);
    const compressed = this.compressContent(prioritized);
    
    return this.ensureTokenLimit(compressed);
  }
  
  private compressContent(content: Content): CompressedContent {
    return {
      ...content,
      code: this.compressCode(content.code),
      docs: this.summarizeDocs(content.docs)
    };
  }
}
```

### 2. Template-Based Generation

```yaml
templates:
  microservice:
    structure:
      - src/
        - controllers/
        - services/
        - repositories/
        - models/
        - utils/
      - tests/
      - docs/
    
    prompts:
      controller: |
        Generate a REST controller for {entity}:
        - CRUD operations
        - Input validation
        - Error handling
        - OpenAPI annotations
        
      service: |
        Generate business logic service for {entity}:
        - Transaction management
        - Business rules validation
        - Event publishing
        - Caching strategy
```

## Quality Assurance Patterns

### 1. Validation Prompts

```python
def create_validation_prompt(generated_code: str, requirements: List[str]) -> str:
    return f"""
    Review the generated code and verify:
    
    1. All requirements are met:
    {format_requirements(requirements)}
    
    2. Code quality checks:
    - No syntax errors
    - Proper error handling
    - Consistent naming conventions
    - Adequate comments
    
    3. Security considerations:
    - Input validation
    - SQL injection prevention
    - Authentication checks
    - Sensitive data handling
    
    Provide a detailed report with any issues found.
    """
```

### 2. Self-Correction Loop

```typescript
async function selfCorrectingGeneration(
  initialPrompt: string,
  validator: CodeValidator
): Promise<GeneratedCode> {
  let code = await generateCode(initialPrompt);
  let attempts = 0;
  
  while (attempts < MAX_ATTEMPTS) {
    const validation = await validator.validate(code);
    
    if (validation.isValid) {
      return code;
    }
    
    const fixPrompt = createFixPrompt(code, validation.errors);
    code = await generateCode(fixPrompt);
    attempts++;
  }
  
  throw new Error('Failed to generate valid code');
}
```

## Performance Metrics

### Prompt Effectiveness Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| First-Pass Success | > 85% | Validation pass rate |
| Code Quality Score | > 90% | Linting + complexity |
| Test Coverage | > 80% | Coverage tools |
| Generation Speed | < 30s | End-to-end timing |

## Best Practices

### 1. Prompt Structure Guidelines
- Start with clear objective statement
- Provide comprehensive context
- Include specific requirements
- Define success criteria
- Add relevant examples

### 2. Context Inclusion Strategy
- Recent project changes
- Existing code patterns
- Team conventions
- Performance requirements
- Security policies

### 3. Output Specification
- File structure expectations
- Code formatting rules
- Documentation requirements
- Test case expectations
- Error handling patterns

## Conclusion

Effective codebase generation requires carefully structured prompts that balance comprehensiveness with clarity. By following these patterns and continuously refining based on outcomes, we can achieve high-quality, production-ready code generation.
