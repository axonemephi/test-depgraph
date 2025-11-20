"""Configuration class for DepCycle settings."""

from pathlib import Path
from typing import List, Optional

# Default exclusion patterns that are automatically applied
DEFAULT_EXCLUDE_PATTERNS = [
    'venv',
    '.venv',
    'env',
    '.env',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '.git',
    '.hg',
    '.svn',
    'node_modules',
    '.pytest_cache',
    '.mypy_cache',
    '.tox',
    'dist',
    'build',
    '*.egg-info',
    'migrations',  # Django/ORM migration directories
]


class Config:
    """
    Holds all configuration settings for a DepCycle run.
    
    This class encapsulates all the options that control how DepCycle
    analyzes and visualizes a Python project.
    
    Attributes:
        project_path (Path): Path to the project root directory.
        output_file (Path): Path where the output visualization should be saved.
        output_format (str): Format for the output ('png', 'svg', 'html').
        exclude_patterns (List[str]): Glob patterns for files to exclude.
        show_third_party (bool): Whether to include third-party modules.
        show_stdlib (bool): Whether to include standard library modules.
        include_all (bool): Whether to include files normally excluded by default patterns.
    """
    
    def __init__(
        self, 
        project_path: Path, 
        output_file: Path, 
        output_format: str = "png", 
        exclude_patterns: Optional[List[str]] = None, 
        show_third_party: bool = True,
        show_stdlib: bool = True,
        include_all: bool = False
    ):
        self.project_path = project_path
        self.output_file = output_file
        self.output_format = output_format
        self.show_third_party = show_third_party
        self.show_stdlib = show_stdlib
        self.include_all = include_all
        
        # Merge default exclusions with user-specified ones
        user_patterns = exclude_patterns if exclude_patterns is not None else []
        if include_all:
            # If include_all is True, only use user-specified patterns
            self.exclude_patterns = user_patterns
        else:
            # Merge defaults with user patterns, avoiding duplicates
            self.exclude_patterns = list(DEFAULT_EXCLUDE_PATTERNS)
            for pattern in user_patterns:
                if pattern not in self.exclude_patterns:
                    self.exclude_patterns.append(pattern)

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation of the Config object."""
        return (
            f"{self.__class__.__name__}("
            f"project_path={self.project_path!r}, "
            f"output_file={self.output_file!r}, "
            f"output_format={self.output_format!r}, "
            f"exclude_patterns={self.exclude_patterns!r}, "
            f"show_third_party={self.show_third_party!r}, "
            f"show_stdlib={self.show_stdlib!r}, "
            f"include_all={self.include_all!r}"
            ")"
        )

