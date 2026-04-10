"""生成假的工作输出,让老板以为你在用Claude Code工作"""

import random
import time
import uuid
from datetime import datetime
from rich.console import Console
from rich.style import Style
from rich.text import Text

# 配色方案
CLAUDE_BLUE = "cyan"
CLAUDE_GREEN = "green"
CLAUDE_YELLOW = "yellow"
CLAUDE_RED = "red"
CLAUDE_DIM = "bright_black"

# 假的项目/文件名
PROJECT_NAMES = [
    "ai-hedge-fund",
    "data-pipeline",
    "ml-training",
    "api-server",
    "web-frontend",
    "auth-service",
]

FILE_NAMES = [
    "main.py", "utils.py", "config.py", "models.py", "api.py",
    "handler.py", "client.py", "server.py", "database.py", "schema.py",
    "test_main.py", "test_utils.py", "middleware.py", "router.py",
]

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

FILE_OPS = [
    ("Creating", "Creating new file at"),
    ("Editing", "Updating"),
    ("Reading", "Reading"),
    ("Deleting", "Removing"),
    ("Renaming", "Renaming"),
]

TOOL_CALLS = [
    "Bash: ls -la",
    "Bash: git status",
    "Bash: git diff",
    "Bash: grep -r 'function' ./src",
    "Bash: python -m pytest",
    "Bash: curl localhost:8000/health",
    "Bash: docker ps",
    "Bash: kubectl get pods",
    "Bash: aws s3 ls",
    "Read: config.yaml",
    "Read: requirements.txt",
    "Glob: **/*.py",
    "Grep: TODO",
    "Edit: main.py",
    "Write: utils.py",
]

AGENT_NAMES = [
    "planner-agent",
    "code-review-agent",
    "test-agent",
    "docs-agent",
    "refactor-agent",
]

PROGRESS_STATES = [
    "Initializing...",
    "Fetching dependencies...",
    "Analyzing code...",
    "Processing...",
    "Compiling...",
    "Running tests...",
    "Building...",
    "Deploying...",
    "Validating...",
    "Finalizing...",
]


