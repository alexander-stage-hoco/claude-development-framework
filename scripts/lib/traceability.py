"""
UC-Service Traceability Library
Parses and validates bidirectional traceability between use cases and services
"""

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Set


@dataclass
class UseCase:
    """Represents a use case with service references"""
    id: str
    name: str
    file_path: Path
    services_used: List[str]
    has_justification: bool


@dataclass
class Service:
    """Represents a service with UC references"""
    id: str
    name: str
    file_path: Path
    used_by: List[str]


class TraceabilityParser:
    """Parses UC and service files for traceability information"""

    def parse_use_cases(self, uc_dir: Path) -> List[UseCase]:
        """Parse all UC files for services used"""
        if not uc_dir.exists():
            return []

        use_cases = []
        for uc_file in sorted(uc_dir.glob("UC-*.md")):
            try:
                uc = self._parse_uc_file(uc_file)
                use_cases.append(uc)
            except Exception as e:
                print(f"Warning: Error parsing {uc_file}: {e}")

        return use_cases

    def _parse_uc_file(self, file_path: Path) -> UseCase:
        """Extract services from a single UC file"""
        content = file_path.read_text()

        # Extract UC ID from filename (UC-001, UC-002, etc.)
        filename = file_path.stem
        uc_id_match = re.match(r'(UC-\d+)', filename)
        uc_id = uc_id_match.group(1) if uc_id_match else filename

        # Find "Services Used" section
        # Pattern matches markdown table in "## Services Used" section
        services_pattern = r'##\s+Services\s+Used\s*\n\s*\|[^\n]+\|[^\n]+\|\s*\n\s*\|[-|\s]+\|\s*\n((?:\s*\|[^\n]+\|\s*\n)*)'
        match = re.search(services_pattern, content, re.IGNORECASE)

        services = []
        if match:
            table_rows = match.group(1)
            # Parse each table row
            for line in table_rows.strip().split('\n'):
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    # Service name is typically in column 1 or 2 (after empty first column)
                    if len(parts) >= 2 and parts[1]:
                        # Extract service ID (SVC-XXX) or service name
                        service_ref = parts[1]
                        # Clean up formatting
                        service_ref = re.sub(r'[\[\]`*]', '', service_ref).strip()
                        if service_ref and not service_ref.startswith('-'):
                            services.append(service_ref)

        # Check for justification if no services
        has_justification = False
        if not services:
            justification_patterns = [
                r'No services needed',
                r'No services required',
                r'Justification:',
                r'Pure UI',
                r'No backend interaction'
            ]
            for pattern in justification_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    has_justification = True
                    break

        return UseCase(
            id=uc_id,
            name=filename,
            file_path=file_path,
            services_used=services,
            has_justification=has_justification
        )

    def parse_services(self, services_dir: Path) -> List[Service]:
        """Parse all service specs for UC references"""
        if not services_dir.exists():
            return []

        services = []
        # Find all service-spec.md files in subdirectories
        for service_spec in services_dir.glob("*/service-spec.md"):
            try:
                service = self._parse_service_file(service_spec)
                services.append(service)
            except Exception as e:
                print(f"Warning: Error parsing {service_spec}: {e}")

        return services

    def _parse_service_file(self, file_path: Path) -> Service:
        """Extract UC references from a single service spec"""
        content = file_path.read_text()

        # Extract service ID from content (Service ID: SVC-XXX)
        id_match = re.search(r'Service\s+ID[:\s]+([A-Z]+-\d+)', content, re.IGNORECASE)
        service_id = id_match.group(1) if id_match else file_path.parent.name

        # Service name from parent directory
        service_name = file_path.parent.name

        # Find "Used By" section (in "Use Cases" or "Used By" heading)
        # Pattern matches markdown table
        used_by_pattern = r'##\s+(?:Used\s+By|Use\s+Cases)\s*\n.*?\n\s*\|[^\n]+\|[^\n]+\|\s*\n\s*\|[-|\s]+\|\s*\n((?:\s*\|[^\n]+\|\s*\n)*)'
        match = re.search(used_by_pattern, content, re.IGNORECASE | re.DOTALL)

        used_by = []
        if match:
            table_rows = match.group(1)
            # Parse each table row
            for line in table_rows.strip().split('\n'):
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    # UC ID is typically in first column (after empty first column)
                    if len(parts) >= 2 and parts[1]:
                        uc_ref = parts[1]
                        # Extract UC-XXX pattern
                        uc_match = re.search(r'(UC-\d+)', uc_ref)
                        if uc_match:
                            used_by.append(uc_match.group(1))

        return Service(
            id=service_id,
            name=service_name,
            file_path=file_path,
            used_by=used_by
        )


