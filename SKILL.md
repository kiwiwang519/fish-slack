# Fish Slack - Claude Code Integration

## Project Overview

Fish Slack is a terminal-based fish-slacking tool that disguises novel reading as Claude Code work. When you import a `.txt` novel file, it displays the content hidden within fake terminal output that looks like an active Claude Code session.

## Usage

### Starting the Tool

```bash
cd ~/fish-slack
poetry install
poetry run fish-slack -n /path/to/novel.txt
```

### Display Modes

1. **Work Mode (Default)** - Full screen fake Claude Code output
2. **Fish Mode (Hidden)** - Novel hidden in disguised format (JSON/CSV/logs)
3. **Focus Mode** - Read the novel with minimal disguise

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `TAB` | Toggle work/fish mode |
| `Q` | Quit |
| `R` | Reset novel to beginning |
| `H` | Hide novel (work-only mode) |
| `S` | Show novel (focus mode) |

## Integration with Claude Code

This project was developed using Claude Code's tools:

- Used `Write` to create source files
- Used `Bash` to set up the project structure
- Used `Glob` to find and organize files

## Key Files

- `src/fake_work.py` - Generates fake Claude Code output
- `src/novel.py` - Novel reading and disguise formatting
- `src/tui.py` - Terminal UI management
- `src/main.py` - Entry point and CLI parsing

## Technology Stack

- **Python 3.10+**
- **Rich** - Terminal formatting and panels
- **Poetry** - Dependency management
