#!/bin/bash
# Claude Development Framework - Template Validation Script
# Version 2.0
# Purpose: Verify template completeness and integrity

set -e

echo "=========================================="
echo "Claude Framework Template Validation"
echo "=========================================="
echo ""

ERRORS=0
WARNINGS=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ERRORS=$((ERRORS + 1))
}

warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo "ℹ️  $1"
}

# Check required files exist
echo "📋 Checking required files..."
echo ""

REQUIRED_FILES=(
    "README.md"
    "quick-start-guide.md"
    "init-project.sh"
    ".gitignore"
    ".claude/READING-ORDER.md"
    ".claude/templates/start-here.md"
    ".claude/templates/CLAUDE.md"
    ".claude/templates/development-rules.md"
    ".claude/templates/session-checklist.md"
    ".claude/templates/context-priority.md"
    ".claude/templates/technical-decisions.md"
    ".claude/templates/session-state.md"
    ".claude/templates/git-workflow.md"
    ".claude/templates/requirements-review-checklist.md"
    ".claude/templates/refactoring-checklist.md"
    ".claude/templates/use-case-template.md"
    ".claude/templates/implementation-CLAUDE.md"
    ".claude/templates/implementation-summary.md"
    ".claude/templates/code-reuse-checklist.md"
    ".claude/templates/service-spec.md"
    ".claude/templates/benchmark-report.md"
    ".claude/templates/library-evaluation.md"
    ".claude/templates/service-registry.md"
    ".claude/templates/services-README-template.md"
    ".claude/templates/research/paper-summary.md"
    ".claude/templates/research/article-links.md"
    ".claude/templates/research/implementation-readme.md"
    ".claude/guides/research-organization.md"
    ".claude/quick-ref/session-start.md"
    ".claude/quick-ref/tdd-cycle.md"
    ".claude/quick-ref/git.md"
    ".claude/quick-ref/services.md"
    ".claude/quick-ref/commands.md"
    ".claude/subagents/service-extractor.md"
    ".claude/subagents/service-designer.md"
    ".claude/subagents/service-dependency-analyzer.md"
    ".claude/subagents/service-optimizer.md"
    ".claude/subagents/service-library-finder.md"
    ".claude/subagents/uc-service-tracer.md"
    "docs/10-minute-start.md"
    "docs/claude-development-framework.md"
    "docs/service-architecture.md"
    "docs/troubleshooting.md"
    "docs/walkthrough-todo-api.md"
    "docs/example-first-session.md"
    "docs/session-types.md"
    "docs/advanced/tool-integration.md"
    "docs/advanced/large-codebase-context.md"
    "docs/examples/README.md"
    "docs/examples/subagent-service-extraction.md"
    "docs/examples/subagent-library-evaluation.md"
    "docs/examples/subagent-performance-optimization.md"
    "docs/examples/subagent-dependency-analysis.md"
    "docs/examples/subagent-traceability-validation.md"
    "docs/examples/subagent-multi-agent-orchestration.md"
    "docs/examples/scenario-circular-dependency-fix.md"
    "docs/examples/scenario-specification-evolution.md"
    "docs/examples/scenario-production-performance-crisis.md"
    "docs/examples/scenario-context-window-management.md"
    "scripts/validate-traceability.py"
    "scripts/lib/traceability.py"
    "scripts/add-template-versions.sh"
    "scripts/add-tier-labels.sh"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        error "Missing required file: $file"
    else
        success "Found: $file"
    fi
done

echo ""
echo "📝 Checking file content..."
echo ""

# Check if templates have placeholder text
if grep -q "\[PROJECT_NAME\]" .claude/templates/CLAUDE.md 2>/dev/null; then
    success "CLAUDE.md template contains PROJECT_NAME placeholder"
else
    warning "CLAUDE.md template missing PROJECT_NAME placeholder"
fi

if grep -q "\[PROJECT_NAME\]" .claude/templates/development-rules.md 2>/dev/null; then
    success "development-rules.md contains PROJECT_NAME placeholder"
else
    warning "development-rules.md missing PROJECT_NAME placeholder"
fi

if grep -q "\[PROJECT_NAME\]" .claude/templates/technical-decisions.md 2>/dev/null; then
    success "technical-decisions.md contains PROJECT_NAME placeholder"
else
    warning "technical-decisions.md missing PROJECT_NAME placeholder"
fi

echo ""
echo "🔍 Checking for critical content..."
echo ""

# Check start-here.md has key sections
if grep -q "Files to Read NOW" .claude/templates/start-here.md 2>/dev/null; then
    success "start-here.md contains reading order"
else
    error "start-here.md missing 'Files to Read NOW' section"
fi

if grep -q "First Session Protocol" .claude/templates/start-here.md 2>/dev/null; then
    success "start-here.md contains first session protocol"
else
    error "start-here.md missing 'First Session Protocol' section"
fi

# Check CLAUDE.md has session protocol
if grep -q "Session Protocol" .claude/templates/CLAUDE.md 2>/dev/null; then
    success "CLAUDE.md contains session protocol"
else
    error "CLAUDE.md missing 'Session Protocol' section"
fi

# Check development-rules.md has all 12 rules (table format)
if grep -q "| \*\*1\*\* |" .claude/templates/development-rules.md 2>/dev/null && \
   grep -q "| \*\*11\*\* |" .claude/templates/development-rules.md 2>/dev/null && \
   grep -q "| \*\*12\*\* |" .claude/templates/development-rules.md 2>/dev/null; then
    success "development-rules.md contains all 12 rules"
else
    error "development-rules.md missing complete rule set"
fi

# Check for git workflow
if grep -q "Git Workflow" .claude/templates/git-workflow.md 2>/dev/null; then
    success "git-workflow.md exists and has content"
else
    warning "git-workflow.md missing or incomplete"
fi

# Check for requirements review checklist
if grep -q "Requirements Review" .claude/templates/requirements-review-checklist.md 2>/dev/null; then
    success "requirements-review-checklist.md exists and has content"
else
    warning "requirements-review-checklist.md missing or incomplete"
fi

# Check for refactoring checklist
if grep -q "Refactoring Checklist" .claude/templates/refactoring-checklist.md 2>/dev/null; then
    success "refactoring-checklist.md exists and has content"
else
    warning "refactoring-checklist.md missing or incomplete"
fi

# Check for broken internal references
echo ""
echo "🔗 Checking for broken references..."
echo ""

# Check if frequently referenced files exist
REFERENCED_FILES=(
    ".claude/templates/start-here.md:CLAUDE.md"
    "README.md:quick-start-guide.md"
)

for ref in "${REFERENCED_FILES[@]}"; do
    file="${ref%%:*}"
    referenced="${ref##*:}"
    if [ -f "$file" ]; then
        if grep -q "$referenced" "$file" 2>/dev/null; then
            success "$file references $referenced"
        else
            warning "$file doesn't reference $referenced"
        fi
    fi
done

echo ""
echo "🧪 Testing init script..."
echo ""

# Check if init script is executable
if [ -x "init-project.sh" ]; then
    success "init-project.sh is executable"
else
    error "init-project.sh is not executable (run: chmod +x init-project.sh)"
fi

# Check if init script has required content
if grep -q "start-here.md" init-project.sh 2>/dev/null; then
    success "init-project.sh copies start-here.md"
else
    error "init-project.sh doesn't copy start-here.md"
fi

if grep -q "example-first-session.md" init-project.sh 2>/dev/null; then
    success "init-project.sh copies example-first-session.md"
else
    warning "init-project.sh doesn't copy example-first-session.md (optional)"
fi

echo ""
echo "📊 Checking documentation completeness..."
echo ""

# Check file sizes (very basic sanity check)
check_file_size() {
    local file=$1
    local min_lines=$2

    if [ -f "$file" ]; then
        local lines=$(wc -l < "$file")
        if [ "$lines" -ge "$min_lines" ]; then
            success "$file has $lines lines (>= $min_lines required)"
        else
            warning "$file only has $lines lines (expected >= $min_lines)"
        fi
    fi
}

check_file_size ".claude/templates/start-here.md" 100
check_file_size ".claude/templates/development-rules.md" 100
check_file_size ".claude/templates/refactoring-checklist.md" 300
check_file_size ".claude/templates/git-workflow.md" 200
check_file_size ".claude/templates/service-spec.md" 200
check_file_size ".claude/templates/benchmark-report.md" 200
check_file_size ".claude/templates/library-evaluation.md" 200
check_file_size ".claude/templates/service-registry.md" 200
check_file_size ".claude/templates/services-README-template.md" 80
check_file_size ".claude/quick-ref/git.md" 250
check_file_size ".claude/quick-ref/services.md" 150
check_file_size ".claude/subagents/service-extractor.md" 300
check_file_size ".claude/subagents/service-designer.md" 300
check_file_size ".claude/subagents/service-dependency-analyzer.md" 300
check_file_size ".claude/subagents/service-optimizer.md" 300
check_file_size ".claude/subagents/service-library-finder.md" 300
check_file_size ".claude/subagents/uc-service-tracer.md" 300
check_file_size ".claude/guides/research-organization.md" 300
check_file_size "quick-start-guide.md" 80
check_file_size "docs/claude-development-framework.md" 400
check_file_size "docs/service-architecture.md" 400
check_file_size "docs/troubleshooting.md" 400
check_file_size "docs/walkthrough-todo-api.md" 600
check_file_size "docs/example-first-session.md" 200
check_file_size "docs/session-types.md" 400
check_file_size "docs/examples/README.md" 300
check_file_size "docs/examples/subagent-service-extraction.md" 400
check_file_size "docs/examples/subagent-library-evaluation.md" 400
check_file_size "docs/examples/subagent-performance-optimization.md" 400

echo ""
echo "🔗 Checking UC-Service traceability validator..."
echo ""
if [ -x "scripts/validate-traceability.py" ]; then
    success "Traceability validator script exists and is executable"
else
    warning "Traceability validator script not found or not executable"
fi

echo ""
echo "=========================================="
echo "Validation Summary"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    success "ALL CHECKS PASSED!"
    echo ""
    echo "✨ Template is complete and ready to use!"
    echo ""
    echo "Next steps:"
    echo "  1. Run: ./init-project.sh my-project"
    echo "  2. cd my-project"
    echo "  3. Start Claude and say: 'Analyze this project'"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    warning "VALIDATION PASSED WITH WARNINGS"
    echo ""
    echo "Found $WARNINGS warning(s)"
    echo "Template is usable but could be improved."
    echo ""
    exit 0
else
    error "VALIDATION FAILED"
    echo ""
    echo "Found:"
    echo "  - $ERRORS error(s)"
    echo "  - $WARNINGS warning(s)"
    echo ""
    echo "Fix errors before using template."
    echo ""
    exit 1
fi