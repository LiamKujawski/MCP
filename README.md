# MCP - Multi-Agent Collaborative Platform

[![CI/CD Pipeline](https://github.com/LiamKujawski/MCP/actions/workflows/ci.yml/badge.svg)](https://github.com/LiamKujawski/MCP/actions/workflows/ci.yml)
[![Multi-Agent Experiment](https://github.com/LiamKujawski/MCP/actions/workflows/multi-agent-experiment.yml/badge.svg)](https://github.com/LiamKujawski/MCP/actions/workflows/multi-agent-experiment.yml)
[![codecov](https://codecov.io/gh/LiamKujawski/MCP/branch/main/graph/badge.svg)](https://codecov.io/gh/LiamKujawski/MCP)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Overview

MCP implements a **fully automated Research → Synthesis → Experiment → Deploy → Optimize loop** that transforms multi-model AI research into production deployments without human intervention.

### Key Features

- **🔄 Continuous Loop**: Automated pipeline from research to production
- **🧠 Multi-Model Synthesis**: Combines insights from O3, Claude-4-Sonnet, and Claude-4-Opus
- **🏗️ Full-Stack Generation**: FastAPI backend + Next.js frontend with ≥90% test coverage
- **📊 Real-Time Monitoring**: WebSocket-based UI for pipeline visualization
- **🐳 Multi-Arch Deployment**: ARM64 and AMD64 support with Traefik routing
- **🔒 Security First**: Semgrep/Bandit clean builds, OWASP compliance

## 🏛️ Architecture

### The Five Phases

```mermaid
graph LR
    A[1. Research] --> B[2. Synthesis]
    B --> C[3. Experiment]
    C --> D[4. Deploy]
    D --> E[5. Optimize]
    E --> A
```

1. **Research Collection**: Normalized markdown with front-matter
2. **Synthesis**: AI-generated implementation prompts
3. **Experiment**: Parallel model execution and testing
4. **Deploy**: Automated containerization and deployment
5. **Optimize**: Performance monitoring and feedback

### System Components

- **Backend**: FastAPI with async Python, WebSocket support
- **Frontend**: Next.js 13+ with TypeScript, Tailwind CSS, Storybook
- **Testing**: Playwright E2E, Jest unit tests, pytest integration
- **Infrastructure**: Docker, Kubernetes, Traefik, GitHub Actions
- **Documentation**: C4 diagrams, ADRs, automated API docs

## 🚦 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker 24+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/LiamKujawski/MCP.git
cd MCP

# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start backend
uvicorn src.main:app --reload

# Frontend setup (in new terminal)
cd ui
npm install
npm run dev

# Access the application
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Running Tests

```bash
# Backend tests
pytest --cov=src --cov-report=html

# Frontend tests
cd ui
npm run test
npm run test:e2e

# Security scans
bandit -r src/
cd ui && npm audit
```

## 📁 Project Structure

```
MCP/
├── .github/workflows/       # CI/CD pipelines
│   ├── ci.yml              # Main CI pipeline
│   └── multi-agent-experiment.yml  # Research loop
├── chatgpt-agent-research/  # Agent research docs
├── codebase-generation-prompt-research/  # Prompt research
├── docs/                    # Documentation
│   ├── architecture/        # C4 diagrams
│   └── LOOP.md             # Pipeline documentation
├── src/                     # Backend source code
├── ui/                      # Frontend Next.js app
├── scripts/                 # Automation scripts
├── docker-compose.prod.yml  # Production config
└── synthesize-research-prompts/  # Generated prompts
```

## 🔬 Research Structure

Each research topic follows this structure:

```
research-type/
└── model-name/
    ├── 01_overview.md
    ├── 02_architecture.md
    ├── 03_prompt_design.md
    ├── 04_codebase_setup.md
    └── 05_enhancements.md
```

With front-matter:

```yaml
---
topic: "topic-name"
model: "model-name"
stage: research
version: 1
---
```

## 🤖 Adding Research

1. Create markdown files following the naming convention
2. Include front-matter and DocOps footer
3. Push to main branch
4. The automation loop triggers automatically

## 📊 Monitoring

Access the monitoring dashboard at `http://localhost:3000/dashboard` to view:

- Pipeline execution status
- Model performance metrics
- Deployment health
- Research coverage

## 🚀 Deployment

### Production Deployment

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml scale web=3
```

### Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://user:pass@localhost/mcp
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## 📚 Documentation

- [Loop Documentation](docs/LOOP.md) - Complete pipeline guide
- [C4 Architecture](docs/architecture/) - System diagrams
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Storybook](http://localhost:6006) - Component library

## 🧪 Experimentation

Run experiments manually:

```bash
python scripts/run_experiment.py --model o3 --type full
```

Evaluate results:

```bash
python scripts/eval.py --output summary.json
```

## 🤝 Contributing

We follow the automated DocOps approach:

1. Add research following the structure
2. Let the system generate implementations
3. Review and iterate on results
4. Document learnings

## 📈 Performance

- **Pipeline Speed**: < 10 minutes from research to deployment
- **Test Coverage**: ≥ 90% across all components
- **Lighthouse Score**: ≥ 90 for UI performance
- **Security**: Zero HIGH/CRITICAL vulnerabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Research synthesis inspired by multi-model collaboration patterns
- Infrastructure patterns from cloud-native best practices
- Documentation approach based on Diátaxis framework

---

**Built with ❤️ by the MCP Team** 