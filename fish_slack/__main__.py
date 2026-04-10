#!/usr/bin/env python3
"""Fish Slack - 摸鱼终端工具

伪装成Claude Code工作的终端摸鱼工具。
"""

import argparse
import sys
import time
import random
from pathlib import Path

from rich.console import Console
try:
    from fish_slack.fake_work import FakeWorkGenerator
    from fish_slack.novel import NovelReader
except ImportError:
    from fake_work import FakeWorkGenerator
    from novel import NovelReader

# 配色
CLAUDE_BLUE = "cyan"
CLAUDE_GREEN = "green"
CLAUDE_YELLOW = "yellow"
CLAUDE_DIM = "bright_black"


class FishSlack:
    """摸鱼终端工具"""

    def __init__(self, novel_path: str = None, disguise: str = "code", lines_per_page: int = 15):
        self.console = Console()
        self.novel = NovelReader(novel_path)
        self.disguise = disguise
        self.lines_per_page = lines_per_page

        self.display_mode = "work"  # work | fish | focus
        self.work_gen = FakeWorkGenerator(self.console)
        self.last_mode_change = time.time()

    def import_novel(self, path: str) -> bool:
        """导入小说"""
        if self.novel.load_novel(path):
            self.console.print(f"[green]✓[/] 已加载小说: {path}")
            return True
        else:
            self.console.print(f"[red]✗[/] 无法加载小说: {path}")
            return False

    def _print_header(self):
        """打印头部"""
        mode_names = {
            "work": "[bold]专注工作[/]",
            "fish": "[bold]摸鱼模式[/] (伪装)",
            "focus": "[bold]摸鱼模式[/] (阅读)",
        }

        self.console.print()
        self.console.print(f"[{CLAUDE_BLUE}]╭─[/] [bold cyan]Fish Slack[/][{CLAUDE_BLUE}] ────────────────────────────────────────────[/]")
        self.console.print(f"[{CLAUDE_BLUE}]│[/]  {mode_names.get(self.display_mode, '')}")
        self.console.print(f"[{CLAUDE_BLUE}]╰─[/]")
        self.console.print()

    def _print_work_area(self):
        """打印工作区"""
        self.console.print(f"[{CLAUDE_BLUE}]┌─[/][bold] Terminal Output [/][{CLAUDE_BLUE}]───[/]")
        self.console.print(f"[{CLAUDE_BLUE}]│[/]")

        # 生成假的工作输出
        self.work_gen.print_user_message()
        self.work_gen.print_thinking()
        self.work_gen.print_thinking()

        self.console.print(f"[{CLAUDE_BLUE}]╰─[/]")
        self.console.print()

    def _print_novel_area(self):
        """打印小说区"""
        if self.display_mode == "work":
            return

        lines = self.novel.get_next_lines(self.lines_per_page if self.display_mode == "focus" else 3)
        formatted = self._format_novel(lines)

        if formatted:
            title = f"Output Log - {self.DISGUISE_FORMATS.get(self.disguise, '代码样式')}"
            self.console.print(f"[{CLAUDE_YELLOW}]┌─[/][bold]{title}[/][{CLAUDE_YELLOW}]───[/]")
            self.console.print(f"[{CLAUDE_YELLOW}]│[/] [dim]{formatted}[/]")
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

    def _print_status_bar(self):
        """打印状态栏"""
        novel_status = ""
        if self.novel.novel_path:
            filename = Path(self.novel.novel_path).name
            progress = f"{self.novel.current_pos}/{len(self.novel.content)}"
            novel_status = f"  小说: {filename} [{progress}]"

        self.console.print(f"[{CLAUDE_DIM}]按 W 切换工作 | F 切换摸鱼 | Q 退出{novel_status}[/]")

    def _auto_switch_mode(self):
        """自动切换模式,模拟老板来了"""
        now = time.time()
        if now - self.last_mode_change > random.randint(20, 45):
            if self.display_mode == "fish":
                self.display_mode = "work"
                self.console.clear()
            self.last_mode_change = now

    def run(self):
        """运行"""
        # 自动切换到摸鱼模式
        time.sleep(random.uniform(0.5, 1.5))
        self.display_mode = "fish"
        self.console.clear()

        try:
            while True:
                self._print_header()
                self._print_work_area()
                self._print_novel_area()
                self._print_status_bar()

                # 自动模式切换
                self._auto_switch_mode()

                time.sleep(3)
                self.console.clear()

        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.console.print(f"[red]错误: {e}[/]")

    DISGUISE_FORMATS = {
        "code": "代码样式",
        "json": "JSON日志",
        "csv": "CSV日志",
        "error": "错误日志",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fish Slack - 摸鱼终端工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  fish-slack -n ~/novel.txt       # 加载小说
  fish-slack -n ~/novel.txt --json # 伪装成JSON日志

快捷键:
  W    切换到工作模式
  F    切换到摸鱼模式
  Q    退出
        """
    )

    parser.add_argument('-n', '--novel', type=str, default=None, help='小说文件路径 (.txt)')
    parser.add_argument('-f', '--format', type=str, choices=['code', 'json', 'csv', 'error'], default='code', help='小说伪装格式 (默认: code)')
    parser.add_argument('-l', '--lines', type=int, default=15, help='每页显示行数 (默认: 15)')

    args = parser.parse_args()

    console = Console()
    app = FishSlack(novel_path=args.novel, disguise=args.format, lines_per_page=args.lines)

    console.print()
    console.print("[bold cyan]🐟 Fish Slack - 摸鱼终端[/]")
    console.print("[dim]伪装成Claude Code工作的终端摸鱼工具[/]")
    console.print()

    if args.novel:
        if app.import_novel(args.novel):
            console.print(f"[dim]小说格式: {args.format}[/]")
    else:
        console.print("[yellow]提示: 使用 -n 参数加载小说文件[/]")

    console.print()
    console.print("[dim]按 Ctrl+C 或 Q 退出[/]")
    console.print()

    time.sleep(1)
    app.run()


if __name__ == "__main__":
    main()
