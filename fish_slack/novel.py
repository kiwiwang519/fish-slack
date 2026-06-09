"""小说内容管理和渲染"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def convert_gbk_to_utf8(source_path: str, dest_path: str = None) -> str:
    """将 GBK 编码的小说文件转换为 UTF-8

    Args:
        source_path: 源文件路径（GBK 编码）
        dest_path: 目标文件路径，默认为源文件同名+.utf8.txt

    Returns:
        转换后的文件路径
    """
    if dest_path is None:
        source = Path(source_path)
        dest_path = str(source.parent / f"{source.stem}.utf8{source.suffix}")

    result = subprocess.run(
        ['iconv', '-f', 'GBK', '-t', 'UTF-8', source_path],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"iconv 转换失败: {result.stderr}")

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(result.stdout)

    return dest_path


class NovelReader:
    """小说阅读器 - 将小说内容伪装成代码或日志"""

    def __init__(self, novel_path: Optional[str] = None):
        self.novel_path = novel_path
        self.content: list[str] = []
        self.current_pos = 0
        self.lines_per_page = 20

    def load_novel(self, path: str) -> bool:
        """加载小说文件"""
        if not os.path.exists(path):
            return False

        self.novel_path = path
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            self.content = f.readlines()

        self.current_pos = 0
        return True

    def get_next_lines(self, n: int = None) -> list[str]:
        """获取接下来的n行"""
        if n is None:
            n = self.lines_per_page

        start = self.current_pos
        end = min(self.current_pos + n, len(self.content))
        self.current_pos = end

        return self.content[start:end]

    def get_alternating_lines(self, novel_count: int = 2, code_count: int = 1, total_lines: int = 30) -> list[str]:
        """获取交替的小说行和伪装代码行

        Args:
            novel_count: 每次获取的小说行数
            code_count: 每次获取的伪装代码行数
            total_lines: 总共需要的行数

        Returns:
            交替排列的字符串列表
        """
        import random
        result = []
        fake_code_templates = [
            "// TODO: implement feature",
            "const data = await fetch(url);",
            "if (err) { log.error(err); }",
            "return res.json();",
            "app.use(cors());",
            "function process() {",
            "const [state, setState] = useState();",
            "export default App;",
            "import React from 'react';",
            "try { await save(); } catch {}",
            "# git push origin main",
            "npm install --save-dev",
            "docker build -t app .",
            "git commit -m 'fix bug'",
            "pytest -v tests/",
        ]

        while len(result) < total_lines and self.current_pos < len(self.content):
            # 获取小说行
            novel_lines = self.get_next_lines(novel_count)
            result.extend(novel_lines)

            # 添加伪装代码行
            if len(result) < total_lines:
                for _ in range(code_count):
                    fake_code = random.choice(fake_code_templates)
                    result.append(fake_code)

        return result

    def has_more(self) -> bool:
        """是否还有更多内容"""
        return self.current_pos < len(self.content)

    def reset(self):
        """重置阅读位置"""
        self.current_pos = 0

    def format_as_code(self, lines: list[str], filename: str = "chapter.txt") -> str:
        """将小说内容格式化成代码样式

        Args:
            lines: 小说行列表
            filename: 显示的文件名

        Returns:
            格式化后的字符串
        """
        output = [f"### File: {filename} ###"]
        for i, line in enumerate(lines, start=self.current_pos + 1):
            line = line.rstrip('\n\r')
            indent = " " * random.randint(0, 2)
            if line.strip():
                # 在行号前加一点随机空格,让阅读更自然
                output.append(f"{indent}{i:4d} │ {line}")
            else:
                output.append(f"{indent}{i:4d} │")
        return '\n'.join(output)

    def format_as_json(self, lines: list[str]) -> str:
        """将小说内容格式化成JSON日志样式"""
        import json
        import random

        output = []
        for line in lines:
            line = line.rstrip('\n\r')
            entry = {
                "timestamp": f"2024-04-{(random.randint(1, 28)):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z",
                "level": random.choice(["INFO", "DEBUG", "INFO", "INFO"]),
                "msg": line if line.strip() else "(empty line)",
                "logger": f"app.novel_{random.randint(1, 9)}"
            }
            output.append(json.dumps(entry))

        return '\n'.join(output)

    def format_as_csv(self, lines: list[str]) -> str:
        """将小说内容格式化成CSV日志"""
        import random
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["timestamp", "user_id", "action", "detail"])

        for line in lines:
            line = line.rstrip('\n\r')
            timestamp = f"2024-04-{(random.randint(1, 28)):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
            writer.writerow([
                timestamp,
                f"user_{random.randint(100, 999)}",
                "read",
                line if line.strip() else "(empty)"
            ])

        return output.getvalue()

    def format_as_error_log(self, lines: list[str]) -> str:
        """将小说内容格式化成错误日志"""
        import random

        output = []
        for line in lines:
            line = line.rstrip('\n\r')
            if line.strip():
                output.append(f"[ERROR] {line}")
            else:
                output.append(f"[DEBUG] {random.choice(['line empty', 'skip', '---', ''])}")

        return '\n'.join(output)


import random  # 确保random可用
