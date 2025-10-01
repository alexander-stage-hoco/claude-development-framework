#!/bin/bash
# Claude Development Framework - Service Registry Updater
# Automatically updates .claude/service-registry.md from service specifications

set -e

DATE=$(date +%Y-%m-%d)

echo "📋 Updating Service Registry..."
echo ""

# Check if we're in a project directory
if [ ! -d "services" ]; then
    echo "⚠️  services/ directory not found"
    echo "   This might be a template or project without services yet"
    echo "   Creating placeholder registry..."
    create_placeholder=true
else
    create_placeholder=false
fi

OUTPUT_FILE=".claude/service-registry.md"

# Function to extract value from service spec
extract_field() {
    local file=$1
    local field=$2
    grep "^**$field" "$file" 2>/dev/null | sed "s/^**$field[:\s]*//; s/\*\*$//" | head -1 || echo "N/A"
}

# Function to extract service ID
extract_service_id() {
    local file=$1
    grep "^**Service ID" "$file" 2>/dev/null | sed 's/^**Service ID[:\s]*//; s/\*\*$//' | head -1 || echo "SVC-???"
}

# Function to extract dependencies
extract_dependencies() {
    local file=$1
    # Look for dependency table and extract service names
    sed -n '/## Dependencies/,/^##/p' "$file" 2>/dev/null | \
        grep "^|" | \
        grep -v "^|[-\s]*|" | \
        grep -v "Service\s*|" | \
        awk -F'|' '{print $2}' | \
        tr -d ' ' | \
        grep -v "^$" | \
        tr '\n' ', ' | \
        sed 's/,$//'
}

# Function to extract "Used By" UCs
extract_used_by() {
    local file=$1
    # Look for Use Cases / Used By table and extract UC IDs
    sed -n '/## Used By/,/^##/{/## Used By/d; /^##/d; p}' "$file" 2>/dev/null | \
        grep "^|" | \
        grep -v "^|[-\s]*|" | \
        grep -v "Use Case" | \
        awk -F'|' '{print $2}' | \
        grep -o "UC-[0-9]\+" | \
        tr '\n' ', ' | \
        sed 's/,$//'
}

# Create registry file
cat > "$OUTPUT_FILE" << 'EOF'
---
tier: 2
purpose: Service catalog and traceability
reload_trigger: When working with services
estimated_read_time: 5 minutes
---

# Service Registry

**Purpose**: Central catalog of all services with bidirectional UC-Service traceability

**Last Updated**: AUTO_GENERATED_DATE
**Total Services**: AUTO_GENERATED_COUNT
**Auto-Generated**: Yes (by scripts/update-service-registry.sh)

---

## How to Update This Registry

**Automatic** (Recommended):
```bash
./scripts/update-service-registry.sh
```

**Manual**:
1. Add new row to table below
2. Ensure bidirectional traceability (UC ↔ Service)
3. Update counts

---

## Service Catalog

| Service ID | Name | Status | Layer | Dependencies | Used By (UCs) | Spec File |
|------------|------|--------|-------|--------------|---------------|-----------|
EOF

# Count services and add rows
service_count=0

if [ "$create_placeholder" = false ]; then
    # Scan services directory
    for service_dir in services/*/; do
        if [ ! -d "$service_dir" ]; then
            continue
        fi

        service_spec="$service_dir/service-spec.md"
        if [ ! -f "$service_spec" ]; then
            continue
        fi

        # Extract metadata
        service_id=$(extract_service_id "$service_spec")
        service_name=$(basename "$service_dir")
        status=$(extract_field "$service_spec" "Status")
        dependencies=$(extract_dependencies "$service_spec")
        used_by=$(extract_used_by "$service_spec")

        # Determine layer (heuristic: count dependencies)
        dep_count=$(echo "$dependencies" | grep -o "," | wc -l | tr -d ' ')
        if [ -z "$dependencies" ] || [ "$dependencies" = "N/A" ]; then
            layer="1"
        elif [ "$dep_count" -le 1 ]; then
            layer="2"
        else
            layer="3"
        fi

        # Add row to table
        echo "| $service_id | $service_name | $status | Layer $layer | ${dependencies:-None} | ${used_by:-None} | \`services/$service_name/service-spec.md\` |" >> "$OUTPUT_FILE"

        service_count=$((service_count + 1))
    done
fi

# If no services found, add placeholder
if [ $service_count -eq 0 ]; then
    echo "| SVC-001 | ExampleService | Draft | Layer 1 | None | UC-001 | \`services/example-service/service-spec.md\` |" >> "$OUTPUT_FILE"
    echo "| (add services here) | ... | ... | ... | ... | ... | ... |" >> "$OUTPUT_FILE"
fi

# Add rest of document
cat >> "$OUTPUT_FILE" << 'EOF'

---

## Service Layers

**Layer 1** (Foundation):
- No dependencies on other services
- Infrastructure services (DB, cache, logging)
- Utilities and helpers

**Layer 2** (Domain):
- Depend on Layer 1 only
- Core business logic services
- Domain-specific operations

**Layer 3** (Application):
- Depend on Layer 1 and 2
- Orchestration and workflow services
- User-facing service compositions

**Rule**: Services can only depend on lower layers (prevents circular dependencies)

---

## Traceability Matrix

### Services → Use Cases

**Purpose**: Which UCs use each service?

| Service | Use Cases |
|---------|-----------|
EOF

# Generate traceability matrix
if [ "$create_placeholder" = false ] && [ $service_count -gt 0 ]; then
    for service_dir in services/*/; do
        if [ ! -d "$service_dir" ]; then
            continue
        fi

        service_spec="$service_dir/service-spec.md"
        if [ ! -f "$service_spec" ]; then
            continue
        fi

        service_id=$(extract_service_id "$service_spec")
        used_by=$(extract_used_by "$service_spec")

        echo "| $service_id | ${used_by:-None} |" >> "$OUTPUT_FILE"
    done
