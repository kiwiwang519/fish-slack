"""Output manager and all realistic output formatters"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter
from fish_slack.outputs.git_output import (
    GitStatusFormatter,
    GitDiffFormatter,
    GitLogFormatter,
    GitBranchFormatter,
)
from fish_slack.outputs.pytest_output import PytestOutputFormatter
from fish_slack.outputs.docker_output import DockerOutputFormatter
from fish_slack.outputs.kubectl_output import KubectlOutputFormatter
from fish_slack.outputs.python_output import PythonOutputFormatter
from fish_slack.outputs.generic_output import (
    GenericOutputFormatter,
    LsOutputFormatter,
    CurlOutputFormatter,
    AwsOutputFormatter,
)


class OutputManager:
    """Routes tool calls to appropriate output formatters."""

    def __init__(self):
        self.formatters: list[OutputFormatter] = [
            GitStatusFormatter(),
            GitDiffFormatter(),
            GitLogFormatter(),
            GitBranchFormatter(),
            PytestOutputFormatter(),
            DockerOutputFormatter(),
            KubectlOutputFormatter(),
            PythonOutputFormatter(),
            LsOutputFormatter(),
            CurlOutputFormatter(),
            AwsOutputFormatter(),
            GenericOutputFormatter(),  # fallback last
        ]

    def get_output(self, tool: str, command: str, state: "ProjectState") -> list[str]:
        """Get realistic output for a tool call.

        Args:
            tool: Tool name (e.g., "Bash", "Read", "Edit")
            command: Command/action string
            state: Current project state

        Returns:
            List of output lines
        """
        for formatter in self.formatters:
            if formatter.can_handle(tool, command):
                return formatter.format(state, command=command)
        # Should never reach here since GenericOutputFormatter handles everything
        return ["[output not available]"]