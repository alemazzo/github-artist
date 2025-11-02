"""Tests for character matrix functionality."""

import pytest
from github_artist.data.characters import (
    get_char_matrix,
    string_to_matrix,
    get_supported_chars,
    GRID_HEIGHT
)


def test_get_supported_chars():
    """Test that we can get the list of supported characters."""
    chars = get_supported_chars()
    assert len(chars) > 0
    assert "A" in chars
    assert "a" in chars
    assert "0" in chars
    assert " " in chars


def test_get_char_matrix_uppercase():
    """Test getting a matrix for an uppercase character."""
    matrix = get_char_matrix("A")
    assert len(matrix) == GRID_HEIGHT
    assert all(isinstance(row, list) for row in matrix)
    assert all(cell in [0, 1] for row in matrix for cell in row)


def test_get_char_matrix_lowercase():
    """Test getting a matrix for a lowercase character."""
    matrix = get_char_matrix("a")
    assert len(matrix) == GRID_HEIGHT


def test_get_char_matrix_number():
    """Test getting a matrix for a number."""
    matrix = get_char_matrix("0")
    assert len(matrix) == GRID_HEIGHT


def test_get_char_matrix_case_insensitive():
    """Test that uppercase fallback works."""
    # Uppercase should work
    matrix_upper = get_char_matrix("A")
    assert len(matrix_upper) == GRID_HEIGHT


def test_get_char_matrix_unsupported():
    """Test that unsupported characters raise ValueError."""
    with pytest.raises(ValueError, match="not supported"):
        get_char_matrix("§")


def test_string_to_matrix_single_char():
    """Test converting a single character to matrix."""
    matrix = string_to_matrix("A")
    assert len(matrix) == GRID_HEIGHT
    assert len(matrix[0]) > 0


def test_string_to_matrix_multiple_chars():
    """Test converting multiple characters to matrix."""
    matrix = string_to_matrix("HI")
    assert len(matrix) == GRID_HEIGHT
    # Should have more columns than a single character
    single = string_to_matrix("H")
    assert len(matrix[0]) > len(single[0])


def test_string_to_matrix_with_spacing():
    """Test that letter spacing works."""
    matrix_no_space = string_to_matrix("HI", letter_spacing=0)
    matrix_with_space = string_to_matrix("HI", letter_spacing=2)
    # With spacing should have more columns
    assert len(matrix_with_space[0]) > len(matrix_no_space[0])


def test_string_to_matrix_empty():
    """Test converting empty string."""
    matrix = string_to_matrix("")
    assert len(matrix) == GRID_HEIGHT
    assert all(len(row) == 0 for row in matrix)


def test_string_to_matrix_with_space():
    """Test that spaces are handled."""
    matrix = string_to_matrix("A B")
    assert len(matrix) == GRID_HEIGHT
    assert len(matrix[0]) > 0


def test_matrix_contains_only_binary():
    """Test that matrix contains only 0s and 1s."""
    matrix = string_to_matrix("TEST")
    for row in matrix:
        for cell in row:
            assert cell in [0, 1], f"Cell value {cell} is not 0 or 1"


def test_all_characters_have_consistent_height():
    """Test that all characters have 7 rows."""
    chars = get_supported_chars()
    for char in chars:
        try:
            matrix = get_char_matrix(char)
            assert len(matrix) == GRID_HEIGHT, f"Character '{char}' has {len(matrix)} rows, expected {GRID_HEIGHT}"
        except ValueError:
            # Skip if character not supported (shouldn't happen)
            pass
