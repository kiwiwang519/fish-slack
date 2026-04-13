# 🐟 Fish Slack

**在终端里光明正大地摸鱼**

当老板走过来时,快速切换界面,让所有人以为你全神贯注在写代码。

## ✨ 特性

- 📖 **导入任意小说** - 支持任何 `.txt` 文件
- 🎭 **多种伪装格式** - 代码、JSON日志、CSV日志、错误日志
- ⚡ **一键切换** - 摸鱼模式 ↔ 工作模式,无缝切换
- 🤖 **自动表演** - 模拟 Claude Code 工作输出,栩栩如生
- 🔄 **自动循环** - 小说读完自动从头再来

## 🎬 效果预览

### 摸鱼模式 (小说隐藏在代码中)

```
┌─Output Log - 代码样式───
│ ### File: novel_574.txt ###
    4 │ 李明站在山巅,俯瞰着脚下的云海
    5 │
    6 │ "师父,我一定会找到那本秘籍的!"
╰─
```

### 工作模式 (看起来像真的在写代码)

```
╭─ Fish Slack ────────────────────────────────────────────
│  专注工作
╰─

➜ You — optimize the authentication module

Thinking...
    Reviewing security implications of the changes
        → Analyzing token-based auth patterns
        → Checking JWT implementation details
Thinking...
    Refactoring the middleware layer
```

## 🚀 快速开始

### 安装

```bash
# 从 GitHub 安装 (推荐)
pip install git+https://github.com/kiwiwang519/fish-slack.git

# 或者手动克隆安装
git clone https://github.com/kiwiwang519/fish-slack.git
cd fish-slack
pip install .
```

### 运行

```bash
# 加载小说 (默认代码格式)
python -m fish_slack -n ~/novel.txt

# JSON日志格式
python -m fish_slack -n ~/novel.txt --format json

# CSV日志格式
python -m fish_slack -n ~/novel.txt --format csv

# 错误日志格式
python -m fish_slack -n ~/novel.txt --format error
```

> **注意**: 本工具暂未发布到 PyPI,需要通过 GitHub 安装。

### 快捷键

| 按键 | 功能 |
|------|------|
| `W` | 切换到工作模式 |
| `F` | 切换到摸鱼模式 |
| `Q` | 退出 |

## 🎨 伪装格式

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| `code` | 伪装成代码文件 | 大部分情况 |
| `json` | 伪装成JSON日志 | 看起来像服务日志 |
| `csv` | 伪装成CSV数据 | 看起来像数据分析 |
| `error` | 伪装成错误日志 | 看起来像在debug |

## 🛠️ 工作原理

Fish Slack 在后台自动生成各种真实的 Claude Code 操作:

- 💭 **Thinking** - 思考过程分析
- 🤖 **Agent** - 任务执行输出
- 🔧 **Tool Calls** - Bash/Grep/Read 等工具调用
- 📝 **File Ops** - 文件操作记录
- 📊 **Progress** - 进度条显示

配合隐藏的小说内容,让摸鱼变得专业。

## 📄 License

MIT

---

**警告**: 使用本工具进行摸鱼导致的一切后果由用户自行承担。请合理安排工作与休息。
