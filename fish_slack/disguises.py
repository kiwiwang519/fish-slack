"""Software disguise renderers - different looks for the same output"""

import random
from abc import ABC, abstractmethod
from typing import Optional

from rich.console import Console
from rich.text import Text


class DisguiseRenderer(ABC):
    """Base class for all software disguises."""

    @abstractmethod
    def render_workflow_start(self, workflow_name: str) -> list[str]:
        """Render the start of a workflow."""
        pass

    @abstractmethod
    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        """Render a tool call with its output."""
        pass

    @abstractmethod
    def render_thinking(self, text: str) -> list[str]:
        """Render thinking/reasoning output."""
        pass

    @abstractmethod
    def render_novel(self, lines: list[str]) -> list[str]:
        """Render novel content in this disguise's style."""
        pass

    @abstractmethod
    def render_user_message(self, text: str) -> list[str]:
        """Render user message."""
        pass


# ANSI color codes for advanced styling
class ANSI:
    """ANSI escape codes."""
    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    ITALIC = "\x1b[3m"
    UNDERLINE = "\x1b[4m"
    RESET = "\x1b[0m"
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    BG_BLACK = "\x1b[40m"


class ClaudeDisguiseRenderer(DisguiseRenderer):
    """Original Claude Code style disguise."""

    CLAUDE_BLUE = "cyan"
    CLAUDE_GREEN = "green"
    CLAUDE_YELLOW = "yellow"
    CLAUDE_DIM = "bright_black"

    def render_workflow_start(self, workflow_name: str) -> list[str]:
        return [
            f"[{self.CLAUDE_BLUE}]╭─[/] [bold]Starting workflow:[/] [cyan]{workflow_name}[/]",
            f"[{self.CLAUDE_BLUE}]│[/]",
        ]

    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        lines = [
            f"[{self.CLAUDE_GREEN}]Tool:[/] [dim]{tool}: {command}[/]",
        ]
        for line in output:
            lines.append(f"[{self.CLAUDE_DIM}]{' ' + line}[/]")
        return lines

    def render_thinking(self, text: str) -> list[str]:
        return [
            f"[{self.CLAUDE_DIM}]Thinking...[/]",
            f"[{self.CLAUDE_DIM}]{'    ' + text}[/]",
        ]

    def render_novel(self, lines: list[str]) -> list[str]:
        return lines # Already formatted by NovelReader

    def render_user_message(self, text: str) -> list[str]:
        return [
            f"[{self.CLAUDE_YELLOW}]➜[/] [bold]You[/] — {text}",
        ]


class VSCodeTerminalDisguise(DisguiseRenderer):
    """Renders output as VS Code integrated terminal."""

    def render_workflow_start(self, workflow_name: str) -> list[str]:
        return [
            f"\x1b[37mStarting {workflow_name}...\x1b[0m",
        ]

    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        lines = [
            f"\x1b[33m❯\x1b[0m \x1b[36m{command}\x1b[0m",
        ]
        for line in output:
            lines.append(f"   \x1b[90m{line}\x1b[0m")
        return lines

    def render_thinking(self, text: str) -> list[str]:
        return [
            f"\x1b[90m⟳ {text}\x1b[0m",
        ]

    def render_novel(self, lines: list[str]) -> list[str]:
        # In VS Code terminal style, show as output with faint styling
        formatted = []
        for line in lines:
            formatted.append(f"\x1b[90m│ {line}\x1b[0m")
        return formatted

    def render_user_message(self, text: str) -> list[str]:
        return [
            f"\x1b[31m➜\x1b[0m \x1b[1m{text}\x1b[0m",
        ]


class JupyterDisguise(DisguiseRenderer):
    """Renders output as Jupyter notebook cells."""

    cell_counter = 0

    def _next_cell(self) -> int:
        JupyterDisguise.cell_counter += 1
        return JupyterDisguise.cell_counter

    def render_workflow_start(self, workflow_name: str) -> list[str]:
        n = self._next_cell()
        return [
            f"\x1b[36mIn [\x1b[1m{n}\x1b[0m]: \x1b[34m# {workflow_name}\x1b[0m",
            "",
        ]

    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        n = self._next_cell()
        lines = [
            f"\x1b[36mIn [\x1b[1m{n}\x1b[0m]: \x1b[34m{command}\x1b[0m",
            ""
        ]
        for line in output:
            lines.append(line)
        lines.append("")

        # Out cell
        out_n = n
        lines.append(f"\x1b[36mOut[\x1b[1m{out_n}\x1b[0m]:")
        return lines

    def render_thinking(self, text: str) -> list[str]:
        return [
            f"\x1b[90m# ⟳ {text}\x1b[0m",
        ]

    def render_novel(self, lines: list[str]) -> list[str]:
        # Novel as blue comments
        formatted = []
        for line in lines:
            formatted.append(f"\x1b[34m# {line}\x1b[0m")
        return formatted

    def render_user_message(self, text: str) -> list[str]:
        return [
            f"\x1b[35m# User: {text}\x1b[0m",
        ]


