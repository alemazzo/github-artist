"""Command-line interface for GitHub Artist."""

import argparse
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from github_artist.data.characters import get_supported_chars, string_to_matrix, print_matrix
from github_artist.core.config import ArtistConfig, create_example_config
from github_artist.core.git_ops import GitRepository, create_commits_for_dates
from github_artist.core.preview import print_full_preview
from github_artist.utils.dates import calculate_optimal_start_date, matrix_to_dates


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def print_banner():
    """Print the GitHub Artist banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗ ║
║             ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗║
║             ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝║
║             ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗║
║             ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝║
║              ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ║
║                                                           ║
║                    ARTIST v2.0.0                          ║
║           Create art in your GitHub contribution graph    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def cmd_create(args):
    """Handle the create command."""
    print_banner()
    
    # Build configuration
    config = ArtistConfig(
        username=args.username,
        repo_name=args.repo,
        protocol=args.protocol,
        text=args.text,
        letter_spacing=args.spacing,
        commits_per_day=args.commits,
        auto_calculate_start=args.start_date is None,
        weeks_in_advance=args.weeks_advance,
        preview_only=args.preview,
        auto_push=not args.no_push,
    )
    
    # Parse start date if provided
    if args.start_date:
        try:
            config.start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid date format: {args.start_date}. Use YYYY-MM-DD")
            return 1
    
    # Calculate start date if needed
    if config.auto_calculate_start:
        config.start_date = calculate_optimal_start_date(weeks_in_advance=config.weeks_in_advance)
        logger.info(f"Calculated optimal start date: {config.start_date.strftime('%Y-%m-%d (%A)')}")
    
    # Validate configuration
    errors = config.validate()
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        return 1
    
    # Generate matrix
    try:
        matrix = string_to_matrix(config.text, config.letter_spacing)
        dates = matrix_to_dates(matrix, config.start_date)
    except ValueError as e:
        logger.error(f"Error generating pattern: {e}")
        return 1
    
    # Show preview
    print_full_preview(
        config.text,
        config.start_date,
        config.letter_spacing,
        config.commits_per_day,
        show_calendar=True
    )
    
    # Stop here if preview only
    if config.preview_only:
        logger.info("Preview mode - no commits will be created")
        return 0
    
    # Confirm with user
    if not args.yes:
        response = input("\nProceed with creating commits? (y/N): ")
        if response.lower() != "y":
            logger.info("Cancelled by user")
            return 0
    
    # Setup repository
    repo_path = config.get_repo_path()
    repo = GitRepository(str(repo_path))
    
    if not repo.exists():
        logger.info(f"Cloning repository {config.username}/{config.repo_name}...")
        if not repo.clone(config.username, config.repo_name, config.protocol):
            logger.error("Failed to clone repository")
            return 1
    
    # Create commits
    logger.info(f"Creating commits for {len(dates)} days...")
    total_commits = len(dates) * config.commits_per_day
    
    successful, failed = create_commits_for_dates(
        repo,
        dates,
        config.commits_per_day,
        config.commit_message_template
    )
    
    logger.info(f"Created {successful}/{total_commits} commits ({failed} failed)")
    
    # Push to remote
    if config.auto_push:
        logger.info("Pushing to remote repository...")
        if repo.push(config.remote_name, config.branch_name):
            logger.info("✓ Successfully pushed to GitHub!")
        else:
            logger.error("Failed to push to GitHub")
            return 1
    else:
        logger.info("Skipping push (use without --no-push to push automatically)")
    
    logger.info("\n✓ GitHub art creation completed!")
    logger.info(f"Check your contribution graph at: https://github.com/{config.username}")
    
    return 0


def cmd_preview(args):
    """Handle the preview command."""
    print_banner()
    
    # Calculate start date
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid date format: {args.start_date}. Use YYYY-MM-DD")
            return 1
    else:
        start_date = calculate_optimal_start_date(weeks_in_advance=args.weeks_advance)
    
    print_full_preview(args.text, start_date, args.spacing, args.commits, show_calendar=True)
    return 0


def cmd_chars(args):
    """Handle the chars command to show supported characters."""
    print_banner()
    chars = get_supported_chars()
    
    print("Supported Characters:")
    print("=" * 60)
    print("\nUppercase Letters:")
    print("  " + " ".join([c for c in chars if c.isupper() and c.isalpha()]))
    
    print("\nLowercase Letters:")
    print("  " + " ".join([c for c in chars if c.islower() and c.isalpha()]))
    
    print("\nNumbers:")
    print("  " + " ".join([c for c in chars if c.isdigit()]))
    
    print("\nSpecial Characters:")
    special = [c for c in chars if not c.isalnum() and c != " "]
    print("  " + " ".join(special))
    
    print("\n" + "=" * 60)
    print(f"Total: {len(chars)} characters supported")
    print()
    
    if args.show_all:
        print("\nCharacter Previews:")
        print("=" * 60)
        for char in chars:
            if char == " ":
                continue
            print(f"\nCharacter: '{char}'")
            matrix = string_to_matrix(char)
            print_matrix(matrix, filled_char="█", empty_char="·")
    
    return 0


def cmd_config(args):
    """Handle the config command."""
    if args.example:
        output_path = Path(args.output) if args.output else Path("github-artist-config.json")
        create_example_config(output_path)
        return 0
    
    print("Config command requires --example flag")
    return 1


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Create art in your GitHub contribution graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create GitHub contribution art")
    create_parser.add_argument("username", help="GitHub username")
    create_parser.add_argument("repo", help="Repository name")
    create_parser.add_argument("text", help="Text to create in the contribution graph")
    create_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD, default: auto-calculate)")
    create_parser.add_argument("--spacing", type=int, default=1, help="Letter spacing (default: 1)")
    create_parser.add_argument("--commits", type=int, default=1, help="Commits per day (default: 1)")
    create_parser.add_argument("--weeks-advance", type=int, default=1, help="Weeks in advance for auto start date (default: 1)")
    create_parser.add_argument("--protocol", choices=["https", "ssh"], default="https", help="Clone protocol (default: https)")
    create_parser.add_argument("--preview", action="store_true", help="Preview only, don't create commits")
    create_parser.add_argument("--no-push", action="store_true", help="Don't push to remote")
    create_parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")
    create_parser.set_defaults(func=cmd_create)
    
    # Preview command
    preview_parser = subparsers.add_parser("preview", help="Preview how text will look")
    preview_parser.add_argument("text", help="Text to preview")
    preview_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD, default: auto-calculate)")
    preview_parser.add_argument("--spacing", type=int, default=1, help="Letter spacing (default: 1)")
    preview_parser.add_argument("--commits", type=int, default=1, help="Commits per day (default: 1)")
    preview_parser.add_argument("--weeks-advance", type=int, default=1, help="Weeks in advance (default: 1)")
    preview_parser.set_defaults(func=cmd_preview)
    
    # Chars command
    chars_parser = subparsers.add_parser("chars", help="Show supported characters")
    chars_parser.add_argument("--show-all", action="store_true", help="Show preview of all characters")
    chars_parser.set_defaults(func=cmd_chars)
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_parser.add_argument("--example", action="store_true", help="Create example configuration file")
    config_parser.add_argument("--output", help="Output file path (default: github-artist-config.json)")
    config_parser.set_defaults(func=cmd_config)
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        argv: Command line arguments (default: sys.argv[1:])
        
    Returns:
        Exit code
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
