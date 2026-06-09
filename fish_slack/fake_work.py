"""Generate fake work output with realistic context-aware workflows"""

import random
import time
import uuid
from typing import TYPE_CHECKING, Optional

from rich.console import Console
from rich.style import Style
from rich.text import Text

if TYPE_CHECKING:
    from fish_slack.state import ProjectState
    from fish_slack.outputs import OutputManager
    from fish_slack.workflows import WorkflowEngine
    from fish_slack.screen_effects import TypingEffect
    from fish_slack.disguises import DisguiseRenderer

# 配色方案
CLAUDE_BLUE = "cyan"
CLAUDE_GREEN = "green"
CLAUDE_YELLOW = "yellow"
CLAUDE_RED = "red"
CLAUDE_DIM = "bright_black"

REASONING_TEMPLATES = [
    "Analyzing the codebase structure to understand dependencies",
    "Planning implementation approach for this feature",
    "Reviewing existing patterns in the codebase",
    "Checking API compatibility and potential breaking changes",
    "Optimizing the algorithm for better performance",
    "Debugging the reported issue step by step",
    "Refactoring to improve code quality and maintainability",
    "Writing unit tests to ensure code correctness",
    "Documenting the public API for future reference",
    "Evaluating different library options for this use case",
    "Analyzing memory usage and potential leaks",
    "Reviewing security implications of the changes",
    "Checking edge cases and error handling paths",
    "Benchmarking critical paths for optimization opportunities",
]


