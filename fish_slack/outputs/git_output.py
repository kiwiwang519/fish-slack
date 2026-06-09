"""Realistic git command outputs"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


# Realistic git diff hunk templates
DIFF_HUNK_TEMPLATES = [
    {
        "file": "src/models.py",
        "old_lines": ["from typing import Optional", "from dataclasses import dataclass", "", "@dataclass", "class User:"],
        "new_lines": ["from typing import Optional", "from dataclasses import dataclass", "import logging", "", "@dataclass", "class User:", "    debug: bool = False"],
    },
    {
        "file": "src/api.py",
        "old_lines": ["@app.get('/users')", "def get_users():", "    return {'users': []}"],
        "new_lines": ["@app.get('/users')", "def get_users():", "    users = db.query(User).all()", "    return {'users': [u.dict() for u in users]}"],
    },
    {
        "file": "tests/test_api.py",
        "old_lines": ["def test_api():", "    assert True"],
        "new_lines": ["def test_api():", "    response = client.get('/api/v1/users')", "    assert response.status_code == 200"],
    },
    {
        "file": "config.py",
        "old_lines": ["DEBUG = True", "PORT = 8000"],
        "new_lines": ["DEBUG = False", "PORT = 8080", "LOG_LEVEL = 'INFO'"],
    },
]


class GitStatusFormatter(OutputFormatter):
    """Realistic git status output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "git status" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        lines = [
            f"On branch {state.current_branch}",
            "",
        ]

        if state.modified_files:
            lines.append("Changes not staged for commit:")
            lines.append("  (use \"git add <file>...\" to update what will be committed)")
            lines.append("")
            for f in state.modified_files:
                status = random.choice(["modified: ", "modified:   "])
                lines.append(f"\t{status}{f}")
            lines.append("")

        if state.new_files:
            lines.append("Untracked files:")
            lines.append("  (use \"git add <file>...\" to include in what will be committed)")
            lines.append("")
            for f in state.new_files:
                lines.append(f"\t{f}")
            lines.append("")

        if not state.modified_files and not state.new_files:
            lines.append("nothing to commit, working tree clean")

        return lines


class GitDiffFormatter(OutputFormatter):
    """Realistic git diff output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "git diff" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        if not state.modified_files:
            return [""]

        lines = []
        files_to_show = state.modified_files[:2]  # Show at most 2 files

        for file in files_to_show:
            # Pick a random hunk template
            hunk = random.choice(DIFF_HUNK_TEMPLATES)

            # Generate a fake hash
            old_hash = ''.join(random.choices('0123456789abcdef', k=7))
            new_hash = ''.join(random.choices('0123456789abcdef', k=7))

            lines.append(f"diff --git a/{file} b/{file}")
            lines.append(f"index {old_hash}..{new_hash} 100644")
            lines.append(f"--- a/{file}")
            lines.append(f"+++ b/{file}")

            # Show a few diff hunks
            old_start = random.randint(1, 10)
            new_start = old_start

            lines.append(f"@@ -{old_start},{len(hunk['old_lines'])} +{new_start},{len(hunk['new_lines'])} @@")

            for old_line, new_line in zip(hunk['old_lines'], hunk['new_lines']):
                if old_line == new_line:
                    lines.append(f" {old_line}")
                else:
                    if old_line:
                        lines.append(f"-{old_line}")
                    if new_line:
                        lines.append(f"+{new_line}")

            # Handle lines that were added
            if len(hunk['new_lines']) > len(hunk['old_lines']):
                for extra in hunk['new_lines'][len(hunk['old_lines']):]:
                    lines.append(f"+{extra}")

            lines.append("")

        return lines


class GitLogFormatter(OutputFormatter):
    """Realistic git log output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "git log" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        lines = []

        for i, commit_msg in enumerate(state.recent_commits[:5]):
            hash_prefix = ''.join(random.choices('0123456789abcdef', k=7))
            author = random.choice(["Dev Team", "Alice Chen", "Bob Smith", "Jane Doe"])
            date = f"{random.randint(1,12)} {random.choice(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])} {random.randint(10,29)} {random.randint(10,23)}:{random.randint(10,59)}:{random.randint(10,59)}2026"

            lines.append(f"commit {hash_prefix}")
            lines.append(f"Author: {author} <{author.lower().replace(' ', '.')}@company.com>")
            lines.append(f"Date:   {date}")
            lines.append("")
            lines.append(f"    {commit_msg}")
            lines.append("")

        return lines


class GitBranchFormatter(OutputFormatter):
    """Realistic git branch output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "git branch" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        branches = ["main", "develop", "feature/auth", "feature/api", "fix/bug", "release/v1.0"]
        current = state.current_branch

        lines = []
        for branch in branches:
            if branch == current:
                lines.append(f"* {branch}")
            else:
                lines.append(f"  {branch}")

        return lines