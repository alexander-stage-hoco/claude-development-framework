#!/usr/bin/env python3
"""
Claude Development Framework - Spec-Code Alignment Library
Version: 2.0
Purpose: Parse and validate alignment between specifications and BDD tests

This library detects spec-code drift by comparing:
- Use case acceptance criteria vs BDD scenarios
- Scenario counts vs criteria counts
- Orphaned implementations (tests without specs)
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Set, Tuple


@dataclass
class UseCase:
    """Represents a use case specification with acceptance criteria."""
    uc_id: str
    file_path: Path
    acceptance_criteria: List[str] = field(default_factory=list)
    bdd_file_referenced: str = ""

    def __repr__(self):
        return f"UseCase({self.uc_id}, {len(self.acceptance_criteria)} criteria)"


@dataclass
class BDDFeature:
    """Represents a BDD feature file with scenarios."""
    feature_name: str
    file_path: Path
    scenarios: List[str] = field(default_factory=list)
    uc_reference: str = ""

    def __repr__(self):
        return f"BDDFeature({self.feature_name}, {len(self.scenarios)} scenarios)"


@dataclass
class AlignmentIssue:
    """Represents a spec-code alignment issue."""
    issue_type: str
    uc_id: str
    feature_name: str
    message: str
    severity: str  # 'error', 'warning'

    def __repr__(self):
        return f"[{self.severity.upper()}] {self.issue_type}: {self.message}"


class AlignmentParser:
    """Parses use case specifications and BDD feature files."""

    @staticmethod
    def parse_use_cases(uc_dir: Path) -> Dict[str, UseCase]:
        """
        Parse all use case specifications.

        Args:
            uc_dir: Directory containing UC-*.md files

        Returns:
            Dictionary mapping UC IDs to UseCase objects
        """
        use_cases = {}

        if not uc_dir.exists():
            return use_cases

        for uc_file in uc_dir.glob("UC-*.md"):
            uc = AlignmentParser._parse_use_case_file(uc_file)
            if uc:
                use_cases[uc.uc_id] = uc

        return use_cases

    @staticmethod
    def _parse_use_case_file(uc_file: Path) -> UseCase:
        """Parse a single use case file."""
        content = uc_file.read_text()

        # Extract UC ID from filename
        uc_id_match = re.match(r"(UC-\d+)", uc_file.name)
        if not uc_id_match:
            return None
        uc_id = uc_id_match.group(1)

        # Extract acceptance criteria
        criteria = AlignmentParser._extract_acceptance_criteria(content)

        # Extract BDD file reference
        bdd_ref = AlignmentParser._extract_bdd_reference(content)

        return UseCase(
            uc_id=uc_id,
            file_path=uc_file,
            acceptance_criteria=criteria,
            bdd_file_referenced=bdd_ref
        )

    @staticmethod
    def _extract_acceptance_criteria(content: str) -> List[str]:
        """
        Extract acceptance criteria from use case content.

        Looks for "## Acceptance Criteria" section and extracts items.
        """
        criteria = []

        # Find acceptance criteria section
        ac_match = re.search(
            r'## Acceptance Criteria\s*\n(.*?)(?=\n##|\Z)',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if not ac_match:
            return criteria

        ac_section = ac_match.group(1)

        # Extract numbered or bulleted items
        # Pattern: "1. ", "- ", "* ", etc.
        for line in ac_section.split('\n'):
            line = line.strip()
            if re.match(r'^(\d+\.|\-|\*|\+)\s+', line):
                # Remove leading marker
                criterion = re.sub(r'^(\d+\.|\-|\*|\+)\s+', '', line)
                if criterion:
                    criteria.append(criterion)

        return criteria

    @staticmethod
    def _extract_bdd_reference(content: str) -> str:
        """
        Extract BDD feature file reference from use case.

        Looks for patterns like:
        - "BDD File: `features/uc-001-example.feature`"
        - "Feature File: features/uc-001-example.feature"
        """
        # Pattern 1: Markdown code format
        match = re.search(
            r'BDD File:\s*`([^`]+\.feature)`',
            content,
            re.IGNORECASE
        )
        if match:
            return match.group(1)

        # Pattern 2: Plain text
        match = re.search(
            r'(?:BDD|Feature) File:\s*([^\s\n]+\.feature)',
            content,
            re.IGNORECASE
        )
        if match:
            return match.group(1)

        return ""

    @staticmethod
    def parse_bdd_features(bdd_dir: Path) -> Dict[str, BDDFeature]:
        """
        Parse all BDD feature files.

        Args:
            bdd_dir: Directory containing .feature files

        Returns:
            Dictionary mapping feature names to BDDFeature objects
        """
        features = {}

        if not bdd_dir.exists():
            return features

        for feature_file in bdd_dir.rglob("*.feature"):
            feature = AlignmentParser._parse_bdd_file(feature_file)
            if feature:
                features[feature.feature_name] = feature

        return features

    @staticmethod
    def _parse_bdd_file(feature_file: Path) -> BDDFeature:
        """Parse a single BDD feature file."""
        content = feature_file.read_text()

        # Extract feature name
        feature_match = re.search(r'^Feature:\s*(.+)$', content, re.MULTILINE)
        if not feature_match:
            return None
        feature_name = feature_match.group(1).strip()

        # Extract scenarios
        scenarios = AlignmentParser._extract_scenarios(content)

        # Extract UC reference
        uc_ref = AlignmentParser._extract_uc_reference(content, feature_file.name)

        return BDDFeature(
            feature_name=feature_name,
            file_path=feature_file,
            scenarios=scenarios,
            uc_reference=uc_ref
        )

    @staticmethod
    def _extract_scenarios(content: str) -> List[str]:
        """
        Extract scenario names from BDD feature file.

        Matches:
        - Scenario: <name>
        - Scenario Outline: <name>
        """
        scenarios = []

        for match in re.finditer(
            r'^\s*(?:Scenario|Scenario Outline):\s*(.+)$',
            content,
            re.MULTILINE
        ):
            scenario_name = match.group(1).strip()
            scenarios.append(scenario_name)

        return scenarios

    @staticmethod
    def _extract_uc_reference(content: str, filename: str) -> str:
        """
        Extract UC reference from BDD feature file.

        Looks in:
        1. Feature description comments
        2. Filename (e.g., uc-001-example.feature)
        """
        # Pattern 1: Comment with UC-XXX
        match = re.search(r'#.*?(UC-\d+)', content)
        if match:
            return match.group(1)

        # Pattern 2: Filename
        match = re.search(r'(uc-\d+)', filename, re.IGNORECASE)
        if match:
            return match.group(1).upper().replace('UC-', 'UC-')

        return ""


class AlignmentValidator:
    """Validates alignment between use cases and BDD features."""

    def validate(
        self,
        use_cases: Dict[str, UseCase],
        bdd_features: Dict[str, BDDFeature]
    ) -> List[AlignmentIssue]:
        """
        Validate spec-code alignment.

        Returns list of issues found (empty list = perfect alignment).
        """
        issues = []

        # Check 1: Use cases without BDD files
        issues.extend(self._check_missing_bdd_files(use_cases, bdd_features))

        # Check 2: BDD files without UC references
        issues.extend(self._check_orphaned_features(use_cases, bdd_features))

        # Check 3: Scenario count vs criteria count mismatch
        issues.extend(self._check_count_mismatch(use_cases, bdd_features))

        # Check 4: Referenced BDD file doesn't exist
        issues.extend(self._check_broken_references(use_cases, bdd_features))

        return issues

    def _check_missing_bdd_files(
        self,
        use_cases: Dict[str, UseCase],
        bdd_features: Dict[str, BDDFeature]
    ) -> List[AlignmentIssue]:
        """Check for use cases without corresponding BDD files."""
        issues = []

        # Build set of UC IDs that have BDD files
        ucs_with_bdd = set()
        for feature in bdd_features.values():
            if feature.uc_reference:
                ucs_with_bdd.add(feature.uc_reference)

        for uc_id, uc in use_cases.items():
            if uc_id not in ucs_with_bdd:
                issues.append(AlignmentIssue(
                    issue_type="missing_bdd",
                    uc_id=uc_id,
                    feature_name="",
                    message=f"{uc_id} has no corresponding BDD feature file",
                    severity="error"
                ))

        return issues

    def _check_orphaned_features(
        self,
        use_cases: Dict[str, UseCase],
        bdd_features: Dict[str, BDDFeature]
    ) -> List[AlignmentIssue]:
        """Check for BDD features without UC references."""
        issues = []

        for feature_name, feature in bdd_features.items():
            if not feature.uc_reference:
                issues.append(AlignmentIssue(
                    issue_type="orphaned_feature",
                    uc_id="",
                    feature_name=feature_name,
                    message=f"BDD feature '{feature_name}' has no UC reference",
                    severity="warning"
                ))
            elif feature.uc_reference not in use_cases:
                issues.append(AlignmentIssue(
                    issue_type="broken_uc_ref",
                    uc_id=feature.uc_reference,
                    feature_name=feature_name,
                    message=f"BDD feature '{feature_name}' references non-existent {feature.uc_reference}",
                    severity="error"
                ))

        return issues

    def _check_count_mismatch(
        self,
        use_cases: Dict[str, UseCase],
        bdd_features: Dict[str, BDDFeature]
    ) -> List[AlignmentIssue]:
        """Check for scenario count vs acceptance criteria count mismatches."""
        issues = []

        # Map UC IDs to their BDD features
        uc_to_feature = {}
        for feature in bdd_features.values():
            if feature.uc_reference:
                uc_to_feature[feature.uc_reference] = feature

        for uc_id, uc in use_cases.items():
            if uc_id not in uc_to_feature:
                continue  # Already reported as missing_bdd

            feature = uc_to_feature[uc_id]
            criteria_count = len(uc.acceptance_criteria)
            scenario_count = len(feature.scenarios)

            if criteria_count != scenario_count:
                issues.append(AlignmentIssue(
                    issue_type="count_mismatch",
                    uc_id=uc_id,
                    feature_name=feature.feature_name,
                    message=(
                        f"{uc_id}: {criteria_count} acceptance criteria "
                        f"but {scenario_count} BDD scenarios in '{feature.feature_name}'"
                    ),
                    severity="warning"
                ))

        return issues

    def _check_broken_references(
        self,
        use_cases: Dict[str, UseCase],
        bdd_features: Dict[str, BDDFeature]
    ) -> List[AlignmentIssue]:
        """Check for use cases referencing non-existent BDD files."""
        issues = []

        # Build set of existing BDD file paths (normalized)
        existing_bdd_files = {
            str(f.file_path.name).lower() for f in bdd_features.values()
        }

        for uc_id, uc in use_cases.items():
            if not uc.bdd_file_referenced:
                continue

            # Extract just the filename from reference
            ref_filename = Path(uc.bdd_file_referenced).name.lower()

            if ref_filename not in existing_bdd_files:
                issues.append(AlignmentIssue(
                    issue_type="broken_bdd_ref",
                    uc_id=uc_id,
                    feature_name="",
                    message=f"{uc_id} references BDD file '{uc.bdd_file_referenced}' which doesn't exist",
                    severity="error"
                ))

        return issues
