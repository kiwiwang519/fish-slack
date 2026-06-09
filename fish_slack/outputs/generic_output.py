"""Generic/fallback output formatters for ls, curl, aws, etc."""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


class GenericOutputFormatter(OutputFormatter):
    """Fallback formatter for commands without specific formatters."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash"

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        command = kwargs.get("command", "")
        return [f"$ {command}", f"[output for: {command}]"]


class LsOutputFormatter(OutputFormatter):
    """Realistic ls -la output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "ls" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        lines = [
            "total56",
            "drwxr-xr-x  5 wanglexin  staff   160 Jun9 10:30 .",
            "drwxr-xr-x  8 wanglexin  staff   256 Jun  9 10:30 ..",
            "drwxr-xr-x  4 wanglexin  staff   128 Jun  9 09:15 .git",
            "-rw-r--r--  1 wanglexin  staff  1024 Jun  9 10:30 README.md",
            "-rw-r--r--  1 wanglexin  staff   512 Jun  8 14:20 requirements.txt",
            "-rw-r--r--  1 wanglexin  staff   2048 Jun  9 10:25 pyproject.toml",
            "drwxr-xr-x 12 wanglexin  staff   384 Jun  9 10:30 src",
            "drwxr-xr-x  3 wanglexin  staff   96 Jun  9 10:30 tests",
            "-rw-r--r--  1 wanglexin  staff   256 Jun  8 16:45 .env",
            "-rw-r--r--  1 wanglexin  staff   128 Jun  7 11:20 .gitignore",
        ]

        return lines


class CurlOutputFormatter(OutputFormatter):
    """Realistic curl HTTP response output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "curl" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        lines = [
            "HTTP/1.1 200 OK",
            "Content-Type: application/json",
            "Content-Length: 156",
            "Date: Tue, 09 Jun 2026 10:30:00 GMT",
            "Server: nginx/1.24.0",
            "",
        ]

        responses = [
            '{"status": "ok", "data": {"users": 42, "active": true}}',
            '{"id": 1, "name": "Alice", "email": "alice@company.com"}',
            '{"result": "success", "message": "Operation completed"}',
            '{"count": 15, "items": [{"id": 1}, {"id": 2}, {"id": 3}]}',
            '{"error": null, "latency_ms": 23}',
        ]

        lines.append(random.choice(responses))

        return lines


class AwsOutputFormatter(OutputFormatter):
    """Realistic AWS CLI output."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "aws" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        command = kwargs.get("command", "")

        if "s3 ls" in command:
            return [
                "2026-06-01 09:00:00 my-bucket-prod",
                "2026-06-03 14:30:00 my-bucket-dev",
                "2026-06-09 10:15:00 data-backups",
            ]
        elif "s3 cp" in command:
            return ["upload: ./local-file to s3://my-bucket-prod/remote-file"]
        elif "ec2 describe-instances" in command:
            return [
                "INSTANCES i-0abcd1234efgh5678 m5.xlarge running us-east-1a",
                "INSTANCES i-0ijkl9012mnop3456 t3.medium running us-east-1b",
            ]
        else:
            return [
                "{",
                '    "Owner": "123456789012",',
                '    "Reservation": "r-0abcdef1",',
                '    "Instances": []',
                "}",
            ]