# Template Customization Guide

**Purpose**: How to adapt the Claude Development Framework for different project types, languages, and team preferences

**Last Updated**: 2025-10-01

---

## Overview

The Claude Development Framework is designed to be language-agnostic and adaptable. This guide shows you how to customize the framework for your specific needs while maintaining its core principles.

**Core principles that should NOT change**:
1. Specification-driven development
2. Test-first approach
3. Incremental iterations (max 3 hours)
4. Documentation of decisions
5. Session discipline

**What you CAN customize**:
- File structures and naming conventions
- Testing frameworks and patterns
- Documentation formats
- Tool integrations
- Language-specific workflows

---

## Quick Start: Language Adaptations

### Python Projects

**Default structure works well** - minimal changes needed.

**Recommended adjustments**:

1. **Testing**:
```bash
# Use pytest instead of generic test runner
# Update .claude/quick-ref/commands.md:
pytest tests/ -v                    # Run all tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/bdd/ --gherkin-terminal-reporter  # BDD tests
pytest --cov=src tests/             # With coverage
```

2. **Type checking**:
```bash
# Add to validation workflow
mypy src/ --strict                  # Type checking
ruff check src/                     # Linting
black src/ --check                  # Formatting
```

3. **Project structure**:
```
project/
├── src/                    # Source code (not implementation/)
│   └── package_name/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── bdd/features/
├── specs/
├── planning/
└── .claude/
```

4. **Dependencies**:
```bash
# Add to init-project.sh:
python -m venv venv
source venv/bin/activate
pip install pytest pytest-bdd pytest-cov mypy ruff black
pip freeze > requirements.txt
```

---

### JavaScript/TypeScript Projects

**Significant structure changes recommended**.

**1. Project structure**:
```
project/
├── src/                    # TypeScript source
├── dist/                   # Compiled JavaScript (gitignored)
├── tests/
│   ├── unit/              # Jest tests
│   ├── integration/       # Integration tests
│   └── bdd/features/      # Cucumber tests
├── specs/
├── planning/
└── .claude/
```

**2. Testing commands**:
```bash
# Update .claude/quick-ref/commands.md:
npm test                    # Run all tests
npm run test:unit           # Unit tests only
npm run test:bdd            # BDD tests (Cucumber)
npm run test:coverage       # With coverage
```

**3. Package scripts** (`package.json`):
```json
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest tests/unit",
    "test:bdd": "cucumber-js tests/bdd",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit",
    "build": "tsc"
  }
}
```

**4. BDD setup**:
```bash
npm install --save-dev @cucumber/cucumber
npm install --save-dev @types/cucumber
```

**5. Git workflow adjustments**:
- Add `dist/` to `.gitignore`
- Add `node_modules/` to `.gitignore`
- Commit `package-lock.json`

---

### Go Projects

**Structure follows Go conventions**.

**1. Project structure**:
```
project/
├── cmd/                    # Main applications
│   └── app/
│       └── main.go
├── pkg/                    # Library code
│   └── service/
├── internal/               # Private code
├── tests/
│   ├── unit/              # Go test files
│   └── bdd/features/      # Godog BDD
├── specs/
├── planning/
└── .claude/
```

**2. Testing commands**:
```bash
# Update .claude/quick-ref/commands.md:
go test ./...                           # All tests
go test ./pkg/...                       # Package tests
go test -v -race ./...                  # With race detector
go test -cover ./...                    # With coverage
godog tests/bdd/features/              # BDD tests
```

**3. BDD setup**:
```bash
go get github.com/cucumber/godog/cmd/godog
```

**4. Code organization**:
- Use `pkg/` for reusable libraries
- Use `internal/` for private packages
- Use `cmd/` for application entry points

**5. Naming conventions**:
```bash
# Test files
filename_test.go                        # Go convention
```

---

### Java Projects

**Use Maven or Gradle structure**.

**1. Maven structure**:
```
project/
├── src/
│   ├── main/java/com/company/project/
│   └── test/java/com/company/project/
├── tests/
│   └── bdd/features/              # Cucumber
├── specs/
├── planning/
├── .claude/
└── pom.xml
```

**2. Testing commands** (Maven):
```bash
# Update .claude/quick-ref/commands.md:
mvn test                            # Run all tests
mvn test -Dtest=ClassName           # Specific test
mvn verify                          # Integration tests
mvn test-compile                    # Compile tests only
```

**3. BDD setup** (Cucumber):
```xml
<!-- Add to pom.xml -->
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-java</artifactId>
    <version>7.14.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>io.cucumber</groupId>
    <artifactId>cucumber-junit</artifactId>
    <version>7.14.0</version>
    <scope>test</scope>
</dependency>
```

**4. Naming conventions**:
```java
// Test classes
ClassNameTest.java                  // JUnit convention
```

---

