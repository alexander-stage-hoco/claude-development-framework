#!/bin/bash
# Claude Development Framework - Context Usage Estimator
# Version: 2.0
# Purpose: Estimate token usage before loading files into Claude context

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Token estimation constants
# Based on Claude tokenizer: ~4 chars per token average for English text
# Code tends to be ~3.5 chars per token due to symbols and structure
CHARS_PER_TOKEN_TEXT=4
CHARS_PER_TOKEN_CODE=3.5

# Context window limits
CONTEXT_WINDOW_TOTAL=200000
SAFE_USAGE_PERCENT=70
WARNING_THRESHOLD_PERCENT=80

echo "================================================================"
echo "Claude Framework - Context Usage Estimator"
echo "================================================================"
echo ""

# Function to estimate tokens for a file
estimate_file_tokens() {
    local file=$1
    local char_count=$(wc -m < "$file" 2>/dev/null || echo "0")

    # Determine if file is code or text based on extension
    local ext="${file##*.}"
    local divisor=$CHARS_PER_TOKEN_CODE

    case "$ext" in
        md|txt|rst)
            divisor=$CHARS_PER_TOKEN_TEXT
            ;;
        py|js|ts|go|java|c|cpp|rs|rb|sh|yaml|json)
            divisor=$CHARS_PER_TOKEN_CODE
            ;;
    esac

    # Calculate estimated tokens
    local tokens=$(echo "scale=0; $char_count / $divisor" | bc)
    echo "$tokens"
}

# Function to format numbers with commas
format_number() {
    printf "%'d" "$1" 2>/dev/null || echo "$1"
}

# Function to calculate percentage
calc_percentage() {
    local part=$1
    local total=$2
    echo "scale=1; $part * 100 / $total" | bc
}

# Parse arguments
TIER=""
PATTERN=""
SHOW_FILES=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --tier)
            TIER="$2"
            shift 2
            ;;
        --pattern)
            PATTERN="$2"
            shift 2
            ;;
        --files)
            SHOW_FILES=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            SHOW_FILES=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --tier N        Estimate only TIER N files (1-5)"
            echo "  --pattern GLOB  Estimate files matching pattern (e.g., '*.py')"
            echo "  --files         Show individual file estimates"
            echo "  --verbose       Show detailed breakdown"
            echo "  --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                          # Estimate all framework files"
            echo "  $0 --tier 1                 # Estimate only TIER 1 files"
            echo "  $0 --pattern '*.py'         # Estimate Python files only"
            echo "  $0 --tier 1 --verbose       # Detailed TIER 1 breakdown"
            echo ""
            echo "Context Window:"
            echo "  Total: $(format_number $CONTEXT_WINDOW_TOTAL) tokens"
            echo "  Safe usage: ${SAFE_USAGE_PERCENT}% ($(format_number $((CONTEXT_WINDOW_TOTAL * SAFE_USAGE_PERCENT / 100))) tokens)"
            echo "  Warning at: ${WARNING_THRESHOLD_PERCENT}% ($(format_number $((CONTEXT_WINDOW_TOTAL * WARNING_THRESHOLD_PERCENT / 100))) tokens)"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run '$0 --help' for usage information"
            exit 1
            ;;
    esac
done

# Build file list based on criteria
FILES=()

if [ -n "$PATTERN" ]; then
    echo "🔍 Finding files matching pattern: $PATTERN"
    while IFS= read -r file; do
        FILES+=("$file")
    done < <(find . -type f -name "$PATTERN" ! -path "*/\.*" ! -path "*/node_modules/*" ! -path "*/venv/*" 2>/dev/null)
elif [ -n "$TIER" ]; then
    echo "🔍 Finding TIER $TIER files..."
    # Find files with tier frontmatter matching the specified tier
    # Search in .claude, docs, and planning directories
    for dir in .claude docs planning; do
        if [ -d "$dir" ]; then
            while IFS= read -r file; do
                if grep -q "^tier: $TIER$" "$file" 2>/dev/null; then
                    FILES+=("$file")
                fi
            done < <(find "$dir" -type f -name "*.md" 2>/dev/null)
        fi
    done
