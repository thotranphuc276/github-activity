import sys
import re
import requests

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Error: No username provided")
    print("Usage: python github-activity.py <username>")
    sys.exit(1)

event_types = {
    "PushEvent": lambda e: f"Pushed {len(e['payload']['commits'])} commits to {e['repo']['name']}",
    "IssuesEvent": lambda e: f"Opened a new issue in {e['repo']['name']}",
    "IssueCommentEvent": lambda e: f"Commented on issue {e['payload']['issue']['number']} in {e['repo']['name']}",
    "PullRequestEvent": lambda e: f"Opened pull request {e['payload']['pull_request']['number']} in {e['repo']['name']}",
    "PullRequestReviewEvent": lambda e: f"Reviewed pull request {e['payload']['pull_request']['number']} in {e['repo']['name']}", 
    "WatchEvent": lambda e: f"Starred {e['repo']['name']}"
}

class GithubActivity:
    def __init__(self, username):
        self.username = username
        self.validate_username()

    def validate_username(self):
        regex = r'^[a-zA-Z0-9_-]+$'
        if not re.match(regex, self.username):
            print(f"Error: Invalid username format: {self.username}")
            print("Username can only contain alphanumeric characters, hyphens, and underscores")
            sys.exit(1)
        return self.username

    def get_user_activity(self):
        url = f"https://api.github.com/users/{self.username}/events"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Check for rate limiting
            remaining_requests = response.headers.get('X-RateLimit-Remaining')
            if remaining_requests and int(remaining_requests) == 0:
                reset_time = response.headers.get('X-RateLimit-Reset')
                print(f"Error: GitHub API rate limit exceeded. Please try again later.")
                sys.exit(1)

            events = response.json()
            
            if not events:
                print(f"No recent activity found for user: {self.username}")
                return

            for event in events:
                event_type = event['type']
                if event_type in event_types:
                    try:
                        print(event_types[event_type](event))
                    except KeyError as e:
                        print(f"Warning: Could not process event due to missing data: {e}")
                        continue
                    except Exception as e:
                        print(f"Warning: Unexpected error processing event: {e}")
                        continue

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Error: User '{self.username}' not found")
            elif e.response.status_code == 403:
                print("Error: GitHub API access denied. You might be rate limited.")
            else:
                print(f"Error: GitHub API request failed with status code {e.response.status_code}")
            sys.exit(1)
        except requests.exceptions.ConnectionError:
            print("Error: Failed to connect to GitHub API. Please check your internet connection.")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Error: An unexpected error occurred: {e}")
            sys.exit(1)

def main():
    try:
        activity = GithubActivity(username)
        activity.get_user_activity()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