## Customizing for Project Types

### Web APIs (REST/GraphQL)

**Add API-specific templates**:

1. **API endpoint specification**:
```bash
# Add to .claude/templates/
cp .claude/templates/use-case-template.md .claude/templates/api-endpoint-template.md
```

**API Endpoint Template** (`.claude/templates/api-endpoint-template.md`):
```markdown
# API Endpoint: [METHOD] /api/path

**Endpoint ID**: EP-XXX
**Use Case**: UC-XXX
**Version**: 1.0

## Request

**Method**: GET | POST | PUT | DELETE
**Path**: `/api/v1/resource/{id}`
**Auth**: Required | Optional | None

### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Resource identifier |

### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filter | string | No | Filter results |

### Request Body
```json
{
  "field": "value"
}
```

## Response

### Success (200 OK)
```json
{
  "data": {...},
  "meta": {...}
}
```

### Errors
- 400 Bad Request: Invalid input
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Resource not found
- 500 Internal Error: Server error
```

2. **API testing structure**:
```
tests/
├── unit/           # Business logic tests
├── integration/    # API endpoint tests
│   └── api/
│       ├── test_users_api.py
│       └── test_posts_api.py
└── bdd/features/   # User journey tests
    └── api/
```

3. **Update commands**:
```bash
# API-specific commands for .claude/quick-ref/commands.md:
curl http://localhost:8000/health         # Health check
curl -X POST http://localhost:8000/api/v1/users -H "Content-Type: application/json" -d '{"name":"test"}'
```

---

### CLI Applications

**Focus on command testing**.

**1. Structure**:
```
project/
├── src/
│   ├── commands/          # Command implementations
│   ├── lib/               # Shared libraries
│   └── main.py           # CLI entry point
├── tests/
│   ├── unit/             # Command unit tests
│   ├── integration/      # CLI integration tests
│   └── bdd/features/     # User workflow tests
├── specs/
│   └── commands/         # Command specifications
└── .claude/
```

**2. Testing approach**:
```python
# tests/integration/test_cli.py
from click.testing import CliRunner
from src.main import cli

def test_help_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output
```

**3. BDD scenarios for CLI**:
```gherkin
# tests/bdd/features/list-command.feature
Feature: List Command
  As a user
  I want to list all items
  So that I can see what's available

  Scenario: List items with no filters
    When I run "app list"
    Then the exit code should be 0
    And the output should contain "Found 3 items"
    And the output should contain item "Item 1"
```

---

### Libraries/Packages

**No application code, only library code**.

**1. Structure**:
```
project/
├── src/
│   └── library_name/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── unit/             # Library function tests
│   └── integration/      # Library integration tests
├── examples/             # Usage examples
├── docs/                 # API documentation
├── specs/
│   └── api/             # Public API specifications
└── .claude/
```

**2. No BDD needed**:
- Libraries don't have user-facing features
- Focus on unit and integration tests
- Use doctests for examples

**3. Public API focus**:
```markdown
# specs/api/public-api.md
# Public API Specification

## Module: core

### Function: process_data(data, options)
**Purpose**: Process input data according to options
**Parameters**:
- data (dict): Input data to process
- options (dict): Processing options

**Returns**: dict - Processed data

**Raises**:
- ValueError: If data is invalid
- TypeError: If types don't match

**Example**:
```python
result = process_data({'key': 'value'}, {'mode': 'fast'})
```
```

---

### Microservices

**Each service is a separate project**.

**1. Multi-service structure**:
```
repo/
├── services/
│   ├── auth-service/
│   │   ├── .claude/       # Service-specific framework
│   │   ├── specs/
│   │   ├── src/
│   │   └── tests/
│   ├── api-gateway/
│   │   ├── .claude/
│   │   ├── specs/
│   │   ├── src/
│   │   └── tests/
│   └── data-service/
│       └── ...
├── shared/
│   ├── .claude/           # Shared framework configurations
│   └── specs/             # Cross-service contracts
└── docs/
    ├── architecture/
    └── service-registry.md
```

**2. Service dependencies**:
```markdown
# services/api-gateway/specs/dependencies.md
# Service Dependencies

**This Service**: api-gateway

## Depends On:
- auth-service (for token validation)
- data-service (for data retrieval)

## Communication:
- HTTP REST (synchronous)
- RabbitMQ events (asynchronous)

## Contracts:
- See shared/specs/contracts/auth-api.md
- See shared/specs/contracts/data-api.md
```