else
    echo "| SVC-001 | UC-001, UC-002 |" >> "$OUTPUT_FILE"
    echo "| (add services here) | ... |" >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << 'EOF'

### Use Cases → Services

**Purpose**: Which services does each UC need?

**See**: Each use case specification should have a "Services Used" section

**Validation**: Run `./scripts/validate-traceability.py` to check bidirectional traceability

---

## Service Status Definitions

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **Draft** | Specification in progress | Complete spec, get approval |
| **Design** | Spec complete, not implemented | Write tests, implement |
| **Implemented** | Code exists, tests passing | Integration testing, optimization |
| **Optimized** | Performance tuned | Maintenance mode |
| **Deprecated** | Being phased out | Migration plan needed |

---

## Dependency Graph

**View Dependencies**:
```bash
# Manual inspection
grep "## Dependencies" services/*/service-spec.md

# Automated validation
./scripts/validate-traceability.py
```

**Check for Circular Dependencies**:
Use service-dependency-analyzer subagent to detect cycles

---

## Adding a New Service

1. **Extract** from use cases (use service-extractor subagent)
2. **Create** specification: `services/[service-name]/service-spec.md`
3. **Update** registry: Run `./scripts/update-service-registry.sh`
4. **Validate** traceability: Run `./scripts/validate-traceability.py`
5. **Reference** in UCs: Add to "Services Used" section of relevant UCs

---

## Maintenance

**When to Update**:
- After creating new service specification
- After modifying service dependencies
- After updating UC-Service relationships
- Weekly audit (verify all services listed)

**How to Update**:
```bash
./scripts/update-service-registry.sh
git add .claude/service-registry.md
git commit -m "docs: update service registry"
```

---

**Template Version**: 1.0
**Framework**: Claude Development Framework v2.0
**Last Updated**: AUTO_FINAL_DATE
**Compatibility**: Framework v2.0+
EOF

# Replace placeholders
sed -i '' "s/AUTO_GENERATED_DATE/$DATE/g" "$OUTPUT_FILE" 2>/dev/null || sed -i "s/AUTO_GENERATED_DATE/$DATE/g" "$OUTPUT_FILE"
sed -i '' "s/AUTO_GENERATED_COUNT/$service_count/g" "$OUTPUT_FILE" 2>/dev/null || sed -i "s/AUTO_GENERATED_COUNT/$service_count/g" "$OUTPUT_FILE"
sed -i '' "s/AUTO_FINAL_DATE/$DATE/g" "$OUTPUT_FILE" 2>/dev/null || sed -i "s/AUTO_FINAL_DATE/$DATE/g" "$OUTPUT_FILE"

echo "✅ Service registry updated: $OUTPUT_FILE"
echo ""
echo "📊 Summary:"
echo "   - Services found: $service_count"
echo "   - Traceability matrix: Generated"
echo "   - Layers: Assigned heuristically"
echo ""
echo "💡 Next steps:"
echo "   1. Review $OUTPUT_FILE for accuracy"
echo "   2. Run: ./scripts/validate-traceability.py (verify bidirectional links)"
echo "   3. Commit: git add $OUTPUT_FILE && git commit -m 'docs: update service registry'"
echo ""
echo "🔗 Validate traceability: ./scripts/validate-traceability.py"
