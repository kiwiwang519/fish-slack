"""Realistic Python compiler and traceback outputs"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


class PythonOutputFormatter(OutputFormatter):
    """Realistic Python error/traceback outputs."""

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and ("python" in command or "python3" in command)

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        command = kwargs.get("command", "")

        if "python" in command and ("SyntaxError" in command or "syntax" in command.lower()):
            return self._format_syntax_error()
        elif "python" in command and ("ImportError" in command or "ModuleNotFoundError" in command):
            return self._format_import_error()
        elif "python" in command and ("TypeError" in command or "type error" in command.lower()):
            return self._format_type_error()
        elif "python" in command and ("Traceback" in command or "error" in command.lower()):
            return self._format_traceback()
        else:
            return self._format_generic()

    def _format_syntax_error(self) -> list[str]:
        return [
            "  File \"/Users/dev/projects/api-server/src/models.py\", line 23",
            "    def get_users(]",
            "                  ^",
            "SyntaxError: invalid syntax",
        ]

    def _format_import_error(self) -> list[str]:
        return [
            "Traceback (most recent call last):",
            "  File \"/Users/dev/projects/api-server/src/api.py\", line 3, in <module>",
            "    from fastapi import FastAPI, HTTPException",
            "ModuleNotFoundError: No module named 'fastapi'",
        ]

    def _format_type_error(self) -> list[str]:
        return [
            "Traceback (most recent call last):",
            "  File \"/Users/dev/projects/api-server/src/views.py\", line 45, in get_user",
            "    return jsonify(user.to_dict())",
            "AttributeError: 'NoneType' object has no attribute 'to_dict'",
        ]

    def _format_traceback(self) -> list[str]:
        lines = [
            "Traceback (most recent call last):",
            "  File \"/Users/dev/projects/api-server/src/handlers.py\", line 67, in process_request",
            "    data = parse_json(body)",
            "",
            "  File \"/Users/dev/projects/api-server/src/utils.py\", line 23, in parse_json",
            "    return json.loads(body)",
            "",
            "  File \"/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/__init__.py\", line 341, in loads",
            "    return _default_decoder.decode(s)",
            "",
            "  File \"/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/__init__.py\", line 125, in JSONDecodeError",
            "    raise JSONDecodeError(\"Expecting value\", s, err.value) from None",
            "json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
        ]

        return lines

    def _format_generic(self) -> list[str]:
        return [
            "Python 3.11.4",
            'Type "help", "copyright", "credits" or "license" for more information.',
        ]