**3. Integration testing**:
```python
# Test cross-service integration
@pytest.mark.integration
def test_api_gateway_auth_flow():
    """Test that API gateway correctly validates tokens via auth service."""
    # Requires both services running
    token = auth_service.create_token("user123")
    response = api_gateway.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

---

## Customizing Documentation

### Markdown Alternatives

**If you prefer other formats**:

1. **ReStructuredText (RST)**:
```bash
# Convert templates to RST
for file in .claude/templates/*.md; do
    pandoc "$file" -f markdown -t rst -o "${file%.md}.rst"
done

# Update references in scripts and CLAUDE.md
```

2. **AsciiDoc**:
```bash
# Similar conversion process
# Update file extensions in validation scripts
```

**Note**: Stick with markdown for widest Claude Code compatibility.

---

### Inline vs Separate Documentation

**Current approach**: Separate specs/ directory

**Alternative**: Inline documentation
```
src/
└── users/
    ├── user_service.py
    ├── user_service_spec.md     # Spec alongside code
    └── test_user_service.py
```

**Pros**:
- Easier to find related spec
- Colocated with implementation

**Cons**:
- Harder to get overview of all specs
- Violates separation of specification and implementation

**Recommendation**: Keep separate specs/ directory unless you have strong preference.

---

## Customizing Git Workflow

### Branch Naming Conventions

**Default**: `iteration-XXX-description` or `uc-XXX-description`

**Alternatives**:

1. **Jira/Issue-based**:
```bash
git checkout -b feature/PROJ-123-user-authentication
git checkout -b bugfix/PROJ-456-login-error
```

Update `.claude/quick-ref/git.md` with your convention.

2. **Conventional Commits style**:
```bash
git checkout -b feat/user-authentication
git checkout -b fix/login-error
git checkout -b refactor/extract-service
```

3. **GitFlow**:
```bash
git checkout -b feature/user-auth
git checkout -b release/1.2.0
git checkout -b hotfix/critical-bug
```

**Update** `.claude/templates/git-workflow.md` to reflect your team's convention.

---

### Commit Message Templates

**Customizing commit format**:

Edit `.claude/templates/git-workflow.md` to update the commit template.

**Example: Jira integration**:
```markdown
[type]: Brief description

JIRA: PROJ-123
Specification: UC-003
Tests: 12 passing / 12 total

Details:
- Implemented user authentication
- Added JWT token generation
- Updated API documentation

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Customizing Iteration Planning

### Iteration Length

**Default**: 1-3 hours maximum

**Shorter iterations** (30-60 min):
```markdown
# Suitable for:
- Bug fixes
- Small features
- Refactoring tasks
- Documentation updates

# Update in development-rules.md:
**Rule 3**: Iterations must be 30-60 minutes maximum.
```

**Longer iterations** (3-5 hours):
```markdown
# WARNING: Not recommended!
# Violates Rule 3 (Incremental Above All)

# Only consider if:
- Working alone (no collaboration blockers)
- Task genuinely atomic (can't be split)
- You have high confidence in approach

# Still maintain checkpoint commits every 2 hours
```

---

### Planning Templates

**Add custom iteration types**:

1. **Spike (Research) Iteration**:
```markdown
# Iteration XXX: Spike - [Topic]

**Type**: SPIKE (Research/Investigation)
**Time Budget**: 2 hours maximum
**Goal**: Understand feasibility and approach

## Questions to Answer:
1. Is X library suitable for our needs?
2. What are performance characteristics?
3. Are there integration challenges?

## Deliverables:
- Research notes in research/learnings/
- ADR if decision needed
- Recommendation (proceed / reject / alternative)

## Success Criteria:
- All questions answered
- Recommendation documented
- No code implementation (research only)
```

2. **Bug Fix Iteration**:
```markdown
# Iteration XXX: Bug Fix - [Issue]

**Type**: BUG FIX
**Severity**: Critical | High | Medium | Low
**Time Budget**: 1-2 hours

## Bug Description:
[Describe the bug]

## Root Cause:
[To be determined during investigation]

## Fix Plan:
1. Write failing test that reproduces bug
2. Identify root cause
3. Implement fix
4. Verify all tests pass
5. Add regression test

## Success Criteria:
- Bug reproduced in test
- Fix implemented
- All tests passing (including new regression test)
```

---

## Tool Integrations

### CI/CD Integration

**Add framework validation to CI**:

**GitHub Actions** (`.github/workflows/framework-validation.yml`):
```yaml
name: Framework Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate template completeness
        run: ./validate-template.sh

      - name: Check traceability
        run: python3 scripts/validate-traceability.py

      - name: Check spec-code alignment
        run: ./scripts/check-alignment.py

      - name: Estimate context usage
        run: ./scripts/estimate-context.sh --tier 1
```

**GitLab CI** (`.gitlab-ci.yml`):
```yaml
framework-validation:
  stage: validate
  script:
    - ./validate-template.sh
    - python3 scripts/validate-traceability.py
    - ./scripts/check-alignment.py
  only:
    - merge_requests
    - main
```

---

### IDE Integration

**VS Code**:

Add workspace snippets (`.vscode/claude-framework.code-snippets`):
```json
{
  "Use Case Specification": {
    "scope": "markdown",
    "prefix": "uc-spec",
    "body": [
      "# Use Case: ${1:Title}",
      "",
      "**UC ID**: UC-${2:001}",
      "**Status**: Draft",
      "**Priority**: ${3:High}",
      "",
      "## Description",
      "${4:Description}",
      "",
      "## Acceptance Criteria",
      "1. ${5:Criterion 1}",
      "2. ${6:Criterion 2}",
      "",
      "## Services Used",
      "- ${7:ServiceName}",
      "",
      "**BDD File**: \\`features/uc-${2:001}-${8:name}.feature\\`"
    ]
  }
}
```

---

### Linter Integration

**Pre-commit hooks** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
# Validate framework before commit

echo "Validating framework structure..."

# Check traceability
if ! python3 scripts/validate-traceability.py; then
    echo "❌ Traceability validation failed"
    exit 1
fi

# Check spec-code alignment
if ! ./scripts/check-alignment.py; then
    echo "❌ Spec-code alignment check failed"
    exit 1
fi

echo "✅ Framework validation passed"
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Team Customizations

### Multi-Developer Teams

**1. Add pair programming support**:
```markdown
# Update git-workflow.md commit template:
Co-authored-by: Partner Name <partner@email.com>
🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**2. Add code review checklist**:
```markdown
# .claude/templates/code-review-checklist.md
- [ ] Specification exists and is followed
- [ ] Tests written before implementation
- [ ] All tests passing
- [ ] Code quality standards met
- [ ] No TODOs or shortcuts
- [ ] Documentation updated
- [ ] ADRs documented
```

**3. Add session handoff**:
```markdown
# planning/session-handoff.md
**From**: Developer A
**To**: Developer B
**Date**: 2025-10-01

## Current Status:
- Iteration 007 in progress (50% complete)
- Last commit: abc123
- Branch: iteration-007-entity-extraction

## What's Done:
- Tests written for basic extraction
- EntityExtractor class implemented

## What's Next:
- Implement confidence scoring
- Add integration tests
- Update documentation

## Blockers:
- None

## Context Files to Load:
- planning/current-iteration.md
- specs/use-cases/UC-007-entity-extraction.md
- implementation/services/entity-extractor/
```

---

### Solo Developer Optimizations

**Simplify ceremony**:

1. **Shorter session checklists**:
```markdown
# Minimal session checklist
1. Read CLAUDE.md, development-rules.md, current-iteration.md
2. Work on current task (test-first)
3. Update session-state.md
4. Commit when complete
```

2. **Skip some documentation**:
```markdown
# Optional to skip (for solo projects):
- ADRs for minor decisions
- Detailed technical decisions logs
- Session handoff notes
```

3. **Combined specs**:
```markdown
# Combine related specs into single file
# specs/use-cases/user-management.md (combines UC-001, UC-002, UC-003)
```

**Warning**: Don't skip test-first or specifications - these are core principles!

---

## Framework Versioning

**Track your customizations**:

```markdown
# .claude/CUSTOMIZATIONS.md
# Framework Customizations

**Base Framework**: Claude Development Framework v2.0
**Project**: MyProject
**Customizations Version**: 1.0
**Last Updated**: 2025-10-01

## Changes from Standard Framework:

1. **Language**: Python (pytest + BDD)
2. **Structure**: src/ instead of implementation/
3. **Iteration Length**: 1-2 hours (shorter than default)
4. **Git Workflow**: GitFlow with Jira integration
5. **Added Templates**:
   - API endpoint specification template
   - Bug fix iteration template
6. **Removed**:
   - Service registry (not applicable to monolith)

## Custom Scripts:
- scripts/deploy.sh - Deployment automation
- scripts/db-migrate.sh - Database migrations

## Team Conventions:
- Commit messages include Jira ticket IDs
- PRs require 2 approvals
- Code review checklist mandatory
```

---

## Validation After Customization

**After customizing, verify**:

```bash
# 1. Template validation still works
./validate-template.sh

# 2. Traceability validator works
python3 scripts/validate-traceability.py

# 3. Alignment checker works
./scripts/check-alignment.py

# 4. Context estimator works
./scripts/estimate-context.sh --tier 1

# 5. Test your custom workflows
[Run your specific test commands]
```

**If validation fails**: Update validation scripts to match your customizations.

---

## Getting Help

**Questions about customization**:

1. Check this guide first
2. Review framework documentation: `docs/claude-development-framework.md`
3. Look at examples: `docs/examples/`
4. Consult troubleshooting: `docs/troubleshooting.md`

**Contributing customizations back**:
- If your customization would benefit others, consider contributing to the framework
- Submit PRs or open issues at the framework repository

---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: 2025-10-01
**Compatibility**: Framework v2.0+
