#!/bin/bash
# Claude Development Framework - Add Template Versions
# Adds version footer to all template files

set -e

DATE=$(date +%Y-%m-%d)

FOOTER="---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: $DATE
**Compatibility**: Framework v2.0+"

echo "Adding version footers to template files..."
echo ""

COUNT=0

# Process all template files
for file in .claude/templates/*.md .claude/templates/research/*.md; do
    if [ ! -f "$file" ]; then
        continue
    fi

    # Check if already has version footer
    if grep -q "Template Version" "$file" 2>/dev/null; then
        echo "✓ $file (already has version)"
    else
        echo "Adding footer to $file"
        echo "" >> "$file"
        echo "$FOOTER" >> "$file"
        COUNT=$((COUNT + 1))
    fi
done

echo ""
if [ $COUNT -eq 0 ]; then
    echo "✅ All templates already have version footers"
else
    echo "✅ Added version footers to $COUNT template files"
fi