class MySQLCLIDisguise(DisguiseRenderer):
    """Renders output as MySQL CLI."""

    def render_workflow_start(self, workflow_name: str) -> list[str]:
        return [
            f"\x1b[36mmysql>\x1b[0m \x1b[1m-- Starting: {workflow_name}\x1b[0m",
        ]

    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        lines = [
            f"\x1b[36mmysql>\x1b[0m \x1b[33m{command}\x1b[0m",
        ]

        if output:
            # Format as a table
            col_width = max(len(output[0]) if output else 20, 20)
            lines.append(f"\x1b[36m+\x1b[0m" + "-" * col_width + f"\x1b[36m+\x1b[0m")
            for row in output:
                lines.append(f"\x1b[36m|\x1b[0m {row}" + " " * (col_width - len(row)) + f"\x1b[36m|\x1b[0m")
            lines.append(f"\x1b[36m+\x1b[0m" + "-" * col_width + f"\x1b[36m+\x1b[0m")

        row_count = len(output)
        lines.append(f"\x1b[32m{row_count} rows in set\x1b[0m")

        return lines

    def render_thinking(self, text: str) -> list[str]:
        return [
            f"\x1b[90m/* {text} */\x1b[0m",
        ]

    def render_novel(self, lines: list[str]) -> list[str]:
        # Novel as SQL comments
        return [f"\x1b[90m-- {line}\x1b[0m" for line in lines]

    def render_user_message(self, text: str) -> list[str]:
        return [
            f"\x1b[35m-- User query: {text}\x1b[0m",
        ]


class VimDisguise(DisguiseRenderer):
    """Renders output as vim editor showing a file."""

    def render_workflow_start(self, workflow_name: str) -> list[str]:
        return [
            f"\x1b[32m\" Starting workflow: {workflow_name}\x1b[0m",
            f"\x1b[33m\" [No Name]100%, 50%  (UTF-8 DOS CRLF)\x1b[0m",
            "",
        ]

    def render_tool_call(self, tool: str, command: str, output: list[str]) -> list[str]:
        # Simulate vim command mode output
        lines = [
            f"\x1b[36m:!{command}\x1b[0m",
        ]
        for line in output:
            lines.append(f"   \x1b[90m{line}\x1b[0m")
        lines.append(f"\x1b[33mPress ENTER or type command to continue\x1b[0m")
        return lines

    def render_thinking(self, text: str) -> list[str]:
        return [
            f"\x1b[90m\" {text}\x1b[0m",
        ]

    def render_novel(self, lines: list[str]) -> list[str]:
        # Simulate vim with novel content as "file contents"
        header = [
            f"\x1b[32m\" novel_chapter.txt\x1b[0m",
            f"\x1b[33m\" {random.randint(1,100)}%, {random.randint(0,100)}%  (UTF-8 DOS CRLF)\x1b[0m",
            "",
        ]
        content = []
        for i, line in enumerate(lines, 1):
            # Calculate line number width
            line_num = str(i).rjust(4)
            content.append(f"  {line_num} \x1b[37m{line}\x1b[0m")
        content.append("~\x1b[0m")  # vim end-of-file marker
        return header + content

    def render_user_message(self, text: str) -> list[str]:
        return [
            f"\x1b[35m\" User: {text}\x1b[0m",
        ]


def get_disguise_renderer(name: str) -> DisguiseRenderer:
    """Get a disguise renderer by name."""
    renderers = {
        "claude": ClaudeDisguiseRenderer,
        "vscode": VSCodeTerminalDisguise,
        "jupyter": JupyterDisguise,
        "mysql": MySQLCLIDisguise,
        "vim": VimDisguise,
    }
    renderer_class = renderers.get(name, ClaudeDisguiseRenderer)
    return renderer_class()