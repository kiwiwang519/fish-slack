"""Realistic pytest outputs with pass/fail states"""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fish_slack.state import ProjectState

from fish_slack.outputs.base import OutputFormatter


class PytestOutputFormatter(OutputFormatter):
    """Realistic pytest outputs."""

    TEST_NAMES_PASS = [
        "tests/test_api.py::test_endpoint",
        "tests/test_api.py::test_validation",
        "tests/test_api.py::test_authentication",
        "tests/test_models.py::test_user_creation",
        "tests/test_models.py::test_user_update",
        "tests/test_views.py::test_homepage",
        "tests/test_views.py::test_404",
        "tests/test_middleware.py::test_cors",
        "tests/test_database.py::test_connection",
        "tests/test_database.py::test_query",
        "tests/test_auth.py::test_login",
        "tests/test_auth.py::test_logout",
        "tests/test_auth.py::test_token_refresh",
        "tests/test_config.py::test_defaults",
        "tests/test_config.py::test_env_override",
    ]

    def can_handle(self, tool: str, command: str) -> bool:
        return tool == "Bash" and ("pytest" in command or "python -m pytest" in command)

    def format(self, state: "ProjectState", **kwargs) -> list[str]:
        if state.tests_pass:
            return self._format_pass()
        else:
            return self._format_fail(state)

    def _format_pass(self) -> list[str]:
        lines = [
            "============================= test session starts ==============================",
            "platform darwin -- Python 3.11.4, pytest-7.4.0",
            "rootdir: /Users/dev/projects/api-server",
            "collected 15 items",
            "",
        ]

        passed_tests = random.sample(self.TEST_NAMES_PASS, k=min(15, len(self.TEST_NAMES_PASS)))
        for i, test in enumerate(passed_tests, 1):
            pct = int(i / len(passed_tests) * 100)
            lines.append(f"{test} PASSED                              [{pct:3d}%]")

        lines.extend([
            "",
            "============================= 15 passed in 3.45s ==============================",
        ])

        return lines

    def _format_fail(self, state: "ProjectState") -> list[str]:
        failing_test = state.failing_test or "test_api_endpoint"

        lines = [
            "============================= test session starts ==============================",
            "platform darwin -- Python 3.11.4, pytest-7.4.0",
            "rootdir: /Users/dev/projects/api-server",
            "collected 15 items",
            "",
        ]

        # Some pass, some fail
        test_results = [
            ("tests/test_api.py::test_endpoint", False),
            ("tests/test_api.py::test_validation", False),
            ("tests/test_api.py::test_authentication", True),
            ("tests/test_models.py::test_user_creation", True),
            ("tests/test_models.py::test_user_update", True),
            ("tests/test_views.py::test_homepage", True),
            ("tests/test_views.py::test_404", True),
            ("tests/test_middleware.py::test_cors", True),
            ("tests/test_database.py::test_connection", True),
            ("tests/test_database.py::test_query", True),
            ("tests/test_auth.py::test_login", True),
            ("tests/test_auth.py::test_logout", True),
            ("tests/test_auth.py::test_token_refresh", True),
            ("tests/test_config.py::test_defaults", True),
            ("tests/test_config.py::test_env_override", True),
        ]

        for i, (test, passed) in enumerate(test_results, 1):
            pct = int(i / len(test_results) * 100)
            if passed:
                lines.append(f"{test} PASSED                              [{pct:3d}%]")
            else:
                lines.append(f"{test} FAILED                              [{pct:3d}%]")

        lines.extend([
            "",
            "",
            "=========================== FAILURES =======================================",
            f"_______________________ {failing_test} ________________________",
            "",
            f"    def {failing_test}():",
            f"> response = client.get('/api/v1/users')",
            f"E       AssertionError: assert 404 == 200",
            "",
            f"tests/test_api.py:45: AssertionError",
            "",
            "",
            f"========================= 2 failed, 13 passed in 4.21s ===================",
        ])

        return lines