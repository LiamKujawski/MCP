# Codebase Generation Prompt - Setup and Organization

## Repository Structure for Generated Projects

### Intelligent Project Scaffolding

#### Dynamic Project Structure Generation
```python
class IntelligentProjectScaffolder:
    """
    Generates optimized project structures based on requirements and best practices
    """
    
    def __init__(self):
        self.structure_templates = ProjectStructureTemplates()
        self.dependency_analyzer = DependencyAnalyzer()
        self.best_practices_engine = BestPracticesEngine()
        self.technology_advisors = TechnologyAdvisors()
    
    def generate_project_structure(self, project_spec: ProjectSpecification) -> ProjectStructure:
        """
        Generate optimal project structure based on specifications
        """
        
        # Analyze technology stack requirements
        tech_analysis = self.technology_advisors.analyze_stack(project_spec)
        
        # Select appropriate base template
        base_template = self.structure_templates.select_template(
            project_type=project_spec.type,
            scale=project_spec.scale,
            technology_stack=tech_analysis.primary_technologies
        )
        
        # Apply best practices customizations
        customized_structure = self.best_practices_engine.apply_customizations(
            base_template, project_spec, tech_analysis
        )
        
        # Generate dependency configuration
        dependency_config = self.dependency_analyzer.generate_dependency_config(
            customized_structure, tech_analysis
        )
        
        return ProjectStructure(
            directory_tree=customized_structure.directory_tree,
            configuration_files=customized_structure.configuration_files,
            dependency_files=dependency_config,
            build_scripts=customized_structure.build_scripts,
            documentation_structure=customized_structure.documentation_structure
        )
```

#### Technology-Specific Structure Templates
```python
class TechnologyStructureTemplates:
    """
    Technology-specific project structure templates
    """
    
    def get_react_typescript_structure(self, scale: ProjectScale) -> DirectoryStructure:
        """
        Generate React + TypeScript project structure
        """
        
        if scale == ProjectScale.ENTERPRISE:
            return DirectoryStructure({
                "src/": {
                    "components/": {
                        "common/": ["Button/", "Input/", "Modal/"],
                        "feature/": ["UserManagement/", "Dashboard/", "Reports/"],
                        "layout/": ["Header/", "Sidebar/", "Footer/"]
                    },
                    "hooks/": ["useAuth.ts", "useApi.ts", "useLocalStorage.ts"],
                    "services/": ["api/", "auth/", "storage/", "validation/"],
                    "utils/": ["helpers/", "constants/", "types/"],
                    "store/": ["slices/", "middleware/", "selectors/"],
                    "pages/": ["Home/", "Login/", "Dashboard/", "Profile/"],
                    "assets/": ["images/", "styles/", "fonts/"],
                    "tests/": ["__mocks__/", "utils/", "fixtures/"]
                },
                "public/": ["index.html", "manifest.json", "robots.txt"],
                "docs/": ["architecture/", "api/", "deployment/", "development/"],
                "scripts/": ["build/", "deployment/", "testing/"],
                "config/": ["webpack/", "jest/", "eslint/", "prettier/"]
            })
        else:
            return self._get_standard_react_structure()
    
    def get_microservices_structure(self, services: List[str]) -> DirectoryStructure:
        """
        Generate microservices architecture structure
        """
        
        structure = {
            "services/": {},
            "shared/": {
                "libs/": ["auth/", "logging/", "metrics/", "validation/"],
                "types/": ["common.ts", "events.ts", "api.ts"],
                "utils/": ["helpers/", "constants/", "config/"]
            },
            "infrastructure/": {
                "kubernetes/": ["base/", "staging/", "production/"],
                "docker/": ["services/", "shared/"],
                "terraform/": ["modules/", "environments/"],
                "monitoring/": ["prometheus/", "grafana/", "alerting/"]
            },
            "docs/": {
                "architecture/": ["system-design.md", "service-map.md"],
                "api/": ["openapi/", "postman/"],
                "deployment/": ["environments/", "procedures/"]
            },
            "scripts/": {
                "deployment/": ["deploy.sh", "rollback.sh"],
                "development/": ["setup.sh", "test-all.sh"],
                "utilities/": ["migration/", "backup/"]
            }
        }
        
        # Generate service-specific directories
        for service in services:
            structure["services/"][f"{service}/"] = {
                "src/": ["controllers/", "services/", "models/", "routes/"],
                "tests/": ["unit/", "integration/", "e2e/"],
                "config/": ["development.json", "staging.json", "production.json"],
                "docs/": ["api.md", "deployment.md"]
            }
        
        return DirectoryStructure(structure)
```

