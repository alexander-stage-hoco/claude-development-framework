"""Template parser utilities for testing.

Provides utilities to parse and validate template markdown files.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import re
import yaml


def get_all_template_paths() -> List[Path]:
    """Get paths to all template markdown files.

    Returns:
        List of paths to template files (sorted)
    """
    templates_dir = Path(__file__).parent.parent.parent.parent / ".claude" / "templates"

    # Get all .md files including those in subdirectories
    template_paths = []
    for pattern in ["*.md", "*/*.md"]:
        template_paths.extend(templates_dir.glob(pattern))

    return sorted(template_paths)


class TemplateParser:
    """Parse and analyze template markdown files."""

    def __init__(self, template_path: Path):
        """Initialize parser with template file path.

        Args:
            template_path: Path to template markdown file
        """
        self.path = template_path
        self.name = template_path.stem
        self.relative_path = template_path.relative_to(
            template_path.parent.parent
        )  # Relative to .claude/
        self._content = self._load_content()
        self._metadata, self._body = self._split_front_matter()
        self._sections = self._parse_sections()

    def _load_content(self) -> str:
        """Load template file content."""
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def _split_front_matter(self) -> tuple[Dict[str, Any], str]:
        """Split YAML front matter from markdown body.

        Returns:
            Tuple of (metadata dict, body string)
        """
        parts = self._content.split("---", 2)

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

        for line in self._body.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    # ========================================================================
    # Metadata Access
    # ========================================================================

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get template metadata from YAML front matter."""
        return self._metadata

    @property
    def has_frontmatter(self) -> bool:
        """Check if template has YAML front matter."""
        return bool(self._metadata)

    def get_metadata_field(self, field: str) -> Optional[Any]:
        """Get specific metadata field value."""
        return self._metadata.get(field)

    # ========================================================================
    # Content Access
    # ========================================================================

    @property
    def content(self) -> str:
        """Get full file content (with front matter)."""
        return self._content

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
    # Placeholder Extraction
    # ========================================================================

    def extract_placeholders(self) -> List[str]:
        """Extract placeholders from template content.

        Placeholders are in format: [PLACEHOLDER], [PROJECT_NAME], etc.

        Returns:
            List of placeholder names (without brackets)
        """
        placeholder_pattern = r"\[([A-Z_][A-Z0-9_]*)\]"
        matches = re.findall(placeholder_pattern, self._body)
        return sorted(set(matches))

    def extract_placeholder_locations(self) -> Dict[str, List[int]]:
        """Get line numbers for each placeholder.

        Returns:
            Dict mapping placeholder names to list of line numbers
        """
        placeholder_pattern = r"\[([A-Z_][A-Z0-9_]*)\]"
        locations = {}

        for line_num, line in enumerate(self._body.split("\n"), 1):
            matches = re.findall(placeholder_pattern, line)
            for match in matches:
                if match not in locations:
                    locations[match] = []
                locations[match].append(line_num)

        return locations

    # ========================================================================
    # Code Block Extraction
    # ========================================================================

    def extract_code_blocks(self, language: Optional[str] = None) -> List[str]:
        """Extract code blocks from template content.

        Args:
            language: Optional language filter (e.g., 'python', 'bash')

        Returns:
            List of code block contents
        """
        blocks = []
        in_block = False
        block_lang = None
        current_block = []

        for line in self._body.split("\n"):
            stripped = line.strip()

            if stripped.startswith("```"):
                if in_block:
                    # End of code block
                    if language is None or block_lang == language:
                        blocks.append("\n".join(current_block))
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

    def get_code_block_languages(self) -> Set[str]:
        """Get set of languages used in code blocks.

        Returns:
            Set of language identifiers
        """
        languages = set()
        in_block = False

        for line in self._body.split("\n"):
            stripped = line.strip()

            if stripped.startswith("```"):
                if in_block:
                    in_block = False
                else:
                    in_block = True
                    lang = stripped[3:].strip()
                    if lang:
                        languages.add(lang)

        return languages

    # ========================================================================
    # Link Extraction
    # ========================================================================

    def extract_links(self) -> List[tuple[str, str]]:
        """Extract markdown links from content.

        Returns:
            List of (link_text, link_url) tuples
        """
        link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
        matches = re.findall(link_pattern, self._body)
        return matches

    def extract_file_references(self) -> List[str]:
        """Extract file path references from links.

        Returns:
            List of file paths referenced in template
        """
        links = self.extract_links()
        file_refs = []

        for text, url in links:
            # Skip external URLs
            if url.startswith(("http://", "https://", "#")):
                continue
            file_refs.append(url)

        return file_refs

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

    def has_h1_title(self) -> bool:
        """Check if template has exactly one H1 title."""
        h1_pattern = r"^# .+"
        matches = re.findall(h1_pattern, self._body, re.MULTILINE)
        return len(matches) == 1

    def get_h1_title(self) -> Optional[str]:
        """Get the H1 title text.

        Returns:
            Title text without the # marker, or None if no H1 found
        """
        h1_pattern = r"^# (.+)"
        match = re.search(h1_pattern, self._body, re.MULTILINE)
        return match.group(1).strip() if match else None

    # ========================================================================
    # Statistics
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about template content.

        Returns:
            Dictionary with statistics
        """
        return {
            "name": self.name,
            "relative_path": str(self.relative_path),
            "has_frontmatter": self.has_frontmatter,
            "metadata_fields": len(self._metadata),
            "sections": len(self._sections),
            "placeholders": len(self.extract_placeholders()),
            "code_blocks": len(self.extract_code_blocks()),
            "code_languages": len(self.get_code_block_languages()),
            "links": len(self.extract_links()),
            "file_references": len(self.extract_file_references()),
            "lines": len(self._content.split("\n")),
            "characters": len(self._content),
        }
