#!/usr/bin/env python3
"""Fish Slack - 摸鱼终端工具

伪装成Claude Code工作的终端摸鱼工具。
"""

import argparse
import sys
import time
import random
import select
import termios
import tty
import fcntl
import os
from pathlib import Path

from rich.console import Console

# Import from fish_slack package
try:
    from fish_slack.fake_work import FakeWorkGenerator
    from fish_slack.novel import NovelReader
    from fish_slack.state import create_initial_state
    from fish_slack.outputs import OutputManager
    from fish_slack.workflows import WorkflowEngine
    from fish_slack.screen_effects import TypingEffect, AnimatedProgress
    from fish_slack.disguises import get_disguise_renderer
except ImportError:
    from fake_work import FakeWorkGenerator
    from novel import NovelReader
    from state import create_initial_state
    from outputs import OutputManager
    from workflows import WorkflowEngine
    from screen_effects import TypingEffect, AnimatedProgress
    from disguises import get_disguise_renderer

# 配色
CLAUDE_BLUE = "cyan"
CLAUDE_GREEN = "green"
CLAUDE_YELLOW = "yellow"
CLAUDE_DIM = "bright_black"
CLAUDE_RED = "red"


class FishSlack:
    """摸鱼终端工具 - 逼真版"""

    def __init__(
        self,
        novel_path: str = None,
        disguise: str = "code",
        lines_per_page: int = 15,
        software_disguise: str = "claude",
    ):
        self.console = Console()
        self.novel = NovelReader(novel_path)
        self.disguise = disguise
        self.lines_per_page = lines_per_page
        self.software_disguise = software_disguise

        # Initialize state and output systems
        self.state = create_initial_state()
        self.output_manager = OutputManager()
        self.workflow_engine = WorkflowEngine(self.state, self.output_manager)
        self.typing_effect = TypingEffect(self.console)
        self.progress_effect = AnimatedProgress(self.console)
        self.disguise_renderer = get_disguise_renderer(software_disguise)

        # Initialize FakeWorkGenerator with all dependencies
        self.work_gen = FakeWorkGenerator(
            console=self.console,
            state=self.state,
            output_manager=self.output_manager,
            workflow_engine=self.workflow_engine,
            typing_effect=self.typing_effect,
            disguise_renderer=self.disguise_renderer,
        )

        self.display_mode = "working"
        self.last_mode_change = time.time()
        self.workflow_count = 0

    def import_novel(self, path: str, auto_convert_gbk: bool = True) -> bool:
        """导入小说，自动转换 GBK 编码"""
        if auto_convert_gbk:
            try:
                from fish_slack.novel import convert_gbk_to_utf8
                path = convert_gbk_to_utf8(path)
                self.console.print(f"[{CLAUDE_GREEN}]✓[/] GBK → UTF-8 转换完成")
            except Exception:
                pass  # 转换失败时继续尝试直接加载

        if self.novel.load_novel(path):
            self.console.print(f"[{CLAUDE_GREEN}]✓[/] 已加载小说: {path}")
            return True
        else:
            self.console.print(f"[{CLAUDE_RED}]✗[/] 无法加载小说: {path}")
            return False

    def _print_header(self) -> None:
        """打印头部"""
        mode_names = {
            "working": "[bold]工作模式[/] (自动滚动)",
            "reading": "[bold]阅读模式[/] (静止)",
        }

        self.console.print()
        self.console.print(f"[{CLAUDE_BLUE}]╭─[/] [bold cyan]Fish Slack[/][{CLAUDE_BLUE}] ────────────────────────────────────────────[/]")
        self.console.print(f"[{CLAUDE_BLUE}]│[/]  {mode_names.get(self.display_mode, '')}")
        self.console.print(f"[{CLAUDE_BLUE}]│[/]  [dim]伪装: {self.software_disguise}[/] | [dim]项目: {self.state.project_name}[/]")
        self.console.print(f"[{CLAUDE_BLUE}]╰─[/]")
        self.console.print()

    def _print_work_area(self) -> None:
        """打印工作区 - 使用工作流引擎"""
        self.console.print(f"[{CLAUDE_BLUE}]┌─[/][bold] Terminal Output [/][{CLAUDE_BLUE}]───[/]")
        self.console.print(f"[{CLAUDE_BLUE}]│[/]")

        # Generate a workflow with realistic multi-step output
        self.work_gen.print_user_message()

        # Run a context-aware workflow
        workflow_results, self.state = self.workflow_engine.select_and_run()
        self.work_gen.print_workflow_output(workflow_results)

        self.console.print(f"[{CLAUDE_BLUE}]╰─[/]")
        self.console.print()

        self.workflow_count += 1

    def _print_novel_area(self) -> None:
        """打印小说区 - 阅读模式下交替显示小说和代码"""
        if self.display_mode == "working":
            return

        # 阅读模式：交替显示 2行小说 + 1行代码
        lines = self.novel.get_alternating_lines(novel_count=2, code_count=1, total_lines=30)

        if lines:
            self.console.print(f"[{CLAUDE_YELLOW}]┌─[/][bold] Reading Novel [/][{CLAUDE_YELLOW}]───[/]")
            for line in lines:
                line = line.rstrip('\n\r')
                self.console.print(f"[{CLAUDE_YELLOW}]│[/] {line}")
            self.console.print(f"[{CLAUDE_YELLOW}]╰─[/]")

    def _format_novel(self, lines: list[str]) -> str:
        """格式化小说"""
        if not lines:
            return ""

        if self.disguise == "json":
            return self.novel.format_as_json(lines)
        elif self.disguise == "csv":
            return self.novel.format_as_csv(lines)
        elif self.disguise == "error":
            return self.novel.format_as_error_log(lines)
        else:
            return self.novel.format_as_code(lines, f"novel_{random.randint(100, 999)}.txt")

    def _print_status_bar(self) -> None:
        """打印状态栏"""
        novel_status = ""
        if self.novel.novel_path:
            filename = Path(self.novel.novel_path).name
            total = len(self.novel.content) if self.novel.content else 0
            progress = f"{self.novel.current_pos}/{total}"
            novel_status = f"  小说: {filename} [{progress}]"

        mode_hints = f"[{CLAUDE_DIM}]W工作 | R阅读 | 空格滚动 | Q退出{novel_status}[/]"
        self.console.print(mode_hints)

    def _handle_keypress(self) -> None:
        """检查按键并处理"""
        try:
            # 使用非阻塞读取
            fd = sys.stdin.fileno()
            old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

            try:
                ch = sys.stdin.read(1)
                if ch:
                    ch = ch.upper()
                    if ch == 'W':
                        self.display_mode = "working"
                        self.console.clear()
                    elif ch == 'R':
                        self.display_mode = "reading"
                        self.console.clear()
                    elif ch == ' ':  # 空格 - 阅读模式下滚动
                        if self.display_mode == "reading":
                            self._scroll_reading()
                    elif ch == 'Q':
                        self.console.print("\n[cyan]再见！[/]")
                        self._restore_stdin()
                        sys.exit(0)
            finally:
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
        except Exception:
            pass

    def _scroll_reading(self) -> None:
        """阅读模式下滚动 - 获取下一批交替内容"""
        self.console.clear()
        self._print_header()
        self._print_novel_area()
        self._print_status_bar()

    def _setup_stdin(self) -> None:
        """设置终端为原始模式"""
        try:
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except termios.error:
            pass

    def _restore_stdin(self) -> None:
        """恢复终端设置"""
        if hasattr(self, '_old_settings'):
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)

    def run(self) -> None:
        """运行主循环"""
        # 默认进入工作模式
        time.sleep(random.uniform(0.5, 1.5))
        self.display_mode = "working"
        self.console.clear()
        self._setup_stdin()

        try:
            while True:
                self._handle_keypress()

                if self.display_mode == "reading":
                    # 阅读模式：静止不动，等待空格滚动
                    time.sleep(0.5)
                else:
                    # 工作模式：自动滚动
                    self._print_header()
                    self._print_work_area()
                    self._print_novel_area()
                    self._print_status_bar()
                    time.sleep(3)
                    self.console.clear()

        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.console.print(f"[{CLAUDE_RED}]错误: {e}[/]")
        finally:
            self._restore_stdin()

    DISGUISE_FORMATS = {
        "code": "代码样式",
        "json": "JSON日志",
        "csv": "CSV日志",
        "error": "错误日志",
    }

    SOFTWARE_DISGUISES = {
        "claude": "Claude Code",
        "vscode": "VS Code Terminal",
        "jupyter": "Jupyter Notebook",
        "mysql": "MySQL CLI",
        "vim": "Vim Editor",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fish Slack - 摸鱼终端工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  fish-slack -n ~/novel.txt              # 加载小说
  fish-slack -n ~/novel.txt -f json      # JSON日志格式
  fish-slack -n ~/novel.txt -s vscode    # VS Code终端风格
  fish-slack -s jupyter -n ~/novel.txt   # Jupyter风格

快捷键:
  W    切换到工作模式
  F    切换到摸鱼模式
  Q    退出

软件伪装模式:
  claude   Claude Code (默认)
  vscode   VS Code 集成终端
  jupyter  Jupyter Notebook
  mysql    MySQL CLI
  vim      Vim 编辑器
        """
    )

    parser.add_argument('-n', '--novel', type=str, default=None, help='小说文件路径 (.txt)')
    parser.add_argument('-f', '--format', type=str, choices=['code', 'json', 'csv', 'error'],
                        default='code', help='小说伪装格式 (默认: code)')
    parser.add_argument('-l', '--lines', type=int, default=15, help='每页显示行数 (默认: 15)')
    parser.add_argument('-s', '--software-disguise', type=str,
                        choices=['claude', 'vscode', 'jupyter', 'mysql', 'vim'],
                        default='claude', help='软件伪装模式 (默认: claude)')

    args = parser.parse_args()

    console = Console()
    app = FishSlack(
        novel_path=args.novel,
        disguise=args.format,
        lines_per_page=args.lines,
        software_disguise=args.software_disguise,
    )

    console.print()
    console.print("[bold cyan]🐟 Fish Slack - 摸鱼终端[/]")
    console.print("[dim]伪装成工作的终端摸鱼工具[/]")
    console.print()
    console.print(f"[dim]软件伪装: {app.SOFTWARE_DISGUISES.get(args.software_disguise, 'Claude Code')}[/]")
    console.print()

    if args.novel:
        if app.import_novel(args.novel):
            console.print(f"[dim]小说格式: {args.format}[/]")
    else:
        console.print("[yellow]提示: 使用 -n 参数加载小说文件[/]")

    console.print()
    console.print("[dim]按 Ctrl+C 退出[/]")
    console.print()

    time.sleep(1)
    app.run()


if __name__ == "__main__":
    main()