# Project Templates - Claude Development Framework

**Purpose**: Production-ready project templates for common software domains

**Version**: 1.0.0
**Last Updated**: 2025-10-03

---

## Overview

This directory contains fully-configured project templates that apply the Claude Development Framework to specific domains. Each template includes:

✅ Complete `.claude/` configuration
✅ 2-3 fully implemented example use cases with tests
✅ Domain-specific adaptations to framework rules
✅ Working CI/CD workflows
✅ Deployment documentation
✅ Common patterns (error handling, logging, configuration)

---

## Available Templates

### 1. REST API (FastAPI)
**Path**: `rest-api-fastapi/`
**Best For**: Backend APIs, microservices, REST services

**Includes**:
- FastAPI application structure
- Example CRUD operations (User management)
- Database integration (SQLAlchemy + PostgreSQL)
- Authentication/authorization patterns
- API documentation (Swagger/OpenAPI)
- Docker deployment

**Use Cases Included**:
- UC-001: Create User
- UC-002: Authenticate User
- UC-003: List Users

---

### 2. CLI Tool (Click)
**Path**: `cli-tool-click/`
**Best For**: Command-line tools, automation scripts

**Includes**:
- Click-based CLI structure
- Subcommand organization
- Configuration management
- Testing patterns for CLI
- Shell completion
- Package distribution setup

**Use Cases Included**:
- UC-001: Initialize Configuration
- UC-002: Process Data
- UC-003: Generate Report

---

### 3. Data Pipeline
**Path**: `data-pipeline/`
**Best For**: ETL workflows, data processing, batch jobs

**Includes**:
- Python-based ETL structure
- Data validation patterns
- Error handling and retry logic
- Pipeline orchestration
- Monitoring and logging
- Testing data pipelines

**Use Cases Included**:
- UC-001: Extract Data from Source
- UC-002: Transform and Validate Data
- UC-003: Load Data to Destination

---

### 4. Web Application (React + FastAPI)
**Path**: `web-app-react/`
**Best For**: Full-stack applications, dashboards, SPAs

**Includes**:
- FastAPI backend
- React frontend (TypeScript)
- Component-driven UCs
- E2E testing setup
- State management (Redux/Context)
- Deployment configuration

**Use Cases Included**:
- UC-001: User Registration Flow
- UC-002: Dashboard Display
- UC-003: Data Submission

---

### 5. Machine Learning Pipeline
**Path**: `ml-pipeline/`
**Best For**: ML training, inference services, model deployment

**Includes**:
- Training pipeline structure
- Model versioning patterns
- Experiment tracking
- Inference service (FastAPI)
- Model monitoring
- MLOps best practices

**Use Cases Included**:
- UC-001: Train Model
- UC-002: Evaluate Model
- UC-003: Serve Predictions

---

## Using Templates

### With CLI Tool (Recommended)

```bash
# Initialize project with template
claude-dev init my-project --template rest-api

# Or with full path
./init-project.sh my-project --template rest-api-fastapi
```

### Manual Copy

```bash
# Copy template to new project
cp -r templates/rest-api-fastapi/ my-new-api/

# Customize for your project
cd my-new-api/
# Update .claude/CLAUDE.md with project name
# Modify example use cases for your domain
# Update README.md
```

---

## Template Structure

Each template follows this structure:

```
template-name/
├── .claude/
│   ├── CLAUDE.md                    # Project overview
│   ├── development-rules.md         # Adapted rules for domain
│   ├── templates/                   # Spec templates
│   ├── guides/                      # Domain-specific guides
│   ├── quick-ref/                   # Quick references
│   └── agents/                      # Framework agents
├── specs/
│   ├── use-cases/
│   │   ├── UC-001-example.md       # Example UC 1
│   │   ├── UC-002-example.md       # Example UC 2
│   │   └── UC-003-example.md       # Example UC 3
│   ├── services/
│   │   └── SVC-001-example.md
│   └── adrs/
│       └── ADR-001-example.md
├── src/                             # Source code with examples
├── tests/                           # Complete test suite
│   ├── unit/
│   ├── integration/
│   └── bdd/
├── planning/
│   ├── current-iteration.md
│   └── iteration-01-example.md
├── docs/
│   ├── setup.md
│   ├── deployment.md
│   └── domain-guide.md              # Domain-specific guidance
├── .github/
│   └── workflows/                   # CI/CD workflows
├── docker-compose.yml               # Local development (if needed)
├── Dockerfile                       # Container deployment
├── requirements.txt                 # Dependencies
├── pyproject.toml                   # Package configuration
└── README.md                        # Template-specific README
```