else
    echo "🔍 Finding all framework files..."
    # Default: All framework markdown and template files
    while IFS= read -r file; do
        FILES+=("$file")
    done < <(find .claude docs -type f -name "*.md" 2>/dev/null)
fi

if [ ${#FILES[@]} -eq 0 ]; then
    echo "❌ No files found matching criteria"
    exit 1
fi

echo "   Found ${#FILES[@]} files"
echo ""

# Estimate tokens for each file
# Use parallel arrays for bash 3.2 compatibility
FILE_LIST=()
TOKEN_LIST=()
TOTAL_TOKENS=0

echo "📊 Estimating token usage..."
echo ""

for file in "${FILES[@]}"; do
    tokens=$(estimate_file_tokens "$file")
    FILE_LIST+=("$file")
    TOKEN_LIST+=("$tokens")
    TOTAL_TOKENS=$((TOTAL_TOKENS + tokens))
done

# Calculate percentages
SAFE_LIMIT=$((CONTEXT_WINDOW_TOTAL * SAFE_USAGE_PERCENT / 100))
WARNING_LIMIT=$((CONTEXT_WINDOW_TOTAL * WARNING_THRESHOLD_PERCENT / 100))
USAGE_PERCENT=$(calc_percentage $TOTAL_TOKENS $CONTEXT_WINDOW_TOTAL)

# Print summary
echo "================================================================"
echo "Summary"
echo "================================================================"
echo ""
echo "Total Files: ${#FILES[@]}"
echo "Estimated Tokens: $(format_number $TOTAL_TOKENS)"
echo "Context Window: $(format_number $CONTEXT_WINDOW_TOTAL) tokens"
echo "Usage: ${USAGE_PERCENT}%"
echo ""

# Status indicator
if (( $(echo "$USAGE_PERCENT < $SAFE_USAGE_PERCENT" | bc -l) )); then
    echo -e "${GREEN}✅ SAFE${NC} - Well within context limits"
elif (( $(echo "$USAGE_PERCENT < $WARNING_THRESHOLD_PERCENT" | bc -l) )); then
    echo -e "${YELLOW}⚠️  CAUTION${NC} - Approaching limits, consider compaction"
else
    echo -e "${RED}🚨 WARNING${NC} - Exceeds safe usage, compaction required"
fi
echo ""

# Remaining capacity
REMAINING=$((CONTEXT_WINDOW_TOTAL - TOTAL_TOKENS))
echo "Remaining Capacity: $(format_number $REMAINING) tokens"
echo ""

# Calculate average tokens (needed for recommendations)
TOTAL_FILES=${#FILE_LIST[@]}
AVG_TOKENS=$((TOTAL_TOKENS / TOTAL_FILES))

# Show file breakdown if requested
if [ "$SHOW_FILES" = true ]; then
    echo "================================================================"
    echo "File Breakdown"
    echo "================================================================"
    echo ""

    # Create temporary file for sorting
    TEMP_FILE=$(mktemp)
    for i in "${!FILE_LIST[@]}"; do
        echo "${TOKEN_LIST[$i]} ${FILE_LIST[$i]}" >> "$TEMP_FILE"
    done

    # Sort by token count (descending) and display
    while read -r tokens file; do
        file_percent=$(calc_percentage $tokens $TOTAL_TOKENS)

        # Color code by size
        if (( tokens > 10000 )); then
            color=$RED
        elif (( tokens > 5000 )); then
            color=$YELLOW
        else
            color=$GREEN
        fi

        printf "  ${color}%7s tokens${NC} (%5.1f%%) - %s\n" "$(format_number $tokens)" "$file_percent" "$file"
    done < <(sort -rn "$TEMP_FILE")

    rm -f "$TEMP_FILE"
    echo ""
fi

# Verbose mode: additional statistics
if [ "$VERBOSE" = true ]; then
    echo "================================================================"
    echo "Detailed Statistics"
    echo "================================================================"
    echo ""

    # Calculate min, max (average already calculated above)
    MIN_TOKENS=999999999
    MAX_TOKENS=0
    MIN_FILE=""
    MAX_FILE=""

    for i in "${!TOKEN_LIST[@]}"; do
        tokens=${TOKEN_LIST[$i]}
        file=${FILE_LIST[$i]}
        if (( tokens < MIN_TOKENS )); then
            MIN_TOKENS=$tokens
            MIN_FILE=$file
        fi
        if (( tokens > MAX_TOKENS )); then
            MAX_TOKENS=$tokens
            MAX_FILE=$file
        fi
    done

    echo "Average: $(format_number $AVG_TOKENS) tokens/file"
    echo "Minimum: $(format_number $MIN_TOKENS) tokens ($MIN_FILE)"
    echo "Maximum: $(format_number $MAX_TOKENS) tokens ($MAX_FILE)"
    echo ""

    # Distribution
    echo "Size Distribution:"

    TINY=0    # < 1000 tokens
    SMALL=0   # 1000-2999
    MEDIUM=0  # 3000-5999
    LARGE=0   # 6000-9999
    HUGE=0    # >= 10000

    for tokens in "${TOKEN_LIST[@]}"; do
        if (( tokens < 1000 )); then
            TINY=$((TINY + 1))
        elif (( tokens < 3000 )); then
            SMALL=$((SMALL + 1))
        elif (( tokens < 6000 )); then
            MEDIUM=$((MEDIUM + 1))
        elif (( tokens < 10000 )); then
            LARGE=$((LARGE + 1))
        else
            HUGE=$((HUGE + 1))
        fi
    done

    echo "  < 1K tokens:   $TINY files"
    echo "  1K - 3K:       $SMALL files"
    echo "  3K - 6K:       $MEDIUM files"
    echo "  6K - 10K:      $LARGE files"
    echo "  >= 10K:        $HUGE files"
    echo ""
fi

# Recommendations
echo "================================================================"
echo "Recommendations"
echo "================================================================"
echo ""

if (( $(echo "$USAGE_PERCENT < $SAFE_USAGE_PERCENT" | bc -l) )); then
    echo "✅ Current usage is healthy. No action needed."
    echo ""
    echo "You can safely load additional files:"
    ADDITIONAL_CAPACITY=$((SAFE_LIMIT - TOTAL_TOKENS))
    echo "  - Up to $(format_number $ADDITIONAL_CAPACITY) more tokens"
    echo "  - Approximately $((ADDITIONAL_CAPACITY / AVG_TOKENS)) more average-sized files"
elif (( $(echo "$USAGE_PERCENT < $WARNING_THRESHOLD_PERCENT" | bc -l) )); then
    echo "⚠️  Approaching context limits. Consider:"
    echo ""
    echo "1. Load only TIER 1 files at session start"
    echo "2. Use 'on-demand' loading for TIER 3-5 files"
    echo "3. Consider compacting large documentation files"
    echo "4. Use quick-ref files instead of full guides"
    echo ""
    echo "Priority files to load:"
    echo "  - .claude/CLAUDE.md"
    echo "  - .claude/development-rules.md"
    echo "  - planning/current-iteration.md"
    echo "  - planning/session-state.md"
else
    echo "🚨 Context usage too high! Immediate action required:"
    echo ""
    echo "1. Load ONLY TIER 1 files (critical)"
    echo "2. Skip all documentation (use quick-ref instead)"
    echo "3. Load working files on-demand only"
    echo "4. Consider splitting large files"
    echo ""
    EXCESS=$((TOTAL_TOKENS - SAFE_LIMIT))
    echo "Need to reduce by: $(format_number $EXCESS) tokens"
fi

echo ""
echo "================================================================"

# Exit with appropriate code
if (( $(echo "$USAGE_PERCENT >= $WARNING_THRESHOLD_PERCENT" | bc -l) )); then
    exit 1
else
    exit 0
fi
