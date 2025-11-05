"""Tests for configuration management."""

import pytest
import json
from pathlib import Path
from datetime import datetime
from github_artist.core.config import ArtistConfig


def test_artist_config_minimal():
    """Test creating minimal configuration."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo"
    )
    assert config.username == "testuser"
    assert config.repo_name == "test-repo"
    assert config.protocol == "https"


def test_artist_config_full():
    """Test creating configuration with all options."""
    start_date = datetime(2024, 1, 7)
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo",
        protocol="ssh",
        text="HELLO",
        letter_spacing=2,
        commits_per_day=3,
        start_date=start_date,
        auto_calculate_start=False,
    )
    assert config.text == "HELLO"
    assert config.letter_spacing == 2
    assert config.commits_per_day == 3
    assert config.start_date == start_date


def test_artist_config_validation_no_username():
    """Test that username is required."""
    with pytest.raises(ValueError, match="Username is required"):
        ArtistConfig(username="", repo_name="test")


def test_artist_config_validation_no_repo():
    """Test that repo name is required."""
    with pytest.raises(ValueError, match="Repository name is required"):
        ArtistConfig(username="test", repo_name="")


def test_artist_config_validation_invalid_protocol():
    """Test that protocol must be valid."""
    with pytest.raises(ValueError, match="Protocol must be"):
        ArtistConfig(
            username="test",
            repo_name="test",
            protocol="invalid"
        )


def test_artist_config_validation_negative_commits():
    """Test that commits per day must be positive."""
    with pytest.raises(ValueError, match="at least 1"):
        ArtistConfig(
            username="test",
            repo_name="test",
            commits_per_day=0
        )


def test_artist_config_to_dict():
    """Test converting configuration to dictionary."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo",
        text="HELLO"
    )
    data = config.to_dict()
    assert data["username"] == "testuser"
    assert data["repo_name"] == "test-repo"
    assert data["text"] == "HELLO"


def test_artist_config_from_dict():
    """Test creating configuration from dictionary."""
    data = {
        "username": "testuser",
        "repo_name": "test-repo",
        "text": "HELLO",
        "letter_spacing": 2,
    }
    config = ArtistConfig.from_dict(data)
    assert config.username == "testuser"
    assert config.repo_name == "test-repo"
    assert config.text == "HELLO"
    assert config.letter_spacing == 2


def test_artist_config_validate():
    """Test configuration validation."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo",
        text="HELLO"
    )
    errors = config.validate()
    assert len(errors) == 0


def test_artist_config_validate_no_text():
    """Test validation fails without text in non-preview mode."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo",
        text="",
        preview_only=False
    )
    errors = config.validate()
    assert len(errors) > 0


def test_artist_config_validate_non_sunday():
    """Test validation warns about non-Sunday start date."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo",
        text="HELLO",
        start_date=datetime(2024, 1, 1)  # Monday
    )
    errors = config.validate()
    assert any("Sunday" in error for error in errors)


def test_artist_config_get_repo_path():
    """Test getting repository path."""
    config = ArtistConfig(
        username="testuser",
        repo_name="test-repo"
    )
    path = config.get_repo_path()
    assert "test-repo" in str(path)
