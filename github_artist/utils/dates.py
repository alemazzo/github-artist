"""Date calculation utilities for GitHub contribution graph alignment."""

from datetime import datetime, timedelta
from typing import List, Tuple


def get_next_sunday(from_date: datetime = None) -> datetime:
    """
    Calculate the next Sunday from a given date for optimal GitHub graph alignment.
    
    Args:
        from_date: Starting date (default: today)
        
    Returns:
        The next Sunday date
    """
    if from_date is None:
        from_date = datetime.now()
    
    # weekday() returns 0 for Monday, 6 for Sunday
    days_until_sunday = (6 - from_date.weekday()) % 7
    
    # If today is Sunday, get next Sunday
    if days_until_sunday == 0:
        days_until_sunday = 7
    
    return from_date + timedelta(days=days_until_sunday)


def calculate_optimal_start_date(
    target_date: datetime = None,
    weeks_in_advance: int = 1
) -> datetime:
    """
    Calculate an optimal start date for creating GitHub art.
    
    The start date is positioned to align with GitHub's contribution grid,
    which displays 7 rows (Sunday-Saturday).
    
    Args:
        target_date: Desired approximate start date (default: today)
        weeks_in_advance: Number of weeks in advance to start (default: 1)
        
    Returns:
        Optimal start date (always a Sunday)
    """
    if target_date is None:
        target_date = datetime.now()
    
    # Add weeks in advance
    target_date = target_date + timedelta(weeks=weeks_in_advance)
    
    # Find the next Sunday
    return get_next_sunday(target_date)


def matrix_to_dates(
    matrix: List[List[int]],
    start_date: datetime
) -> List[datetime]:
    """
    Convert a character matrix to a list of dates for commits.
    
    The matrix is processed column by column, with each column representing
    a week (7 days, Sunday to Saturday).
    
    Args:
        matrix: A 7-row matrix where 1 indicates a commit should be made
        start_date: The starting date (should be a Sunday for proper alignment)
        
    Returns:
        List of dates where commits should be made
    """
    dates = []
    current_date = start_date
    
    if not matrix or not matrix[0]:
        return dates
    
    num_cols = len(matrix[0])
    
    # Process column by column (each column is a week)
    for col in range(num_cols):
        for row in range(len(matrix)):
            if matrix[row][col] == 1:
                dates.append(current_date)
            current_date += timedelta(days=1)
    
    return dates


def get_date_range_info(dates: List[datetime]) -> dict:
    """
    Get information about a date range.
    
    Args:
        dates: List of dates
        
    Returns:
        Dictionary with date range information
    """
    if not dates:
        return {
            "start_date": None,
            "end_date": None,
            "total_days": 0,
            "num_dates": 0,
            "weeks": 0,
        }
    
    sorted_dates = sorted(dates)
    start = sorted_dates[0]
    end = sorted_dates[-1]
    total_days = (end - start).days + 1
    
    return {
        "start_date": start,
        "end_date": end,
        "total_days": total_days,
        "num_dates": len(dates),
        "weeks": total_days // 7,
    }


def format_date_for_git(date: datetime) -> str:
    """
    Format a date for use in git commit commands.
    
    Args:
        date: The date to format
        
    Returns:
        Date string in ISO 8601 format
    """
    return date.strftime("%Y-%m-%dT%H:%M:%S")
