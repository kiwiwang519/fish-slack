"""Base class for realistic output formatters"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState


class OutputFormatter(ABC):
    """Base class for realistic output formatters."""

    @abstractmethod
    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        """Return list of output lines for this tool.

        Args:
            state: Current project state for context-aware output
            **kwargs: Additional context (e.g., command string)

        Returns:
            List of output lines (without trailing newlines)
        """
        pass

    @abstractmethod
    def can_handle(self, tool: str, command: str) -> bool:
        """Check if this formatter handles the given tool/command.

        Args:
            tool: Tool name (e.g., "Bash", "Read", "Edit")
            command: Command/action string

        Returns:
            True if this formatter handles the given tool/command
        """
        pass