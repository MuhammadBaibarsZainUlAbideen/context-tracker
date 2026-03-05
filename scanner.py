from git import Repo
from git import Repo
import datetime
import os
import argparse
import json
with open('config.json', 'r') as f:
    data = json.load(f)
path = data["scan_paths"]
context_switching = data["switch_threshold_minutes"]
parser = argparse.ArgumentParser()

parser.add_argument("--today",action="store_true")
parser.add_argument("--week",action="store_true")
parser.add_argument("--month",action="store_true")
parser.add_argument("--days", type=int)

args = parser.parse_args()




def get_commits(path):
    time_frame = 0
    if(args.today):
        time_frame = 1
    elif(args.week):
        time_frame=7
    elif(args.month):
        time_frame=30
    elif args.days:
        time_frame = args.days
    else:
        time_frame=1

    len1 = len(path)
    print(f"Total Path:",len1)
    new_list = []
    for i in path:
        try:
            repo = Repo(i) 
            repo_name = os.path.basename(i)
            since_date = datetime.datetime.now() - datetime.timedelta(days=time_frame)
            recent_commits = repo.iter_commits(since=since_date.strftime('%Y-%m-%d'))
            for commit in recent_commits:
                commit_time = datetime.datetime.fromtimestamp(commit.committed_date)
                new_list.append({
                    'repo_name': repo_name,
                    'timestamp': commit_time,
                    'message': commit.message.strip(),
                    'author': commit.author.name
                })
            
        except Exception as e:
             print(f"Error: {e}")
    new_list.sort(key=lambda x: x['timestamp'])
    return new_list


def detect_switches(commits):
    switches = []
    
    for i in range(1, len(commits)):
        current = commits[i]
        previous = commits[i-1]
        
        
        if current['repo_name'] != previous['repo_name']:
            time_gap = (current['timestamp'] - previous['timestamp']).total_seconds() / 60
            
            if time_gap > context_switching:
                switches.append({
                    'from': previous['repo_name'],
                    'to': current['repo_name'],
                    'time': current['timestamp'],
                    'gap': int(time_gap)
                })
    
    return switches
def calculate_cost(switches):
    total_minutes = len(switches) * 20  
    return {
        'switches': len(switches),
        'minutes': total_minutes,
        'hours': round(total_minutes / 60, 1)
    }

def find_git_repositories(root_path):
    git_repos = []
    
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            if '.git' in dirnames:
                git_repos.append(dirpath)
        a = get_commits(git_repos)
        for commit in a:
            print(f"{commit['timestamp'].strftime('%Y-%m-%d %H:%M')} | {commit['repo_name']:30} | {commit['message']}")
        switches = detect_switches(a)
        print(f"\nCONTEXT SWITCHES: {len(switches)}\n")
        for switch in switches:
            print(f"{switch['time'].strftime('%H:%M')} - {switch['from']} → {switch['to']} (gap: {switch['gap']} min)")
        
        stats = calculate_cost(switches)
        print(f"\nSTATS")
        print(f"Total switches: {stats['switches']}")
        print(f"Time lost: {stats['hours']} hours ({stats['minutes']} minutes)")
    
    except PermissionError as e:
        print(f"Permission denied: {e}")
    
    except PermissionError as e:
        print(f"Permission denied: {e}")
        get_commits(git_repos)
        return git_repos




if __name__ == "__main__":


    user_path = path
    
    repositories = find_git_repositories(user_path)
    