"""Realistic kubectl command outputs"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


class KubectlOutputFormatter(OutputFormatter):
    """Realistic kubectl outputs."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and "kubectl" in command

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        command = kwargs.get("command", "")

        if "kubectl get pods" in command:
            return self._format_pods()
        elif "kubectl describe" in command:
            return self._format_describe()
        elif "kubectl logs" in command:
            return self._format_logs()
        elif "kubectl get svc" in command:
            return self._format_svc()
        else:
            return self._format_generic()

    def _format_pods(self) -> list[str]:
        lines = [
            "NAME                        READY   STATUS    RESTARTS   AGE",
            "----- -----   ------    -------- ---",
        ]

        pod_data = [
            ("api-server-7d8f9c6b5-x2k9p", "1/1", "Running", random.randint(0, 3), f"{random.randint(1,30)}d"),
            ("api-server-7d8f9c6b5-y3m7n", "1/1", "Running", random.randint(0, 3), f"{random.randint(1,30)}d"),
            ("postgres-54dc8b9f7-q8r2t", "1/1", "Running", 0, f"{random.randint(31,60)}d"),
            ("redis-7f9b5c4d8-m1n3p", "1/1", "Running", random.randint(0, 2), f"{random.randint(31,60)}d"),
            ("worker-6c8d4f7a9-b5c7d", "1/1", "Running", random.randint(1, 5), f"{random.randint(1,15)}d"),
            ("nginx-ingress-5f7b8c9a-d4e6f", "1/1", "Running", 0, f"{random.randint(60,90)}d"),
        ]

        for name, ready, status, restarts, age in pod_data:
            lines.append(f"{name:28s} {ready:5s} {status:8s} {restarts:5d}       {age}")

        return lines

    def _format_describe(self) -> list[str]:
        lines = [
            "Name: api-server-7d8f9c6b5-x2k9p",
            "Namespace:    default",
            "Priority:     0",
            "Node:         node-pool-1",
            "Start Time:   Mon, 08 Jun 2026 10:30:00 +0000",
            "Labels:       app=api-server",
            "Annotations:  <none>",
            "",
            "Status: Running",
            "IP:           10.128.2.45",
            "Controlled By:  ReplicaSet/api-server-7d8f9c6b5",
            "",
            "Containers:",
            "  api-server:",
            "    Container ID:   docker://a1b2c3d4e5f6...",
            "    Image:          api-server:latest",
            "    Port:           8080/TCP",
            "    State:          Running",
            " Started:      Mon, 08 Jun 2026 10:30:05 +0000",
            "    Ready:          True",
            "    Restart Count:  0",
            "    Limits:",
            "      cpu:     500m",
            "      memory:  512Mi",
            "    Requests:",
            "      cpu:     250m",
            "      memory: 256Mi",
        ]

        return lines

    def _format_logs(self) -> list[str]:
        lines = []
        log_levels = ["INFO", "DEBUG", "WARN", "ERROR"]
        messages = [
            "Processing request: GET /api/v1/users",
            "Database query executed in 12ms",
            "Cache miss for key: session_abc123",
            "JWT token validated successfully",
            "Rate limit check passed",
            "Connection established to redis",
            "Health check passed",
            "Request completed in 45ms",
            "Slow query warning: 1.5s",
            "Authentication failed: invalid token",
        ]

        for _ in range(random.randint(10, 20)):
            level = random.choice(log_levels)
            timestamp = f'2026-06-{random.randint(1,9):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z'
            msg = random.choice(messages)
            lines.append(f"{timestamp} {level:5s} {msg}")

        return lines

    def _format_svc(self) -> list[str]:
        lines = [
            "NAME         TYPE        CLUSTER-IP      PORT(S)        AGE",
            "----- -----       ---------- ------        ----",
            "api-server   ClusterIP   10.128.45.67    8080/TCP      60d",
            "postgres     ClusterIP   10.128.23.45    5432/TCP      60d",
            "redis        ClusterIP   10.128.78.90    6379/TCP      60d",
            "nginx        LoadBalancer 35.92.45.67 80:30080/TCP  45d",
        ]

        return lines

    def _format_generic(self) -> list[str]:
        return ["Unable to connect to cluster. Please check your kubeconfig."]