class FakeWorkGenerator:
    def __init__(self, console: Console):
        self.console = console
        self.session_id = str(uuid.uuid4())[:8]
        self.line_count = 0

    def print_header(self):
        """打印Claude Code头"""
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
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]   • Bash — execute shell commands",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]   • Grep — search file contents",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]   • Glob — find files by pattern",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]   • Read — read file contents",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]│[/]   • Edit — modify files",
            style=Style(color=CLAUDE_BLUE)
        )
        self.console.print(
            f"[{CLAUDE_BLUE}]╰─[/]"
        )
        self.line_count += 10

    def print_user_message(self, msg: str = None):
        """打印用户消息"""
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
        self.console.print()
        self.console.print(
            f"[{CLAUDE_YELLOW}]➜[/] [bold]You[/] — {msg}",
            style=Style(color=CLAUDE_YELLOW)
        )
        self.console.print()
        self.line_count += 3

    def print_thinking(self):
        """打印思考过程"""
        self.console.print(
            f"[{CLAUDE_DIM}]Thinking...[/]",
            style=Style(color=CLAUDE_DIM)
        )
        self.line_count += 1
        time.sleep(random.uniform(0.5, 1.5))

        reasoning = random.choice(REASONING_TEMPLATES)
        self.console.print(
            f"[{CLAUDE_DIM}]{' '*4}{reasoning}[/]",
            style=Style(color=CLAUDE_DIM)
        )
        self.line_count += 1

        # 有时候显示子任务
        if random.random() > 0.5:
            for i in range(random.randint(1, 3)):
                task = random.choice(REASONING_TEMPLATES)
                self.console.print(
                    f"[{CLAUDE_DIM}]{' '*8}→ {task}[/]",
                    style=Style(color=CLAUDE_DIM)
                )
                self.line_count += 1
                time.sleep(random.uniform(0.2, 0.5))

    def print_agent_start(self, agent_name: str = None):
        """打印agent开始工作"""
        if agent_name is None:
            agent_name = random.choice(AGENT_NAMES)
        self.console.print()
        self.console.print(
            f"[{CLAUDE_BLUE}][{agent_name}][/] [dim]Starting...[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        self.line_count += 2

    def print_agent_reasoning(self):
        """打印agent推理过程"""
        for _ in range(random.randint(2, 5)):
            reasoning = random.choice(REASONING_TEMPLATES)
            self.console.print(
                f"[{CLAUDE_BLUE}][{random.choice(AGENT_NAMES)}][/] [dim]{reasoning}[/]",
                style=Style(color=CLAUDE_BLUE)
            )
            self.line_count += 1
            time.sleep(random.uniform(0.3, 0.8))

    def print_progress(self):
        """打印进度条"""
        progress_title = random.choice(PROGRESS_STATES)
        total = random.randint(20, 100)
        current = random.randint(5, total - 5)

        self.console.print(
            f"[{CLAUDE_GREEN}]{progress_title}[/] [dim]{current}/{total}[/]"
        )

        # 进度条
        bar_len = 40
        filled = int(bar_len * current / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        self.console.print(f"  [{bar}] {int(current/total*100)}%")
        self.line_count += 2
        time.sleep(random.uniform(0.2, 0.5))

    def print_file_op(self):
        """打印文件操作"""
        op, verb = random.choice(FILE_OPS)
        filename = random.choice(FILE_NAMES)

        colors = {
            "Creating": CLAUDE_GREEN,
            "Editing": CLAUDE_YELLOW,
            "Reading": CLAUDE_BLUE,
            "Deleting": CLAUDE_RED,
            "Renaming": CLAUDE_YELLOW,
        }
        color = colors.get(op, CLAUDE_BLUE)

        self.console.print(
            f"[{color}]{op}:[/] [dim]{filename}[/]",
            style=Style(color=color)
        )
        self.line_count += 1

        if random.random() > 0.6:
            # 显示更多细节
            lines = random.randint(3, 15)
            for _ in range(lines):
                code = "    " + "".join(random.choices(
                    "abcdefghijklmnopqrstuvwxyz0123456789_()[]{}:=",
                    k=random.randint(30, 60)
                ))
                self.console.print(f"[{CLAUDE_DIM}]{code}[/]", style=Style(color=CLAUDE_DIM))
                self.line_count += 1

    def print_tool_call(self):
        """打印工具调用"""
        tool = random.choice(TOOL_CALLS)
        self.console.print(
            f"[{CLAUDE_GREEN}]Tool:[/] [dim]{tool}[/]",
            style=Style(color=CLAUDE_GREEN)
        )
        self.line_count += 1

        # 假输出
        if "Bash" in tool:
            if "ls" in tool:
                self.console.print(f"[{CLAUDE_DIM}]drwxr-xr-x  5 user  staff   160 Apr  9 10:30 .[/]")
                self.console.print(f"[{CLAUDE_DIM}]drwxr-xr-x  8 user  staff   256 Apr  9 10:30 ..[/]")
                self.console.print(f"[{CLAUDE_DIM}]-rw-r--r--  1 user  staff  1024 Apr  9 10:30 README.md[/]")
                self.console.print(f"[{CLAUDE_DIM}]drwxr-xr-x 12 user  staff   384 Apr  9 10:30 src[/]")
                self.line_count += 4
            elif "git" in tool:
                self.console.print(f"[{CLAUDE_DIM}]On branch main[/]")
                self.console.print(f"[{CLAUDE_DIM}]nothing to commit, working tree clean[/]")
                self.line_count += 2
            elif "pytest" in tool:
                self.console.print(f"[{CLAUDE_GREEN}]===== 15 passed in 2.34s =====[/]")
                self.line_count += 1

        time.sleep(random.uniform(0.1, 0.4))

    def print_agent_done(self):
        """打印agent完成"""
        agent_name = random.choice(AGENT_NAMES)
        confidence = random.randint(60, 99)
        self.console.print()
        self.console.print(
            f"[{CLAUDE_BLUE}][{agent_name}][/] [green]Completed[/] [dim]— confidence {confidence}%[/]",
            style=Style(color=CLAUDE_BLUE)
        )
        self.line_count += 3

    def print_summary(self):
        """打印总结"""
        self.console.print()
        self.console.print(
            f"[{CLAUDE_GREEN}]✓[/] [bold]Analysis complete[/]"
        )
        self.console.print()
        self.line_count += 3

    def generate_session(self, duration: int = 10):
        """生成一段假的工作会话

        Args:
            duration: 大约持续时间(秒)
        """
        self.print_header()
        self.print_user_message()

        start_time = time.time()

        while time.time() - start_time < duration:
            # 随机选择一种输出类型
            choice = random.random()

            if choice < 0.15:
                self.print_thinking()
            elif choice < 0.30:
                self.print_agent_start()
                self.print_agent_reasoning()
                self.print_agent_done()
            elif choice < 0.45:
                self.print_progress()
            elif choice < 0.60:
                self.print_file_op()
            elif choice < 0.75:
                self.print_tool_call()
            else:
                self.print_thinking()

            # 偶尔换行
            if random.random() > 0.7:
                self.console.print()

            time.sleep(random.uniform(0.5, 1.5))

        self.print_summary()
