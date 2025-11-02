"""Configuration management for GitHub Artist."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import json


@dataclass
class ArtistConfig:
    """Configuration for creating GitHub contribution art."""
    
    # Repository settings
    username: str
    repo_name: str
    protocol: str = "https"  # "https" or "ssh"
    
    # Art settings
    text: str = ""
    letter_spacing: int = 1
    commits_per_day: int = 1
    
    # Date settings
    start_date: Optional[datetime] = None
    auto_calculate_start: bool = True
    weeks_in_advance: int = 1
    
    # Git settings
    commit_message_template: Optional[str] = None
    remote_name: str = "origin"
    branch_name: str = "main"
    
    # Execution settings
    preview_only: bool = False
    auto_push: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.username:
            raise ValueError("Username is required")
        if not self.repo_name:
            raise ValueError("Repository name is required")
        if self.protocol not in ["https", "ssh"]:
            raise ValueError("Protocol must be 'https' or 'ssh'")
        if self.commits_per_day < 1:
            raise ValueError("Commits per day must be at least 1")
        if self.letter_spacing < 0:
            raise ValueError("Letter spacing must be non-negative")
    
    @classmethod
    def from_dict(cls, data: dict) -> "ArtistConfig":
        """
        Create configuration from a dictionary.
        
        Args:
            data: Dictionary with configuration values
            
        Returns:
            ArtistConfig instance
        """
        # Handle datetime conversion
        if "start_date" in data and data["start_date"]:
            if isinstance(data["start_date"], str):
                data["start_date"] = datetime.fromisoformat(data["start_date"])
        
        return cls(**data)
    
    def to_dict(self) -> dict:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dictionary representation
        """
        data = {
            "username": self.username,
            "repo_name": self.repo_name,
            "protocol": self.protocol,
            "text": self.text,
            "letter_spacing": self.letter_spacing,
            "commits_per_day": self.commits_per_day,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "auto_calculate_start": self.auto_calculate_start,
            "weeks_in_advance": self.weeks_in_advance,
            "commit_message_template": self.commit_message_template,
            "remote_name": self.remote_name,
            "branch_name": self.branch_name,
            "preview_only": self.preview_only,
            "auto_push": self.auto_push,
        }
        return data
    
    @classmethod
    def from_file(cls, filepath: Path) -> "ArtistConfig":
        """
        Load configuration from a JSON file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            ArtistConfig instance
        """
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    def to_file(self, filepath: Path) -> None:
        """
        Save configuration to a JSON file.
        
        Args:
            filepath: Path to save configuration
        """
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def get_repo_path(self, base_dir: Path = None) -> Path:
        """
        Get the path where the repository should be cloned.
        
        Args:
            base_dir: Base directory (default: current directory)
            
        Returns:
            Path to repository
        """
        if base_dir is None:
            base_dir = Path.cwd()
        return base_dir / self.repo_name
    
    def validate(self) -> list[str]:
        """
        Validate the configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.text and not self.preview_only:
            errors.append("Text is required when not in preview-only mode")
        
        if self.start_date and self.start_date.weekday() != 6:
            errors.append(f"Start date should be a Sunday for proper alignment (currently {self.start_date.strftime('%A')})")
        
        return errors


def create_example_config(filepath: Path) -> None:
    """
    Create an example configuration file.
    
    Args:
        filepath: Path to save the example configuration
    """
    config = ArtistConfig(
        username="your-username",
        repo_name="github-art",
        protocol="https",
        text="HELLO",
        letter_spacing=1,
        commits_per_day=1,
        auto_calculate_start=True,
        weeks_in_advance=1,
        preview_only=False,
        auto_push=False,
    )
    config.to_file(filepath)
    print(f"Example configuration saved to: {filepath}")
