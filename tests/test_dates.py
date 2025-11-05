"""Tests for date calculation utilities."""

import pytest
from datetime import datetime, timedelta
from github_artist.utils.dates import (
    get_next_sunday,
    calculate_optimal_start_date,
    matrix_to_dates,
    get_date_range_info,
    format_date_for_git
)


def test_get_next_sunday_from_monday():
    """Test getting next Sunday from a Monday."""
    # Create a Monday
    monday = datetime(2024, 1, 1)  # 2024-01-01 is a Monday
    sunday = get_next_sunday(monday)
    assert sunday.weekday() == 6  # Sunday
    assert sunday > monday
    assert (sunday - monday).days == 6


def test_get_next_sunday_from_sunday():
    """Test getting next Sunday when starting from Sunday."""
    # Create a Sunday
    sunday = datetime(2024, 1, 7)  # 2024-01-07 is a Sunday
    next_sunday = get_next_sunday(sunday)
    assert next_sunday.weekday() == 6  # Sunday
    assert next_sunday > sunday
    assert (next_sunday - sunday).days == 7


def test_get_next_sunday_from_saturday():
    """Test getting next Sunday from Saturday."""
    saturday = datetime(2024, 1, 6)  # 2024-01-06 is a Saturday
    sunday = get_next_sunday(saturday)
    assert sunday.weekday() == 6
    assert (sunday - saturday).days == 1


def test_calculate_optimal_start_date():
    """Test calculating optimal start date."""
    start_date = calculate_optimal_start_date()
    # Should be a Sunday
    assert start_date.weekday() == 6
    # Should be in the future
    assert start_date > datetime.now()


def test_calculate_optimal_start_date_with_target():
    """Test calculating optimal start date with specific target."""
    target = datetime(2024, 1, 1)  # Monday
    start_date = calculate_optimal_start_date(target, weeks_in_advance=0)
    assert start_date.weekday() == 6
    assert start_date > target


def test_matrix_to_dates_simple():
    """Test converting a simple matrix to dates."""
    matrix = [
        [1, 0],
        [0, 1],
        [1, 0],
        [0, 1],
        [1, 0],
        [0, 1],
        [1, 0],
    ]
    start_date = datetime(2024, 1, 7)  # Sunday
    dates = matrix_to_dates(matrix, start_date)
    
    # Should have 7 dates (one per row in first column, one per row in second column where 1)
    assert len(dates) == 7
    # First date should be the start date
    assert dates[0] == start_date


def test_matrix_to_dates_empty():
    """Test converting an empty matrix."""
    matrix = [[], [], [], [], [], [], []]
    start_date = datetime(2024, 1, 7)
    dates = matrix_to_dates(matrix, start_date)
    assert len(dates) == 0


def test_matrix_to_dates_all_zeros():
    """Test matrix with all zeros."""
    matrix = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    start_date = datetime(2024, 1, 7)
    dates = matrix_to_dates(matrix, start_date)
    assert len(dates) == 0


def test_matrix_to_dates_all_ones():
    """Test matrix with all ones."""
    matrix = [
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
    ]
    start_date = datetime(2024, 1, 7)
    dates = matrix_to_dates(matrix, start_date)
    assert len(dates) == 14  # 2 columns * 7 rows


def test_get_date_range_info_empty():
    """Test date range info with empty list."""
    info = get_date_range_info([])
    assert info["start_date"] is None
    assert info["end_date"] is None
    assert info["total_days"] == 0
    assert info["num_dates"] == 0


def test_get_date_range_info_single_date():
    """Test date range info with single date."""
    date = datetime(2024, 1, 1)
    info = get_date_range_info([date])
    assert info["start_date"] == date
    assert info["end_date"] == date
    assert info["total_days"] == 1
    assert info["num_dates"] == 1


def test_get_date_range_info_multiple_dates():
    """Test date range info with multiple dates."""
    dates = [
        datetime(2024, 1, 1),
        datetime(2024, 1, 5),
        datetime(2024, 1, 10),
    ]
    info = get_date_range_info(dates)
    assert info["start_date"] == dates[0]
    assert info["end_date"] == dates[2]
    assert info["total_days"] == 10
    assert info["num_dates"] == 3


def test_format_date_for_git():
    """Test formatting date for git."""
    date = datetime(2024, 1, 1, 12, 30, 45)
    formatted = format_date_for_git(date)
    assert "2024-01-01" in formatted
    assert "12:30:45" in formatted
