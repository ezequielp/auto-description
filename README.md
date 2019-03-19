# auto-description

Uses JIRA API to generate a summary of work done.

# Installation

Create a python environment and install dependencies

```
python3.6 -m venv pyenv
source py36env/bin/activate
pip install -r requirements.txt
```

# Configuration

Rename `src/configuration.py.sample` to `src/configuration.py` and `auth` to your user name and password. You can customize the generated message.

# Usage

```
jira-description.py [-h] [--date DATE | --today | --yesterday]

optional arguments:
  -h, --help   show this help message and exit
  --date DATE  Generate description for given date
  --today      Generate description for today
  --yesterday  Generate description for yesterday
```
