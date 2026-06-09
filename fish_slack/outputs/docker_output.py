"""Realistic docker command outputs"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


CONTAINER_NAMES = [
    "api-server", "postgres-db", "redis-cache", "nginx-proxy",
    "worker-1", "worker-2", "celery-worker", "rabbitmq",
]

IMAGE_NAMES = [
    "api-server:latest", "postgres:15-alpine", "redis:7-alpine",
    "nginx:alpine", "python:3.11-slim", "rabbitmq:3-management",
]


class DockerOutputFormatter(OutputFormatter):
    """Realistic docker outputs."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "docker" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        command = kwargs.get("command", "")

        if "docker ps" in command:
            return self._format_ps()
        elif "docker logs" in command:
            return self._format_logs()
        elif "docker images" in command:
            return self._format_images()
        elif "docker inspect" in command:
            return self._format_inspect()
        else:
            return self._format_generic()

    def _format_ps(self) -> list[str]:
        lines = [
            "CONTAINER ID   IMAGE STATUS        PORTS                    NAMES",
            "------------ ----- ------ -----                    -----",
        ]

        num_containers = random.randint(2, 5)
        for i in range(num_containers):
            cid = ''.join(random.choices('0123456789abcdef', k=12))
            img = random.choice(IMAGE_NAMES)
            status = random.choice(["Up 2 hours", "Up 5 minutes", "Up 45 seconds", "Exited (0) 3 hours ago"])
            ports = random.choice(["0.0.0.0:8080->8080/tcp", "0.0.0.0:5432->5432/tcp", "", "0.0.0.0:6379->6379/tcp"])
            name = CONTAINER_NAMES[i] if i < len(CONTAINER_NAMES) else f"container-{i}"

            lines.append(f"{cid}   {img:17s} {status:13s} {ports:24s} {name}")

        return lines

    def _format_logs(self) -> list[str]:
        log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
        lines = []
        for _ in range(random.randint(8, 15)):
            level = random.choice(log_levels)
            timestamp = f"2026-06-{random.randint(1,9):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
            msg = random.choice([
                "Processing request from client",
                "Query executed in 23ms",
                "Cache hit for key: user_session",
                "Connection established to database",
                "Request completed successfully",
                "Retrying connection (attempt 2/3)",
                "Health check passed",
                "Slow query detected: 1.2s",
                "JWT token validated",
                "Rate limit threshold reached",
            ])
            lines.append(f"{timestamp} - {level} - {msg}")

        return lines

    def _format_images(self) -> list[str]:
        lines = [
            "REPOSITORY               TAG IMAGE ID       SIZE",
            "----- ----- ----- -----",
        ]

        for img in IMAGE_NAMES[:5]:
            size = f"{random.randint(50, 500)}MB"
            img_id = ''.join(random.choices('0123456789abcdef', k=12))
            lines.append(f"{img:21s} latest {img_id}   {size}")

        return lines

    def _format_inspect(self) -> list[str]:
        return [
            "{",
            '    "Id": "a1b2c3d4e5f6...",',
            '    "Name": "/api-server",',
            '    "State": {',
            '        "Status": "running",',
            '        "Running": true,',
            '        "StartedAt": "2026-06-09T10:30:00.000000000Z"',
            "    },",
            '    "Config": {',
            '        "Image": "api-server:latest",',
            '        "Env": [',
            '            "ENV=production",',
            '            "PORT=8080"',
            "        ]",
            "    }",
            "}",
        ]

    def _format_generic(self) -> list[str]:
        return [
            "WARNING: Usage of --flag is deprecated.",
            "This command is not fully implemented in demo mode.",
        ]