## Build System Configuration Generation

### Adaptive Build Configuration
```python
class BuildSystemGenerator:
    """
    Generates optimized build configurations for different technology stacks
    """
    
    def __init__(self):
        self.build_optimizers = {
            'webpack': WebpackOptimizer(),
            'vite': ViteOptimizer(),
            'rollup': RollupOptimizer(),
            'maven': MavenOptimizer(),
            'gradle': GradleOptimizer(),
            'npm': NPMOptimizer(),
            'cargo': CargoOptimizer()
        }
    
    def generate_build_config(self, project_spec: ProjectSpecification,
                            structure: ProjectStructure) -> BuildConfiguration:
        """
        Generate optimized build configuration
        """
        
        # Determine primary build tool
        primary_tool = self._select_primary_build_tool(project_spec)
        
        # Generate base configuration
        base_config = self.build_optimizers[primary_tool].generate_base_config(
            project_spec, structure
        )
        
        # Apply environment-specific optimizations
        env_configs = {}
        for env in ['development', 'staging', 'production']:
            env_config = self._generate_environment_config(
                base_config, env, project_spec
            )
            env_configs[env] = env_config
        
        # Generate auxiliary configurations
        auxiliary_configs = self._generate_auxiliary_configs(
            project_spec, structure
        )
        
        return BuildConfiguration(
            primary_tool=primary_tool,
            base_config=base_config,
            environment_configs=env_configs,
            auxiliary_configs=auxiliary_configs,
            scripts=self._generate_build_scripts(primary_tool, project_spec)
        )
    
    def _generate_environment_config(self, base_config: dict, 
                                   environment: str,
                                   project_spec: ProjectSpecification) -> dict:
        """
        Generate environment-specific build optimizations
        """
        
        env_config = base_config.copy()
        
        if environment == 'development':
            env_config.update({
                'mode': 'development',
                'devtool': 'eval-source-map',
                'optimization': {'minimize': False},
                'devServer': {
                    'hot': True,
                    'port': 3000,
                    'historyApiFallback': True
                }
            })
        
        elif environment == 'production':
            env_config.update({
                'mode': 'production',
                'devtool': 'source-map',
                'optimization': {
                    'minimize': True,
                    'splitChunks': {
                        'chunks': 'all',
                        'cacheGroups': {
                            'vendor': {
                                'test': '/node_modules/',
                                'name': 'vendors',
                                'chunks': 'all'
                            }
                        }
                    }
                },
                'performance': {
                    'maxAssetSize': 250000,
                    'maxEntrypointSize': 250000
                }
            })
        
        return env_config
```

### Multi-Language Build Orchestration
```python
class MultiLanguageBuildOrchestrator:
    """
    Orchestrates builds across multiple programming languages in a project
    """
    
    def __init__(self):
        self.language_detectors = LanguageDetectors()
        self.build_dependency_resolver = BuildDependencyResolver()
        self.parallel_executor = ParallelBuildExecutor()
    
    def generate_orchestration_config(self, project_structure: ProjectStructure) -> OrchestrationConfig:
        """
        Generate configuration for multi-language build orchestration
        """
        
        # Detect languages and their build requirements
        language_analysis = self.language_detectors.analyze_project(project_structure)
        
        # Resolve build dependencies and order
        build_graph = self.build_dependency_resolver.resolve_dependencies(
            language_analysis
        )
        
        # Generate parallel execution plan
        execution_plan = self.parallel_executor.generate_execution_plan(build_graph)
        
        return OrchestrationConfig(
            languages=language_analysis.detected_languages,
            build_order=build_graph.topological_order,
            parallel_groups=execution_plan.parallel_groups,
            orchestration_scripts=self._generate_orchestration_scripts(
                execution_plan, language_analysis
            )
        )
    
    def _generate_orchestration_scripts(self, plan: ExecutionPlan,
                                      analysis: LanguageAnalysis) -> Dict[str, str]:
        """
        Generate orchestration scripts for different environments
        """
        
        scripts = {}
        
        # Main build script
        scripts['build-all.sh'] = self._generate_main_build_script(plan, analysis)
        
        # Test script
        scripts['test-all.sh'] = self._generate_test_script(plan, analysis)
        
        # Development script
        scripts['dev-start.sh'] = self._generate_dev_script(plan, analysis)
        
        # CI/CD scripts
        scripts['ci-build.yml'] = self._generate_ci_script(plan, analysis)
        
        return scripts
```

