"""Visualization and preview utilities for GitHub contribution art."""

from datetime import datetime
from typing import List, Optional
from github_artist.data.characters import print_matrix, string_to_matrix
from github_artist.utils.dates import get_date_range_info


def preview_text(text: str, letter_spacing: int = 1) -> None:
    """
    Preview how text will appear in the GitHub contribution graph.
    
    Args:
        text: Text to preview
        letter_spacing: Space between letters (default: 1)
    """
    print(f"\nPreview of: '{text}'")
    print("=" * 60)
    
    try:
        matrix = string_to_matrix(text, letter_spacing)
        
        # Print matrix with GitHub-style characters
        print_matrix(matrix, filled_char="█", empty_char="·")
        
        # Print dimensions
        num_rows = len(matrix)
        num_cols = len(matrix[0]) if matrix else 0
        num_weeks = num_cols // 7 + (1 if num_cols % 7 else 0)
        
        print("=" * 60)
        print(f"Dimensions: {num_cols} columns x {num_rows} rows")
        print(f"Approximate weeks: {num_weeks}")
        print(f"Total commits needed: {sum(sum(row) for row in matrix)}")
        print()
        
    except ValueError as e:
        print(f"Error: {e}")


def preview_dates(
    text: str,
    start_date: datetime,
    letter_spacing: int = 1,
    commits_per_day: int = 1
) -> None:
    """
    Preview the date range and commit statistics.
    
    Args:
        text: Text to create
        start_date: Starting date
        letter_spacing: Space between letters (default: 1)
        commits_per_day: Number of commits per day (default: 1)
    """
    from github_artist.utils.dates import matrix_to_dates
    
    print(f"\nDate range preview for: '{text}'")
    print("=" * 60)
    
    try:
        matrix = string_to_matrix(text, letter_spacing)
        dates = matrix_to_dates(matrix, start_date)
        
        if not dates:
            print("No dates to commit")
            return
        
        info = get_date_range_info(dates)
        
        print(f"Start date: {info['start_date'].strftime('%Y-%m-%d (%A)')}")
        print(f"End date:   {info['end_date'].strftime('%Y-%m-%d (%A)')}")
        print(f"Duration:   {info['total_days']} days (~{info['weeks']} weeks)")
        print(f"Commit days: {info['num_dates']}")
        print(f"Total commits: {info['num_dates'] * commits_per_day}")
        print(f"Commits per day: {commits_per_day}")
        print("=" * 60)
        print()
        
    except ValueError as e:
        print(f"Error: {e}")


def show_calendar_view(
    matrix: List[List[int]],
    start_date: datetime,
    show_dates: bool = False
) -> None:
    """
    Show a calendar-style view of the contribution pattern.
    
    Args:
        matrix: Character matrix
        start_date: Starting date
        show_dates: Whether to show dates (default: False)
    """
    from github_artist.utils.dates import matrix_to_dates
    
    print("\nCalendar view:")
    print("=" * 60)
    
    if not matrix or not matrix[0]:
        print("Empty matrix")
        return
    
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    # Print header
    if show_dates:
        print("    ", end="")
    else:
        print("   ", end="")
    
    num_cols = len(matrix[0])
    for i in range(0, num_cols, 7):
        week_num = i // 7 + 1
        print(f"W{week_num:2} ", end="")
    print()
    
    # Print days and data
    for row_idx, day in enumerate(days):
        print(f"{day} ", end="")
        for col_idx in range(num_cols):
            if matrix[row_idx][col_idx] == 1:
                print("█", end="")
            else:
                print("·", end="")
        print()
    
    print("=" * 60)
    print()


def create_contribution_summary(
    text: str,
    start_date: datetime,
    letter_spacing: int = 1,
    commits_per_day: int = 1
) -> dict:
    """
    Create a comprehensive summary of the GitHub art project.
    
    Args:
        text: Text to create
        start_date: Starting date
        letter_spacing: Space between letters
        commits_per_day: Commits per day
        
    Returns:
        Dictionary with summary information
    """
    from github_artist.utils.dates import matrix_to_dates
    
    matrix = string_to_matrix(text, letter_spacing)
    dates = matrix_to_dates(matrix, start_date)
    info = get_date_range_info(dates)
    
    return {
        "text": text,
        "start_date": start_date,
        "end_date": info["end_date"],
        "duration_days": info["total_days"],
        "commit_days": info["num_dates"],
        "total_commits": info["num_dates"] * commits_per_day,
        "commits_per_day": commits_per_day,
        "letter_spacing": letter_spacing,
        "matrix_size": {
            "rows": len(matrix),
            "cols": len(matrix[0]) if matrix else 0,
        },
    }


def print_full_preview(
    text: str,
    start_date: datetime,
    letter_spacing: int = 1,
    commits_per_day: int = 1,
    show_calendar: bool = True
) -> None:
    """
    Print a comprehensive preview of the GitHub art.
    
    Args:
        text: Text to create
        start_date: Starting date
        letter_spacing: Space between letters
        commits_per_day: Commits per day
        show_calendar: Whether to show calendar view
    """
    print("\n" + "=" * 60)
    print("GitHub Artist - Preview")
    print("=" * 60)
    
    # Show text preview
    preview_text(text, letter_spacing)
    
    # Show date information
    preview_dates(text, start_date, letter_spacing, commits_per_day)
    
    # Show calendar view
    if show_calendar:
        matrix = string_to_matrix(text, letter_spacing)
        show_calendar_view(matrix, start_date)
    
    print("=" * 60)
    print()