class TraceabilityValidator:
    """Validates bidirectional UC-Service traceability"""

    def validate(self, use_cases: List[UseCase], services: List[Service]) -> Dict:
        """Run all validation checks and return issues"""
        issues = {
            'orphan_services': [],
            'unjustified_serviceless_ucs': [],
            'missing_services': [],
            'bidirectional_mismatches': []
        }

        # Build lookup maps
        service_ids = {s.id for s in services}
        service_by_id = {s.id: s for s in services}
        uc_ids = {uc.id for uc in use_cases}

        # Check 1: UCs with no services (and no justification)
        for uc in use_cases:
            if not uc.services_used and not uc.has_justification:
                issues['unjustified_serviceless_ucs'].append(uc)

        # Check 2: Services not used by any UC (orphans)
        used_services = set()
        for uc in use_cases:
            used_services.update(uc.services_used)

        for service in services:
            # Check if service ID or name is referenced
            if service.id not in used_services and service.name not in used_services:
                # Also check if any UC references this service
                is_used = False
                for uc in use_cases:
                    if service.id in uc.services_used or service.name in uc.services_used:
                        is_used = True
                        break
                if not is_used:
                    issues['orphan_services'].append(service)

        # Check 3: UCs reference non-existent services
        for uc in use_cases:
            for service_ref in uc.services_used:
                # Check if service exists by ID or name
                if service_ref not in service_ids:
                    # Check if it matches a service name
                    found = any(s.name == service_ref for s in services)
                    if not found:
                        issues['missing_services'].append({
                            'uc': uc.id,
                            'service': service_ref,
                            'uc_file': str(uc.file_path)
                        })

        # Check 4: Bidirectional consistency
        for uc in use_cases:
            for service_ref in uc.services_used:
                # Find service by ID or name
                service = service_by_id.get(service_ref)
                if not service:
                    # Try by name
                    service = next((s for s in services if s.name == service_ref), None)

                if service:
                    # Check if service lists this UC in "Used By"
                    if uc.id not in service.used_by:
                        issues['bidirectional_mismatches'].append({
                            'uc': uc.id,
                            'service': service.id,
                            'issue': f'UC references service but service does not list UC in "Used By" section',
                            'uc_file': str(uc.file_path),
                            'service_file': str(service.file_path)
                        })

        # Check reverse direction: services listing UCs that don't reference them
        for service in services:
            for uc_ref in service.used_by:
                uc = next((u for u in use_cases if u.id == uc_ref), None)
                if uc:
                    # Check if UC lists this service
                    if service.id not in uc.services_used and service.name not in uc.services_used:
                        issues['bidirectional_mismatches'].append({
                            'uc': uc_ref,
                            'service': service.id,
                            'issue': f'Service lists UC but UC does not reference service',
                            'uc_file': str(uc.file_path),
                            'service_file': str(service.file_path)
                        })

        return issues


def format_report(use_cases: List[UseCase], services: List[Service], issues: Dict) -> str:
    """Format validation results as a readable report"""
    lines = []

    lines.append("=" * 60)
    lines.append("UC-Service Traceability Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Use Cases: {len(use_cases)}")
    lines.append(f"Services: {len(services)}")
    lines.append("")

    has_issues = any(issues.values())

    if not has_issues:
        lines.append("✅ ALL CHECKS PASSED")
        lines.append("")
        lines.append("Summary:")
        lines.append(f"  - {len(use_cases)} use cases analyzed")
        lines.append(f"  - {len(services)} services analyzed")
        lines.append(f"  - 100% bidirectional traceability")
        lines.append("")
    else:
        lines.append("❌ ISSUES FOUND")
        lines.append("")

        if issues['unjustified_serviceless_ucs']:
            lines.append("❌ Use Cases Without Services (No Justification):")
            for uc in issues['unjustified_serviceless_ucs']:
                lines.append(f"   - {uc.id}: {uc.file_path}")
                lines.append(f"     Fix: Add 'Services Used' table OR add justification")
            lines.append("")

        if issues['orphan_services']:
            lines.append("⚠️  Orphan Services (Not Used By Any UC):")
            for svc in issues['orphan_services']:
                lines.append(f"   - {svc.id} ({svc.name}): {svc.file_path}")
                lines.append(f"     Fix: Remove service OR add UC that uses it")
            lines.append("")

        if issues['missing_services']:
            lines.append("❌ Missing Service References:")
            for issue in issues['missing_services']:
                lines.append(f"   - {issue['uc']} references '{issue['service']}' (doesn't exist)")
                lines.append(f"     File: {issue['uc_file']}")
                lines.append(f"     Fix: Create service OR fix UC reference")
            lines.append("")

        if issues['bidirectional_mismatches']:
            lines.append("❌ Bidirectional Traceability Mismatches:")
            for issue in issues['bidirectional_mismatches']:
                lines.append(f"   - {issue['uc']} ↔ {issue['service']}: {issue['issue']}")
                lines.append(f"     UC: {issue['uc_file']}")
                lines.append(f"     Service: {issue['service_file']}")
                lines.append(f"     Fix: Update both files to match")
            lines.append("")

        lines.append("Summary:")
        lines.append(f"  {len(issues['unjustified_serviceless_ucs'])} serviceless UCs")
        lines.append(f"  {len(issues['orphan_services'])} orphan services")
        lines.append(f"  {len(issues['missing_services'])} missing service refs")
        lines.append(f"  {len(issues['bidirectional_mismatches'])} mismatches")
        lines.append("")

    return "\n".join(lines)