## Development Environment Configuration

### IDE and Editor Configuration Generation
```python
class DevelopmentEnvironmentGenerator:
    """
    Generates development environment configurations for popular IDEs and editors
    """
    
    def __init__(self):
        self.ide_configurators = {
            'vscode': VSCodeConfigurator(),
            'intellij': IntelliJConfigurator(),
            'vim': VimConfigurator(),
            'emacs': EmacsConfigurator()
        }
    
    def generate_ide_configs(self, project_spec: ProjectSpecification,
                           structure: ProjectStructure) -> IDEConfigurations:
        """
        Generate IDE configurations for project
        """
        
        configs = {}
        
        # Generate VS Code configuration
        vscode_config = self.ide_configurators['vscode'].generate_config(
            project_spec, structure
        )
        configs['vscode'] = vscode_config
        
        # Generate IntelliJ configuration
        intellij_config = self.ide_configurators['intellij'].generate_config(
            project_spec, structure
        )
        configs['intellij'] = intellij_config
        
        return IDEConfigurations(configs)

class VSCodeConfigurator:
    """
    Generates VS Code specific configurations
    """
    
    def generate_config(self, project_spec: ProjectSpecification,
                       structure: ProjectStructure) -> VSCodeConfig:
        """
        Generate VS Code workspace configuration
        """
        
        # Settings configuration
        settings = self._generate_settings(project_spec)
        
        # Extensions recommendations
        extensions = self._recommend_extensions(project_spec)
        
        # Launch configurations for debugging
        launch_configs = self._generate_launch_configs(project_spec, structure)
        
        # Tasks configuration
        tasks = self._generate_tasks(project_spec, structure)
        
        return VSCodeConfig(
            settings=settings,
            extensions=extensions,
            launch_configurations=launch_configs,
            tasks=tasks
        )
    
    def _generate_settings(self, project_spec: ProjectSpecification) -> dict:
        """
        Generate .vscode/settings.json content
        """
        
        settings = {
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll.eslint": True,
                "source.organizeImports": True
            },
            "files.exclude": {
                "**/node_modules": True,
                "**/.git": True,
                "**/dist": True,
                "**/build": True
            }
        }
        
        # Language-specific settings
        if 'typescript' in project_spec.languages:
            settings.update({
                "typescript.preferences.importModuleSpecifier": "relative",
                "typescript.suggest.autoImports": True,
                "typescript.updateImportsOnFileMove.enabled": "always"
            })
        
        if 'python' in project_spec.languages:
            settings.update({
                "python.defaultInterpreterPath": "./venv/bin/python",
                "python.linting.enabled": True,
                "python.linting.pylintEnabled": True,
                "python.formatting.provider": "black"
            })
        
        return settings
```

## Testing Framework Configuration

