#!/bin/bash
# Claude Development Framework - Session State Auto-Generator
# Automatically generates session-state.md for session continuity

set -e

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)

echo "🔄 Generating Session State..."
echo ""

# Check if we're in a project directory
if [ ! -d "planning" ]; then
    echo "❌ ERROR: planning/ directory not found"
    echo "   Run this from a project root directory (not template)"
    exit 1
fi

OUTPUT_FILE="planning/session-state.md"
CURRENT_ITERATION="planning/current-iteration.md"

# Function to get git info
get_git_info() {
    if [ -d ".git" ]; then
        git log -5 --oneline 2>/dev/null || echo "No git history yet"
    else
        echo "Not a git repository"
    fi
}

# Function to count files
count_files() {
    local pattern=$1
    find . -name "$pattern" 2>/dev/null | wc -l | tr -d ' '
}

# Function to get current branch
get_branch() {
    if [ -d ".git" ]; then
        git branch --show-current 2>/dev/null || echo "main"
    else
        echo "N/A"
    fi
}

# Generate session state
cat > "$OUTPUT_FILE" << EOF
# Session State

**Last Updated**: $DATE $TIME
**Auto-Generated**: Yes (review and edit as needed)

---

## Current Context

**Branch**: $(get_branch)
**Session**: $(date +%Y-%m-%d)

---

## Active Work

EOF

# Add current iteration content
if [ -f "$CURRENT_ITERATION" ]; then
    echo "Reading current iteration status..."

    # Extract active work section from current-iteration.md
    if grep -q "## Active Work" "$CURRENT_ITERATION"; then
        sed -n '/## Active Work/,/^##/p' "$CURRENT_ITERATION" | sed '$ d' >> "$OUTPUT_FILE"
    else
        echo "**Status**: See \`planning/current-iteration.md\` for details" >> "$OUTPUT_FILE"
    fi
    echo "" >> "$OUTPUT_FILE"
else
    echo "**Status**: No current iteration defined yet" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
fi

# Add project statistics
cat >> "$OUTPUT_FILE" << EOF

## Project Statistics

**Files**:
- Use Cases: $(count_files "UC-*.md") specifications
- Services: $(count_files "service-spec.md") services
- Tests: $(count_files "test_*.py") test files

**Recent Activity**:
EOF

echo '```' >> "$OUTPUT_FILE"
get_git_info >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"

cat >> "$OUTPUT_FILE" << EOF

---

## Work Completed (This Session)

<!-- Auto-generated placeholder - fill in what was accomplished -->

**Implemented**:
- [ ] Item 1
- [ ] Item 2

**Tests**:
- [ ] All tests passing?
- [ ] Coverage maintained?

**Documentation**:
- [ ] Specs updated?
- [ ] ADRs documented?

---

## What's Next

<!-- Auto-generated placeholder - edit for next session -->

**Immediate Tasks**:
1. Complete current iteration
2. Run tests
3. Update documentation

**Blockers**:
- None identified

**Decisions Needed**:
- None identified

---

## Files to Load (Next Session)

**TIER 1 (Critical)**:
- \`.claude/CLAUDE.md\` - Session protocol
- \`.claude/development-rules.md\` - The 12 rules
- \`planning/current-iteration.md\` - Current work
- \`planning/session-state.md\` - This file

**Working Context**:
- Current use case specifications
- Current service specifications
- Active implementation files

---

## Context Notes

**Current Focus**: [Describe main focus area]

**Key Decisions Made**:
- [ADR reference or decision summary]

**Testing Status**:
- Tests passing: [N/N]
- Coverage: [X%]

**Known Issues**:
- None

---

## For Claude

**When starting next session**:
1. Read this file first (session-state.md)
2. Read current-iteration.md for active work
3. Re-read development-rules.md to refresh rules
4. Load working context files listed above
5. Report context usage percentage
6. Continue work where left off

**Context Management**:
- Last session context: [X%]
- Estimated next session start: [Y%]
- Files to prioritize: TIER 1 + working context

---

**Auto-Generated**: $DATE $TIME
**Review**: Please review and update placeholders before committing
**Command**: \`git add planning/session-state.md && git commit -m "docs: update session state"\`
EOF

echo "✅ Session state generated: $OUTPUT_FILE"
echo ""
echo "📝 Next steps:"
echo "   1. Review and edit $OUTPUT_FILE"
echo "   2. Fill in 'Work Completed' section"
echo "   3. Update 'What's Next' section"
echo "   4. Commit: git add $OUTPUT_FILE && git commit -m 'docs: update session state'"
echo ""
echo "💡 Tip: Run this at the END of each session for continuity"
