#!/bin/bash
# Claude Development Framework - Add TIER Labels
# Adds YAML frontmatter with TIER classification to framework files

set -e

echo "Adding TIER labels to framework files..."
echo ""

add_tier_frontmatter() {
    local file=$1
    local tier=$2
    local purpose=$3
    local reload_trigger=$4
    local read_time=$5

    # Check if file already has frontmatter
    if head -1 "$file" | grep -q "^---"; then
        echo "✓ $file (already has frontmatter)"
        return
    fi

    echo "Adding TIER $tier to $file"

    # Create temp file with frontmatter prepended
    cat > /tmp/tier_temp.md << EOF
---
tier: $tier
purpose: $purpose
reload_trigger: $reload_trigger
estimated_read_time: $read_time
---

EOF
    cat "$file" >> /tmp/tier_temp.md
    mv /tmp/tier_temp.md "$file"
}

# TIER 1 Files (Critical - Always load)
add_tier_frontmatter ".claude/templates/start-here.md" 1 "Framework orientation" "Always at session start" "5 minutes"
add_tier_frontmatter ".claude/templates/CLAUDE.md" 1 "Session protocols and enforcement" "Always at session start" "10 minutes"
add_tier_frontmatter ".claude/templates/development-rules.md" 1 "The 12 non-negotiable rules" "Always at session start, at 70% context" "15 minutes"
add_tier_frontmatter ".claude/READING-ORDER.md" 1 "Canonical file reading sequence" "When reading order unclear" "10 minutes"

# TIER 2 Files (Important - Load early)
add_tier_frontmatter ".claude/templates/session-checklist.md" 2 "Session start/end procedures" "At session start" "5 minutes"
add_tier_frontmatter ".claude/templates/context-priority.md" 2 "Context management and compression" "At 70% context usage" "10 minutes"
add_tier_frontmatter ".claude/templates/technical-decisions.md" 2 "Architecture decision records template" "When making/reviewing ADRs" "5 minutes"
add_tier_frontmatter ".claude/templates/service-registry.md" 2 "Service catalog template" "When working with services" "5 minutes"

# TIER 3 Files (Working references)
add_tier_frontmatter ".claude/templates/git-workflow.md" 3 "Git branching and commit strategy" "When committing or branching" "10 minutes"
add_tier_frontmatter ".claude/templates/refactoring-checklist.md" 3 "RED-GREEN-REFACTOR process" "After GREEN phase" "15 minutes"
add_tier_frontmatter ".claude/templates/requirements-review-checklist.md" 3 "Specification review process" "When reviewing specs" "10 minutes"
add_tier_frontmatter ".claude/templates/code-reuse-checklist.md" 3 "Before writing new code" "Before implementing new capability" "5 minutes"
add_tier_frontmatter ".claude/templates/implementation-CLAUDE.md" 3 "Implementation phase instructions" "During implementation" "5 minutes"
add_tier_frontmatter ".claude/templates/implementation-summary.md" 3 "Implementation session summary template" "After implementation complete" "3 minutes"
add_tier_frontmatter ".claude/templates/session-state.md" 3 "Session continuity template" "At session end" "5 minutes"

# TIER 4 Files (Templates - load when creating)
add_tier_frontmatter ".claude/templates/use-case-template.md" 4 "Use case specification template" "When creating new UC" "5 minutes"
add_tier_frontmatter ".claude/templates/service-spec.md" 4 "Service specification template" "When creating new service" "10 minutes"
add_tier_frontmatter ".claude/templates/benchmark-report.md" 4 "Performance benchmark template" "When benchmarking" "5 minutes"
add_tier_frontmatter ".claude/templates/library-evaluation.md" 4 "Library evaluation template" "When evaluating libraries" "5 minutes"
add_tier_frontmatter ".claude/templates/services-README-template.md" 4 "Services directory README template" "When creating services/ directory" "3 minutes"
add_tier_frontmatter ".claude/templates/research/paper-summary.md" 4 "Research paper summary template" "When summarizing papers" "3 minutes"
add_tier_frontmatter ".claude/templates/research/article-links.md" 4 "Article links collection template" "When collecting research links" "2 minutes"
add_tier_frontmatter ".claude/templates/research/implementation-readme.md" 4 "Implementation notes template" "When documenting implementation research" "3 minutes"

# Quick Reference Files (TIER 4)
add_tier_frontmatter ".claude/quick-ref/session-start.md" 4 "Session start quick checklist" "At session start (quick ref)" "2 minutes"
add_tier_frontmatter ".claude/quick-ref/tdd-cycle.md" 4 "TDD cycle quick reference" "During implementation (quick ref)" "2 minutes"
add_tier_frontmatter ".claude/quick-ref/git.md" 4 "Git commands quick reference" "When using git (quick ref)" "3 minutes"
add_tier_frontmatter ".claude/quick-ref/services.md" 4 "Service patterns quick reference" "When designing services (quick ref)" "5 minutes"
add_tier_frontmatter ".claude/quick-ref/commands.md" 4 "Common commands quick reference" "When need command reminder" "3 minutes"

# Guides (TIER 4)
add_tier_frontmatter ".claude/guides/research-organization.md" 4 "Research organization guide" "When organizing research" "10 minutes"

# TIER 5 Files (On-demand - subagents)
add_tier_frontmatter ".claude/subagents/service-extractor.md" 5 "Service extraction subagent" "On-demand via Task tool" "5 minutes to load"
add_tier_frontmatter ".claude/subagents/service-designer.md" 5 "Service design subagent" "On-demand via Task tool" "5 minutes to load"
add_tier_frontmatter ".claude/subagents/service-dependency-analyzer.md" 5 "Dependency analysis subagent" "On-demand via Task tool" "5 minutes to load"
add_tier_frontmatter ".claude/subagents/service-optimizer.md" 5 "Performance optimization subagent" "On-demand via Task tool" "5 minutes to load"
add_tier_frontmatter ".claude/subagents/service-library-finder.md" 5 "Library evaluation subagent" "On-demand via Task tool" "5 minutes to load"
add_tier_frontmatter ".claude/subagents/uc-service-tracer.md" 5 "Traceability validation subagent" "On-demand via Task tool" "5 minutes to load"

echo ""
echo "✅ TIER labels added to all framework files"
echo ""
echo "TIER Distribution:"
echo "  TIER 1 (Critical): 4 files"
echo "  TIER 2 (Important): 4 files"
echo "  TIER 3 (Working): 7 files"
echo "  TIER 4 (Templates/Quick-Ref): 14 files"
echo "  TIER 5 (Subagents): 6 files"
echo "  Total: 35 files"
