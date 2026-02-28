# analyzer.py
import git
import time

def get_recent_commits(repo_path="."):
    """Checks how many git commits were made in the last hour."""
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        # Get commits from the last 1 hour
        recent_commits = list(repo.iter_commits(since='1.hours.ago'))
        return len(recent_commits)
    except git.exc.InvalidGitRepositoryError:
        return 1  # Default to 1 to avoid punishing non-git directories

def calculate_load(monitor, repo_path="."):
    """
    Heuristic to calculate cognitive load (0-100%):
    - High pauses = High load (stuck thinking)
    - Low key presses = High load (staring at screen)
    - Low commits = High load (no progress)
    """
    elapsed_minutes = (time.time() - monitor.start_time) / 60.0
    if elapsed_minutes < 0.1: 
        return 0 # Not enough data yet

    commits = get_recent_commits(repo_path)
    
    # Calculate penalty based on pauses
    pause_penalty = min(monitor.pauses_over_5_sec * 10, 50)  # Max 50 points from pauses
    
    # Calculate penalty based on lack of commits
    commit_penalty = 30 if commits == 0 else 0  # 30 points if no recent commits
    
    # Calculate penalty based on typing speed (Keys per minute)
    kpm = monitor.key_presses / elapsed_minutes
    typing_penalty = 20 if kpm < 20 else 0      # 20 points if typing incredibly slow
    
    cognitive_load_score = pause_penalty + commit_penalty + typing_penalty
    
    return min(cognitive_load_score, 100) # Cap at 100%