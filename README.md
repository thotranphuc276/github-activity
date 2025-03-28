# GitHub Activity Viewer

A simple Python script to view a GitHub user's recent activity.

## Features

- View recent pushes, issues, pull requests, and other GitHub activities
- Clean command-line output
- Error handling and input validation
- Supports multiple types of GitHub events:
  - Push events
  - Issue events 
  - Issue comments
  - Pull request events
  - Pull request reviews
  - Repository stars

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install requests
```

3. Create an alias for the script:

```bash
alias github-activity="python3 github-activity.py"                                                                                           
```

## Usage

```bash
github-activity <username>
```