"""Screen effects: typing, progress bars, cursor simulation"""

import random
import time
from typing import Optional

from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text


class TypingEffect:
    """Character-by-character typing effect with natural variance."""

    def __init__(self, console: Console):
        self.console = console

    def type_text(
        self,
        text: str,
        delay: float = 0.015,
        variance: float = 0.02,
        style: str = "",
        end_newline: bool = True,
    ) -> None:
        """Type text with natural variance in speed.

        Args:
            text: Text to type
            delay: Base delay between characters
            variance: Variance range for delay
            style: Rich style string
            end_newline: Whether to add newline at end
        """
        for char in text:
            self.console.print(char, end="", style=style)
            # Natural typing variance
            if char in ".,!?;:": # Pause longer on punctuation
                time.sleep(delay * 4 + random.uniform(0, variance))
            elif char in " \n\t":  # Slight pause on whitespace
                time.sleep(delay * 0.5)
            else:
                time.sleep(delay + random.uniform(-variance, variance))

        if end_newline:
            self.console.print()

    def type_lines(
        self,
        lines: list[str],
        delay: float = 0.008,
        line_delay: float = 0.05,
        style: str = "",
    ) -> None:
        """Type multiple lines with natural pacing.

        Args:
            lines: List of lines to type
            delay: Base delay per character
            line_delay: Delay between lines
            style: Rich style string
        """
        for i, line in enumerate(lines):
            if i > 0:
                time.sleep(line_delay)
            self.type_text(line, delay=delay, style=style, end_newline=True)


class AnimatedProgress:
    """Animated progress bars using rich.live.Live."""

    def __init__(self, console: Console):
        self.console = console

    def run_progress(
        self,
        task_name: str = "Processing",
        total: int = 100,
        description: str = "Working...",
    ) -> None:
        """Run an animated progress bar.

        Args:
            task_name: Name of the task
            total: Total count
            description: Description text
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}[/]"),
            BarColumn(),
            TextColumn("[dim]{task.completed}/{task.total}[/]"),
            TimeElapsedColumn(),
            console=self.console,
        )

        with Live(progress, console=self.console, refresh_per_second=20, transient=False) as live:
            task_id = progress.add_task(description, total=total)

            for i in range(total + 1):
                progress.update(task_id, completed=i)
                # Natural variation in speed
                base_delay = 0.03
                if i % 10 == 0:
                    time.sleep(base_delay * 3)  # Slight pause every 10%
                elif i % 25 == 0:
                    time.sleep(base_delay * 5)  # Longer pause every 25%
                else:
                    time.sleep(base_delay + random.uniform(-0.01, 0.01))

    def run_spinner(self, message: str = "Processing...", duration: float = 2.0) -> None:
        """Run a simple spinner.

        Args:
            message: Message to display
            duration: How long to spin
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}[/]"),
            console=self.console,
        )

        with Live(progress, console=self.console, refresh_per_second=20) as live:
            task_id = progress.add_task(message, total=100)
            elapsed = 0.0
            step = 10

            while elapsed < duration:
                progress.update(task_id, completed=min(elapsed / duration * 100, 99))
                time.sleep(0.1)
                elapsed += 0.1

            progress.update(task_id, completed=100)


class CursorEffect:
    """Simulates a blinking cursor in the terminal."""

    CURSOR_BLOCK = "█"
    CURSOR_STYLES = ["reverse", "blink"]

    def __init__(self, console: Console):
        self.console = console
        self.visible = True
        self._counter = 0

    def toggle_cursor(self) -> str:
        """Return cursor string, alternating visibility."""
        self.visible = not self.visible
        self._counter += 1
        if self.visible:
            # Use style that creates blinking effect visually
            style = "bold green" if self._counter % 4 == 0 else "green"
            return f"[{style}]{self.CURSOR_BLOCK}[/]"
        return " "

    def print_with_cursor(self, text: str, cursor_after: bool = True) -> None:
        """Print text with cursor at the end.

        Args:
            text: Text to print
            cursor_after: Whether to show cursor after text
        """
        self.console.print(text, end="")
        if cursor_after:
            for _ in range(3):  # Blink a few times
                self.console.print(self.toggle_cursor(), end="", style="")
                time.sleep(0.3)
                self.console.print("\b \b", end="", style="")  # Erase cursor
                time.sleep(0.2)
            self.console.print()  # Final newline


class ScrollingOutput:
    """Simulates scrolling terminal output."""

    def __init__(self, console: Console, max_height: int = 20):
        self.console = console
        self.max_height = max_height
        self.lines: list[str] = []
        self._visible_start = 0

    def add_line(self, line: str, with_live: bool = False) -> None:
        """Add a line and scroll if needed.

        Args:
            line: Line to add
            with_live: Whether to use Live refresh
        """
        self.lines.append(line)

        # Scroll if exceeds max height
        if len(self.lines) > self.max_height:
            self._visible_start = len(self.lines) - self.max_height

    def render(self) -> Panel:
        """Render current visible lines as a panel."""
        visible = self.lines[self._visible_start:]
        text = Text("\n".join(visible))
        return Panel(text, border_style="cyan", title="[dim]Terminal Output[/dim]")

    def clear(self) -> None:
        """Clear all lines."""
        self.lines = []
        self._visible_start = 0