### Comprehensive Testing Setup
```python
class TestingFrameworkGenerator:
    """
    Generates comprehensive testing configurations and boilerplate
    """
    
    def __init__(self):
        self.test_framework_selectors = TestFrameworkSelectors()
        self.test_config_generators = TestConfigGenerators()
        self.test_utility_generators = TestUtilityGenerators()
    
    def generate_testing_setup(self, project_spec: ProjectSpecification,
                             structure: ProjectStructure) -> TestingSetup:
        """
        Generate complete testing setup for project
        """
        
        # Select appropriate testing frameworks
        frameworks = self.test_framework_selectors.select_frameworks(project_spec)
        
        # Generate framework configurations
        configurations = {}
        for framework in frameworks:
            config = self.test_config_generators[framework].generate_config(
                project_spec, structure
            )
            configurations[framework] = config
        
        # Generate test utilities and helpers
        utilities = self.test_utility_generators.generate_utilities(
            project_spec, frameworks
        )
        
        # Generate test templates
        templates = self._generate_test_templates(project_spec, frameworks)
        
        return TestingSetup(
            frameworks=frameworks,
            configurations=configurations,
            utilities=utilities,
            templates=templates,
            scripts=self._generate_test_scripts(frameworks)
        )
    
    def _generate_test_templates(self, project_spec: ProjectSpecification,
                               frameworks: List[str]) -> Dict[str, TestTemplate]:
        """
        Generate test templates for different types of tests
        """
        
        templates = {}
        
        # Unit test templates
        if 'jest' in frameworks:
            templates['unit'] = JestUnitTestTemplate(project_spec)
        elif 'pytest' in frameworks:
            templates['unit'] = PytestUnitTestTemplate(project_spec)
        
        # Integration test templates
        if 'cypress' in frameworks:
            templates['e2e'] = CypressE2ETestTemplate(project_spec)
        elif 'playwright' in frameworks:
            templates['e2e'] = PlaywrightE2ETestTemplate(project_spec)
        
        # API test templates
        if project_spec.has_api:
            templates['api'] = APITestTemplate(project_spec, frameworks)
        
        return templates

class JestConfigurationGenerator:
    """
    Generates Jest testing framework configuration
    """
    
    def generate_config(self, project_spec: ProjectSpecification,
                       structure: ProjectStructure) -> JestConfig:
        """
        Generate optimized Jest configuration
        """
        
        config = {
            "preset": "ts-jest" if "typescript" in project_spec.languages else None,
            "testEnvironment": "jsdom" if project_spec.has_frontend else "node",
            "roots": ["<rootDir>/src", "<rootDir>/tests"],
            "testMatch": [
                "**/__tests__/**/*.(ts|tsx|js)",
                "**/*.(test|spec).(ts|tsx|js)"
            ],
            "collectCoverageFrom": [
                "src/**/*.(ts|tsx)",
                "!src/**/*.d.ts",
                "!src/index.ts"
            ],
            "coverageDirectory": "coverage",
            "coverageReporters": ["html", "text", "lcov"],
            "setupFilesAfterEnv": ["<rootDir>/tests/setup.ts"],
            "moduleNameMapping": self._generate_module_mapping(structure)
        }
        
        # Add TypeScript specific configuration
        if "typescript" in project_spec.languages:
            config.update({
                "transform": {
                    "^.+\\.(ts|tsx)$": "ts-jest"
                },
                "moduleFileExtensions": ["ts", "tsx", "js", "jsx", "json"]
            })
        
        return JestConfig(config)
```

## Quality Assurance Configuration

### Automated Code Quality Setup
```python
class CodeQualitySetupGenerator:
    """
    Generates comprehensive code quality assurance configurations
    """
    
    def __init__(self):
        self.linting_configurators = LintingConfigurators()
        self.formatting_configurators = FormattingConfigurators()
        self.security_configurators = SecurityConfigurators()
        self.performance_configurators = PerformanceConfigurators()
    
    def generate_quality_setup(self, project_spec: ProjectSpecification) -> QualitySetup:
        """
        Generate complete code quality setup
        """
        
        # Linting configuration
        linting_config = self.linting_configurators.generate_config(project_spec)
        
        # Code formatting configuration
        formatting_config = self.formatting_configurators.generate_config(project_spec)
        
        # Security scanning configuration
        security_config = self.security_configurators.generate_config(project_spec)
        
        # Performance monitoring configuration
        performance_config = self.performance_configurators.generate_config(project_spec)
        
        # Pre-commit hooks configuration
        precommit_config = self._generate_precommit_config(
            linting_config, formatting_config, security_config
        )
        
        return QualitySetup(
            linting=linting_config,
            formatting=formatting_config,
            security=security_config,
            performance=performance_config,
            precommit_hooks=precommit_config,
            ci_integration=self._generate_ci_quality_integration(project_spec)
        )
    
    def _generate_precommit_config(self, linting: LintingConfig,
                                 formatting: FormattingConfig,
                                 security: SecurityConfig) -> PrecommitConfig:
        """
        Generate pre-commit hooks configuration
        """
        
        hooks = []
        
        # Add formatting hooks
        if formatting.prettier_enabled:
            hooks.append({
                "repo": "https://github.com/pre-commit/mirrors-prettier",
                "rev": "v3.0.3",
                "hooks": [{"id": "prettier"}]
            })
        
        # Add linting hooks
        if linting.eslint_enabled:
            hooks.append({
                "repo": "https://github.com/pre-commit/mirrors-eslint",
                "rev": "v8.47.0",
                "hooks": [{"id": "eslint", "files": "\\.(js|ts|jsx|tsx)$"}]
            })
        
        # Add security hooks
        if security.secrets_detection_enabled:
            hooks.append({
                "repo": "https://github.com/Yelp/detect-secrets",
                "rev": "v1.4.0",
                "hooks": [{"id": "detect-secrets"}]
            })
        
        return PrecommitConfig({"repos": hooks})
```

This comprehensive codebase setup and organization framework ensures that generated projects follow industry best practices, maintain high code quality, and provide excellent developer experience across different technology stacks and project scales.