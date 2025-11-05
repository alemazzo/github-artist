"""Git operations for creating commits with specific dates."""

import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class GitRepository:
    """Manages Git repository operations for creating GitHub art."""
    
    def __init__(self, repo_path: str):
        """
        Initialize a GitRepository.
        
        Args:
            repo_path: Path to the repository directory
        """
        self.repo_path = Path(repo_path)
        self.data_file = self.repo_path / "art_data.txt"
    
    def exists(self) -> bool:
        """Check if the repository exists."""
        return self.repo_path.exists() and (self.repo_path / ".git").exists()
    
    def clone(self, username: str, repo_name: str, protocol: str = "https") -> bool:
        """
        Clone a repository if it doesn't exist.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            protocol: Clone protocol ('https' or 'ssh')
            
        Returns:
            True if successful, False otherwise
        """
        if self.exists():
            logger.info(f"Repository already exists at {self.repo_path}")
            return True
        
        if protocol == "ssh":
            url = f"git@github.com:{username}/{repo_name}.git"
        else:
            url = f"https://github.com/{username}/{repo_name}.git"
        
        try:
            logger.info(f"Cloning repository from {url}")
            result = subprocess.run(
                ["git", "clone", url, str(self.repo_path)],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("Repository cloned successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e.stderr}")
            return False
    
    def init(self) -> bool:
        """
        Initialize a new Git repository.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.repo_path.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "init"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            logger.info(f"Initialized new repository at {self.repo_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize repository: {e.stderr}")
            return False
    
    def create_commit(
        self,
        date: datetime,
        message: Optional[str] = None,
        append_data: str = "x"
    ) -> bool:
        """
        Create a commit with a specific date.
        
        Args:
            date: The date for the commit
            message: Commit message (default: uses the date)
            append_data: Data to append to the file (default: "x")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.exists():
            logger.error("Repository does not exist")
            return False
        
        try:
            # Append data to file
            with open(self.data_file, "a") as f:
                f.write(append_data + "\n")
            
            # Stage changes
            subprocess.run(
                ["git", "add", "."],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            
            # Create commit with specific date
            commit_msg = message or date.strftime("%Y-%m-%d %H:%M:%S")
            date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
            
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date_str
            env["GIT_COMMITTER_DATE"] = date_str
            
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.repo_path,
                env=env,
                capture_output=True,
                check=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create commit: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating commit: {str(e)}")
            return False
    
    def push(self, remote: str = "origin", branch: str = "main") -> bool:
        """
        Push commits to remote repository.
        
        Args:
            remote: Remote name (default: "origin")
            branch: Branch name (default: "main")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.exists():
            logger.error("Repository does not exist")
            return False
        
        try:
            logger.info(f"Pushing to {remote}/{branch}...")
            result = subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("Pushed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to push: {e.stderr}")
            return False
    
    def get_status(self) -> str:
        """
        Get repository status.
        
        Returns:
            Git status output
        """
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def get_commit_count(self) -> int:
        """
        Get the number of commits in the repository.
        
        Returns:
            Number of commits
        """
        try:
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return int(result.stdout.strip())
        except subprocess.CalledProcessError:
            return 0


def create_commits_for_dates(
    repo: GitRepository,
    dates: List[datetime],
    commits_per_day: int = 1,
    message_template: Optional[str] = None
) -> tuple[int, int]:
    """
    Create commits for a list of dates.
    
    Args:
        repo: GitRepository instance
        dates: List of dates to create commits for
        commits_per_day: Number of commits per date (default: 1)
        message_template: Template for commit messages (default: None)
        
    Returns:
        Tuple of (successful_commits, failed_commits)
    """
    successful = 0
    failed = 0
    
    for date in dates:
        for i in range(commits_per_day):
            message = None
            if message_template:
                message = message_template.format(date=date, index=i)
            
            if repo.create_commit(date, message):
                successful += 1
            else:
                failed += 1
    
    return successful, failed
