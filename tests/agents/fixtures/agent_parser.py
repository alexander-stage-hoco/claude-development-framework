"""Agent parser utilities for testing.

Provides utilities to parse and validate agent markdown files.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import re
import yaml


class AgentParser:
    """Parse and analyze agent markdown files."""

    def __init__(self, agent_path: Path):
        """Initialize parser with agent file path.

        Args:
            agent_path: Path to agent markdown file
        """
        self.path = agent_path
        self.name = agent_path.stem
        self._content = self._load_content()
        self._metadata, self._body = self._split_front_matter()
        self._sections = self._parse_sections()

    def _load_content(self) -> str:
        """Load agent file content."""
        with open(self.path, 'r', encoding='utf-8') as f:
            return f.read()

    def _split_front_matter(self) -> tuple[Dict[str, Any], str]:
        """Split YAML front matter from markdown body.

        Returns:
            Tuple of (metadata dict, body string)
        """
        parts = self._content.split('---', 2)

        if len(parts) < 3:
            return {}, self._content

        try:
            metadata = yaml.safe_load(parts[1])
        except yaml.YAMLError:
            metadata = {}

        return metadata or {}, parts[2].strip()

    def _parse_sections(self) -> Dict[str, str]:
        """Parse markdown sections from body.

        Returns:
            Dict mapping section titles to content
        """
        sections = {}
        current_section = None
        current_content = []

        for line in self._body.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    # ========================================================================
    # Metadata Access
    # ========================================================================

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get agent metadata from YAML front matter."""
        return self._metadata

    @property
    def has_frontmatter(self) -> bool:
        """Check if agent has YAML front matter."""
        return bool(self._metadata)

    def get_metadata_field(self, field: str) -> Optional[Any]:
        """Get specific metadata field value."""
        return self._metadata.get(field)

    # ========================================================================
    # Content Access
    # ========================================================================

    @property
    def body(self) -> str:
        """Get markdown body (without front matter)."""
        return self._body

    @property
    def sections(self) -> Dict[str, str]:
        """Get all parsed sections."""
        return self._sections

    def get_section(self, title: str) -> Optional[str]:
        """Get specific section content by title."""
        return self._sections.get(title)

    def has_section(self, title: str) -> bool:
        """Check if section exists."""
        return title in self._sections

    # ========================================================================
    # Code Block Extraction
    # ========================================================================

    def extract_code_blocks(self, language: Optional[str] = None) -> List[str]:
        """Extract code blocks from agent content.

        Args:
            language: Optional language filter (e.g., 'python', 'bash')

        Returns:
            List of code block contents
        """
        blocks = []
        in_block = False
        block_lang = None
        current_block = []

        for line in self._body.split('\n'):
            stripped = line.strip()

            if stripped.startswith('```'):
                if in_block:
                    # End of code block
                    if language is None or block_lang == language:
                        blocks.append('\n'.join(current_block))
                    current_block = []
                    in_block = False
                    block_lang = None
                else:
                    # Start of code block
                    in_block = True
                    block_lang = stripped[3:].strip() or None
            elif in_block:
                current_block.append(line)

        return blocks

    # ========================================================================
    # Checklist Extraction
    # ========================================================================

    def extract_checkboxes(self) -> List[str]:
        """Extract checkbox items from content.

        Returns:
            List of checkbox items (without checkbox markers)
        """
        checkboxes = []
        checkbox_pattern = r'^\s*-\s*\[\s*[xX ]?\s*\]\s*(.+)$'

        for line in self._body.split('\n'):
            match = re.match(checkbox_pattern, line)
            if match:
                checkboxes.append(match.group(1).strip())

        return checkboxes

    def get_section_checkboxes(self, section_title: str) -> List[str]:
        """Extract checkboxes from specific section.

        Args:
            section_title: Section title to search in

        Returns:
            List of checkbox items in that section
        """
        section_content = self.get_section(section_title)
        if not section_content:
            return []

        checkboxes = []
        checkbox_pattern = r'^\s*-\s*\[\s*[xX ]?\s*\]\s*(.+)$'

        for line in section_content.split('\n'):
            match = re.match(checkbox_pattern, line)
            if match:
                checkboxes.append(match.group(1).strip())

        return checkboxes

    # ========================================================================
    # Anti-Pattern Extraction
    # ========================================================================

    def extract_antipatterns(self) -> List[str]:
        """Extract anti-patterns from content.

        Returns:
            List of anti-pattern descriptions (without ❌ markers)
        """
        antipatterns = []
        antipattern_pattern = r'^\s*[❌✗]\s*(.+)$'

        for line in self._body.split('\n'):
            match = re.match(antipattern_pattern, line)
            if match:
                antipatterns.append(match.group(1).strip())

        return antipatterns

    # ========================================================================
    # Process Step Extraction
    # ========================================================================

    def extract_process_steps(self) -> List[str]:
        """Extract numbered process steps from Process section.

        Returns:
            List of process step descriptions
        """
        process_section = self.get_section("Process")
        if not process_section:
            return []

        steps = []
        step_pattern = r'^\s*(\d+)\.\s*\*?\*?(.+?)\*?\*?\s*-\s*(.+)$'
        simple_pattern = r'^\s*(\d+)\.\s*(.+)$'

        for line in process_section.split('\n'):
            # Try detailed pattern first
            match = re.match(step_pattern, line)
            if match:
                steps.append(f"{match.group(2)}: {match.group(3)}")
                continue

            # Try simple pattern
            match = re.match(simple_pattern, line)
            if match:
                steps.append(match.group(2).strip())

        return steps

    # ========================================================================
    # Validation Helpers
    # ========================================================================

    def validate_required_metadata(self, required_fields: List[str]) -> Dict[str, bool]:
        """Validate that required metadata fields are present.

        Args:
            required_fields: List of required field names

        Returns:
            Dict mapping field names to presence (True/False)
        """
        return {field: field in self._metadata for field in required_fields}

    def validate_required_sections(self, required_sections: List[str]) -> Dict[str, bool]:
        """Validate that required sections are present.

        Args:
            required_sections: List of required section titles

        Returns:
            Dict mapping section titles to presence (True/False)
        """
        return {section: self.has_section(section) for section in required_sections}

    # ========================================================================
    # Statistics
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about agent content.

        Returns:
            Dictionary with statistics
        """
        return {
            "name": self.name,
            "has_frontmatter": self.has_frontmatter,
            "metadata_fields": len(self._metadata),
            "sections": len(self._sections),
            "code_blocks": len(self.extract_code_blocks()),
            "checkboxes": len(self.extract_checkboxes()),
            "antipatterns": len(self.extract_antipatterns()),
            "process_steps": len(self.extract_process_steps()),
            "lines": len(self._content.split('\n')),
            "characters": len(self._content),
        }