class FakeWorkGenerator:
    """Generates realistic fake Claude Code work output."""

    def __init__(
        self,
        console: Console,
        state: Optional["ProjectState"] = None,
        output_manager: Optional["OutputManager"] = None,
        workflow_engine: Optional["WorkflowEngine"] = None,
        typing_effect: Optional["TypingEffect"] = None,
        disguise_renderer: Optional["DisguiseRenderer"] = None,
    ):
        self.console = console
        self.session_id = str(uuid.uuid4())[:8]
        self.line_count = 0

        # Injected dependencies for advanced features
        self.state = state
        self.output_manager = output_manager
        self.workflow_engine = workflow_engine
        self.typing_effect = typing_effect
        self.disguise_renderer = disguise_renderer

    def print_header(self) -> None:
        """Print Claude Code header."""
        self.console.print(
            f"[{CLAUDE_BLUE}]╭─[/] [bold]Welcome to[/] [bold cyan]Claude Code[/][cyan] ─[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/] [dim]Session: {self.session_id}[/]    [dim]Model: claude-sonnet-4-6[/]    [dim]Location: ~/projects[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]├─[/] [bold]Available Tools:[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        for tool in ["Bash", "Grep", "Glob", "Read", "Edit"]:
            self.console.print(
                f"[{CLAUDE_BLUE}]│[/]   • {tool}",
                style=Style(color=CLAUDE_BLUE)
            )
        self.console.print(
            f"[{CLAUDE_BLUE}]╰─[/]"
        )
        self.line_count += 10

    def print_user_message(self, msg: str = None) -> None:
        """Print user message."""
        if msg is None:
            msg = random.choice([
                "帮我检查一下这个函数的bug",
                "review the code and fix performance issues",
                "add unit tests for the new feature",
                "优化这个算法的性能",
                "refactor the authentication module",
                "check api endpoint for security issues",
                "implement the new dashboard feature",
                "fix the memory leak in the worker",
            ])

        if self.disguise_renderer:
            lines = self.disguise_renderer.render_user_message(msg)
            for line in lines:
                self.console.print(line)
        else:
            self.console.print()
            self.console.print(
                f"[{CLAUDE_YELLOW}]➜[/] [bold]You[/] — {msg}",
                style=Style(color=CLAUDE_YELLOW)
            )
            self.console.print()

        self.line_count += 3

    def print_thinking(self, text: str = None) -> None:
        """Print thinking/reasoning output."""
        if text is None:
            text = random.choice(REASONING_TEMPLATES)

        if self.disguise_renderer:
            lines = self.disguise_renderer.render_thinking(text)
            for line in lines:
                self.console.print(line)
            self.line_count += len(lines)
        else:
            self.console.print(
                f"[{CLAUDE_DIM}]Thinking...[/]",
                style=Style(color=CLAUDE_DIM)
            )
            self.line_count += 1
            time.sleep(random.uniform(0.5, 1.5))

            self.console.print(
                f"[{CLAUDE_DIM}]{' '*4}{text}[/]",
                style=Style(color=CLAUDE_DIM)
            )
            self.line_count += 1

            # Sometimes show sub-tasks
            if random.random() > 0.5:
                for i in range(random.randint(1, 3)):
                    task = random.choice(REASONING_TEMPLATES)
                    self.console.print(
                        f"[{CLAUDE_DIM}]{' '*8}→ {task}[/]",
                        style=Style(color=CLAUDE_DIM)
                    )
                    self.line_count += 1
                    time.sleep(random.uniform(0.2, 0.5))

    def print_tool_call(self, tool: str, command: str, output: list[str]) -> None:
        """Print a tool call with output."""
        if self.disguise_renderer:
            lines = self.disguise_renderer.render_tool_call(tool, command, output)
            for line in lines:
                self.console.print(line)
            self.line_count += len(lines)
        else:
            self.console.print(
                f"[{CLAUDE_GREEN}]Tool:[/] [dim]{tool}: {command}[/]",
                style=Style(color=CLAUDE_GREEN)
            )
            self.line_count += 1

            for line in output:
                self.console.print(
                    f"[{CLAUDE_DIM}]{' ' + line}[/]",
                    style=Style(color=CLAUDE_DIM)
                )
                self.line_count += 1

        time.sleep(random.uniform(0.1, 0.4))

    def print_workflow_output(self, workflow_results: list[dict]) -> None:
        """Print output from a workflow execution.

        Args:
            workflow_results: List of step results from WorkflowEngine.run_workflow
        """
        for step_result in workflow_results:
            # Show thinking if enabled
            if step_result.get("show_thinking") and step_result.get("thinking"):
                self.print_thinking(step_result["thinking"])
                time.sleep(random.uniform(0.3, 0.6))

            # Show tool call with output
            self.print_tool_call(
                step_result["tool"],
                step_result["command"],
                step_result["output"]
            )

            # Show failure state if applicable
            if step_result.get("failed"):
                self.console.print(
                    f"[{CLAUDE_RED}]! Tool call failed (expected in workflow)[/]",
                    style=Style(color=CLAUDE_RED)
                )
                self.line_count += 1

            time.sleep(random.uniform(0.5, 1.0))

    def generate_session(self, duration: int = 10) -> None:
        """Generate a complete fake work session.

        Uses the workflow engine if available, otherwise falls back to
        simple random output generation.
        """
        self.print_header()
        self.print_user_message()

        start_time = time.time()

        if self.workflow_engine and self.output_manager:
            # Use the workflow engine for realistic context-aware output
            while time.time() - start_time < duration:
                results, self.state = self.workflow_engine.select_and_run()
                self.print_workflow_output(results)

                time.sleep(random.uniform(1.0, 2.0))
        else:
            # Fallback to simple random generation
            while time.time() - start_time < duration:
                choice = random.random()

                if choice < 0.3:
                    self.print_thinking()
                elif choice < 0.5:
                    self.print_thinking()
                    self.print_tool_call(
                        "Bash",
                        random.choice([
                            "git status",
                            "pytest tests/",
                            "docker ps",
                            "ls -la src/",
                        ]),
                        ["output line 1", "output line 2"]
                    )
                elif choice < 0.7:
                    self.print_tool_call(
                        "Bash",
                        random.choice([
                            "git diff",
                            "kubectl get pods",
                            "curl localhost:8000/health",
                        ]),
                        ["line 1", "line 2", "line 3"]
                    )
                else:
                    self.print_thinking()

                time.sleep(random.uniform(0.5, 1.5))

        self.print_summary()

    def print_summary(self) -> None:
        """Print session summary."""
        self.console.print()
        self.console.print(
            f"[{CLAUDE_GREEN}]✓[/] [bold]Analysis complete[/]"
        )
        self.console.print()
        self.line_count += 3