---

## Customization Guide

### Step 1: Project Setup
1. Copy template to new directory
2. Update `.claude/CLAUDE.md` with your project details
3. Review and adapt `development-rules.md` if needed

### Step 2: Modify Examples
1. Replace example use cases with your actual requirements
2. Update example code to match your domain
3. Adapt tests to your specifications

### Step 3: Configuration
1. Update `requirements.txt` with your dependencies
2. Configure `.env` or config files
3. Adjust CI/CD workflows for your deployment

### Step 4: Domain Adaptations
1. Review domain-specific guides in `docs/`
2. Adapt architectural patterns if needed
3. Update ADRs with your technical decisions

---

## Template Development Rules

When creating new templates, follow these guidelines:

### 1. Framework Compliance
- ✅ Include all 12 Non-Negotiable Rules
- ✅ Complete `.claude/` directory structure
- ✅ Proper use case specifications
- ✅ Test-first development examples
- ✅ BDD scenarios for user-facing features

### 2. Production Ready
- ✅ Working code (not just stubs)
- ✅ Complete test coverage (90%+)
- ✅ Error handling and logging
- ✅ Configuration management
- ✅ Deployment documentation

### 3. Domain Best Practices
- ✅ Idiomatic patterns for the domain
- ✅ Industry-standard tools and libraries
- ✅ Security considerations
- ✅ Performance optimization
- ✅ Scalability patterns

### 4. Educational Value
- ✅ Clear, well-documented examples
- ✅ Common patterns demonstrated
- ✅ Pitfalls and solutions documented
- ✅ Learning resources included

---

## Contributing New Templates

Want to add a template? Follow this process:

### 1. Proposal
- Open an issue describing the template
- Identify target domain and use cases
- List key features and patterns

### 2. Implementation
- Follow template structure above
- Include 2-3 complete example use cases
- Write comprehensive tests
- Document domain-specific adaptations

### 3. Review
- Ensure framework compliance
- Verify production readiness
- Test with real projects
- Document lessons learned

### 4. Submission
- Submit PR with template
- Update this README
- Add to template generator script

---

## Template Maintenance

### Version Compatibility

| Template | Framework Version | Last Updated |
|----------|------------------|--------------|
| REST API | v2.1+ | 2025-10-03 |
| CLI Tool | v2.1+ | 2025-10-03 |
| Data Pipeline | v2.1+ | 2025-10-03 |
| Web App | v2.1+ | 2025-10-03 |
| ML Pipeline | v2.1+ | 2025-10-03 |

### Update Schedule
- Templates reviewed quarterly
- Dependency updates monthly
- Framework alignment on each major version

---

## FAQ

### Q: Can I mix templates?
A: Yes! Templates can be combined. For example, use ML Pipeline + REST API for ML inference services.

### Q: How do I update an existing project to use a template?
A: Templates are starting points. Extract patterns and best practices, then apply incrementally to your project.

### Q: Are templates language-specific?
A: Current templates use Python. Contributions for other languages welcome!

### Q: Can I customize development rules?
A: Yes, but maintain the 12 core principles. Document deviations in ADRs.

### Q: How do I choose the right template?
A: Match your primary use case:
- Building API → REST API
- CLI tool → CLI Tool
- Data processing → Data Pipeline
- Web app → Web App
- ML project → ML Pipeline

---

## Support

For template-specific questions:
- See template README.md
- Check `docs/domain-guide.md` in template
- Open an issue with [TEMPLATE] prefix

For framework questions:
- See main framework documentation
- Review framework troubleshooting guide

---

## Roadmap

### Completed ✅
- [x] REST API template (FastAPI)
- [x] CLI Tool template (Click)
- [x] Data Pipeline template (Python)
- [x] Web App template (React + FastAPI)
- [x] ML Pipeline template

### Planned 📋
- [ ] Microservices template (FastAPI + Docker + K8s)
- [ ] GraphQL API template (Strawberry)
- [ ] Event-Driven template (Kafka/RabbitMQ)
- [ ] Serverless template (AWS Lambda)
- [ ] Mobile Backend template (FastAPI + Firebase)

---

**Version**: 1.0.0
**Last Updated**: 2025-10-03
**Part of**: Claude Development Framework v2.1

Happy building! 🚀
