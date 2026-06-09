# 🐟 Fish Slack - 摸鱼神器

**在终端里光明正大地摸鱼看书！**

当老板走过来时，快速切换到工作模式，让所有人以为你全神贯注在写代码。老板一走，按一下空格键就能继续安静地阅读小说。
>>>>>>> f66cc3d (feat: 添加阅读模式 - 交替显示小说和代码，空格键滚动)

---

## 📖 这个工具是干什么的？

Fish Slack 是一个**摸鱼终端工具**，它可以：

1. **显示小说内容** - 让你在电脑前光明正大地看书
2. **伪装成工作界面** - 屏幕看起来像在写代码或调试程序
3. **一键切换模式** - 按键盘就能在"工作"和"阅读"之间切换

简单来说：它是一个**假装在工作、实际上在看小说**的工具。

---

## 🚀 五分钟上手指南（超级详细版）

### 第一步：确保你的电脑有 Python

Fish Slack 需要 Python 3 才能运行。先检查一下：

1. 打开**终端**（Terminal）
   - Mac 用户：按 `Command + 空格`，搜索 "终端" 或 "Terminal"
   - Windows 用户：按 `Win + R`，输入 `cmd`，回车

2. 在终端里输入以下命令，检查 Python 版本：

```bash
python3 --version
```

3. 如果显示类似 `Python 3.8.0` 或更高的版本号（3.8、3.9、3.10、3.11 等），就说明已经安装好了。

4. 如果显示 `command not found` 或报错，说明没安装。请先 [安装 Python](https://www.python.org/downloads/)

---

### 第二步：下载并安装 Fish Slack

**方法 A：复制粘贴命令（推荐）**

在终端里依次输入以下命令，每行回车一次：

```bash
# 1. 克隆（下载）代码到电脑
git clone https://github.com/kiwiwang519/fish-slack.git

# 2. 进入下载的文件夹
cd fish-slack

# 3. 安装依赖
pip install rich
```

**方法 B：如果你已经下载了 ZIP 文件**

1. 把 ZIP 文件解压到任何地方（比如桌面）
2. 打开终端，输入：
```bash
cd ~/Desktop/fish-slack
pip install rich
```

---

### 第三步：准备你的小说文件

1. 把你的小说文本文件（`.txt` 格式）放到一个方便找的地方
2. **重要**：如果文件名有**中文**，确保文件编码是 **UTF-8**（大部分情况默认就是）
3. 如果小说文件是 **GBK 编码**（以前的老文件可能是），Fish Slack 会**自动转换**，不需要你手动处理

---

### 第四步：运行 Fish Slack！

在终端里输入（把路径改成你小说文件的实际路径）：

**Mac / Linux 用户：**
```bash
cd ~/fish-slack
python3 -m fish_slack -n ~/Desktop/我的小说.txt
```

**Windows 用户：**
```bash
cd %USERPROFILE%\fish-slack
python -m fish_slack -n C:\Users\你的用户名\Desktop\我的小说.txt
```

> 💡 **提示**：路径中的 `~` 代表你的用户文件夹（比如 Mac 的 `/Users/你的用户名`）

---

### 第五步：开始摸鱼！

运行后，你会看到屏幕开始滚动显示"工作内容"。

**切换到阅读模式：**

1. 按键盘上的 **R** 键（Reading = 阅读）
2. 屏幕会变成交替显示：2行小说内容 → 1行代码 → 2行小说 → 1行代码...

**继续滚动阅读：**

1. 按键盘上的 **空格键**（就是空格）
2. 每次按空格，屏幕会向下滚动显示更多内容

**切换回工作模式：**

1. 按键盘上的 **W** 键（Working = 工作）
2. 屏幕会变成自动滚动的"工作界面"，伪装成 Claude Code 在写代码

**退出程序：**

1. 按键盘上的 **Q** 键（Quit = 退出）

---

## ⌨️ 快捷键说明

| 按键 | 功能 | 什么情况用 |
|------|------|-----------|
| **W** | 工作模式 | 老板来了！快速切换到工作伪装 |
| **R** | 阅读模式 | 开始安静地阅读小说 |
| **空格** | 向下滚动 | 阅读模式下继续看下一段 |
| **Q** | 退出程序 | 不想用了，关掉它 |

---

## 🎨 切换伪装样式（可选）

Fish Slack 有几种不同的"伪装风格"，可以让你看起来像在不同软件里工作：

```bash
# 默认伪装成 Claude Code
python3 -m fish_slack -n ~/小说.txt

# 伪装成 VS Code 终端
python3 -m fish_slack -n ~/小说.txt -s vscode

# 伪装成 Jupyter Notebook
python3 -m fish_slack -n ~/小说.txt -s jupyter

# 伪装成 MySQL 命令行
python3 -m fish_slack -n ~/小说.txt -s mysql

# 伪装成 Vim 编辑器
python3 -m fish_slack -n ~/小说.txt -s vim
```

---

## 🔧 常见问题

### Q: 运行时显示 `command not found: python3`

**A:** 可能是 Python 没安装或路径不对。试试：
```bash
python --version
```
如果这个能显示版本，用 `python` 代替 `python3`。

---

### Q: 运行时显示 `No module named 'rich'`

**A:** 需要安装依赖。在终端输入：
```bash
pip install rich
```

---

### Q: 小说显示乱码了？

**A:** 大部分情况 Fish Slack 会自动转换 GBK 编码。如果还是乱码，可以用以下命令手动转换：
```bash
# Mac / Linux
iconv -f GBK -t UTF-8 ~/原文件.txt > ~/新文件_utf8.txt

# Windows PowerShell
Get-Content ~/原文件.txt -Encoding Default | Set-Content ~/新文件_utf8.txt -Encoding UTF8
```

---

### Q: 快捷键没反应怎么办？

**A:** 确保终端窗口是焦点（点击一下终端窗口再按快捷键）。有些终端可能不支持，推荐用：
- Mac：终端.app 或 iTerm2
- Windows：Windows Terminal 或 PowerShell
- Linux：GNOME Terminal 或 Terminator

---

## 📁 项目结构

```
fish-slack/
├── fish_slack/          # 主程序代码
│   ├── main.py          # 主程序入口
│   ├── novel.py         # 小说读取和转换
│   ├── fake_work.py     # 模拟工作输出
│   ├── workflows.py     # 工作流引擎
│   ├── disguises.py     # 伪装样式
│   ├── screen_effects.py # 屏幕效果
│   ├── state.py         # 状态管理
│   └── outputs/         # 各种输出模块
├── README.md            # 使用说明（本文件）
├── setup.py             # 安装配置
└── pyproject.toml       # 项目配置
```

---

## 🛠️ 开发者指南

如果你想自己修改代码或贡献：

```bash
# 克隆项目
git clone https://github.com/kiwiwang519/fish-slack.git
cd fish-slack

# 安装开发依赖
pip install -e .

# 运行测试
python3 -m fish_slack -n test_novel.txt
```

---

## ⚠️ 免责声明

- 本工具仅供娱乐和学习使用
- 使用本工具进行摸鱼导致的一切后果由用户自行承担
- 请合理安排工作与休息，不要沉迷摸鱼

---

## 📄 许可证

MIT License - 免费使用，可以随意修改和分享

---

**祝你摸鱼愉快！🐟**