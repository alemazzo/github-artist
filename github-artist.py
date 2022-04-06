#!/usr/bin/python3
import subprocess, sys, os
from datetime import date, timedelta, datetime
from letters import stringToMatrix

def add_random_letter_to_file(repo, file_name):
    command = f'cd {repo} && echo "a" >> {file_name}' 
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

def git_add_all_to_stage(repo):
    command = f'cd {repo} && git add .'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
    
def git_commit_with_specified_date(repo, date, commit_message = None):
    command = f'cd {repo} && git commit --date="{date}" -m "{date}"'
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)

def make_commit_with_specified_date(repo, date, commit_message = None):
    add_random_letter_to_file(repo, "test")
    git_add_all_to_stage(repo)
    git_commit_with_specified_date(repo, date, commit_message)

def git_push_to_remote_repo(repo):
    command = f"cd {repo} && git push"
    subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)
    
def clone_repo_if_not_exists_already(username, repo, protocol = "ssh"):
    if protocol == "ssh":
        command = f"git clone git@github.com:{username}/{repo}.git"
    elif protocol == "https":
        command = f"git clone https://github.com/{username}/{repo}.git"
        
    if not os.path.exists(repo):
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)




def execute(repo, date, numbers_of_commits_per_day = 1):
    commits = 0
    total_commits = len(dates) * numbers_of_commits_per_day
    print("Info:")
    print(f"Number of dates: {len(dates)}")
    print(f"Number of commits per day: {numbers_of_commits_per_day}")
    print(f"Number of commits: {total_commits}")
    print("-" * 50)
    for date in dates:
        for i in range(numbers_of_commits_per_day):
            start_time = datetime.now()
            make_commit_with_specified_date(repo, date)
            end_time = datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            eta = total_seconds * (total_commits - commits)
            formatted_eta = str(timedelta(seconds=int(eta)))
            commits += 1
            percentage = (commits / total_commits) * 100
            print(f"Status: Commits: {commits} -- {percentage:.2f}% -- ETA: {formatted_eta}", end="\r")
    print(f"Commits: {commits} -- 100%")
    
if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print("Usage: python3 github-history-writer.py <username/repo-name>")
        sys.exit(1)
        
    username, repo = sys.argv[1].split("/")
    message = sys.argv[2] if len(sys.argv) > 2 else None
    
    # parse date from third element of argv
    start_date = datetime.strptime(sys.argv[3], '%y/%m/%d')
    number_of_commits_per_day = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    
    dates = []
    actual_date = start_date
    message_matrix = stringToMatrix(message)
    for col in range(len(message_matrix[0])):
        for row in range(len(message_matrix)):
            if message_matrix[row][col] == 1:
                dates.append(actual_date)
            actual_date += timedelta(days = 1)

    
    # Start
    print("-" * 50)
    print(f"Starting write {message} to {username}'s github history.")
    print(f"Using repo: {username}/{repo}")
    print("-" * 50)
    clone_repo_if_not_exists_already(username, repo)
    execute(repo, dates, number_of_commits_per_day)
    git_push_to_remote_repo(repo)