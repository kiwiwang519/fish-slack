"""Workflow engine for context-aware multi-step fake work generation"""

import random
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from fish_slack.state import ProjectState
    from fish_slack.outputs import OutputManager


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


@dataclass
class WorkflowStep:
    """A single step in a workflow."""
    tool: str           # "Bash", "Read", "Edit", "Write"
    command: str        # actual command string
    show_thinking: bool = True
    duration: float = 0.5  # simulated duration in seconds
    can_fail: bool = False
    fail_probability: float = 0.0
    context_updates: dict = field(default_factory=dict)

    def should_fail(self) -> bool:
        return self.can_fail and random.random() < self.fail_probability


@dataclass
class Workflow:
    """A named workflow with steps."""
    name: str
    description: str
    steps: list[WorkflowStep]


# Predefined workflow templates
WORKFLOW_TEMPLATES: dict[str, Workflow] = {}


def _init_workflows():
    """Initialize predefined workflow templates."""

    global WORKFLOW_TEMPLATES

    # Test-driven development: write test -> run test (fail) -> fix -> run test (pass)
    WORKFLOW_TEMPLATES["test_driven_development"] = Workflow(
        name="test_driven_development",
        description="Write test → Run test → Fix → Run test → Pass",
        steps=[
            WorkflowStep(
                tool="Read",
                command="Read: tests/test_api.py",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: tests/test_api.py",
                show_thinking=True,
                duration=0.5,
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest tests/test_api.py",
                show_thinking=True,
                duration=1.0,
                can_fail=True,
                fail_probability=0.8,
                context_updates={"tests_pass": False, "failing_test": "test_new_endpoint"},
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest -v tests/test_api.py::test_new_endpoint",
                show_thinking=True,
                duration=0.8,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/api.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"modified_files": ["src/api.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest tests/test_api.py",
                show_thinking=False,
                duration=1.0,
                context_updates={"tests_pass": True},
            ),
        ],
    )

    # Feature development: read spec -> create file -> edit code -> run tests
    WORKFLOW_TEMPLATES["feature_development"] = Workflow(
        name="feature_development",
        description="Read spec → Create file → Edit code → Test",
        steps=[
            WorkflowStep(
                tool="Read",
                command="Read: SPEC.md",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Write",
                command="Write: src/features/user_auth.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"new_files": ["src/features/user_auth.py"]},
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/api.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"modified_files": ["src/api.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="git diff src/api.py",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest tests/",
                show_thinking=False,
                duration=1.5,
            ),
        ],
    )

    # Bug fix: run tests -> see failure -> analyze -> fix -> verify
    WORKFLOW_TEMPLATES["bug_fix"] = Workflow(
        name="bug_fix",
        description="Run tests → See failure → Analyze → Fix → Verify",
        steps=[
            WorkflowStep(
                tool="Bash",
                command="pytest tests/test_api.py",
                show_thinking=True,
                duration=1.0,
                can_fail=True,
                fail_probability=1.0,
                context_updates={"tests_pass": False, "failing_test": "test_user_update"},
            ),
            WorkflowStep(
                tool="Read",
                command="Read: tests/test_api.py",
                show_thinking=True,
                duration=0.4,
            ),
            WorkflowStep(
                tool="Read",
                command="Read: src/api.py",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/api.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"modified_files": ["src/api.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest tests/test_api.py",
                show_thinking=False,
                duration=1.0,
                context_updates={"tests_pass": True},
            ),
        ],
    )

    # Refactor: review code -> make changes -> test -> commit
    WORKFLOW_TEMPLATES["refactor"] = Workflow(
        name="refactor",
        description="Review code → Make changes → Test → Commit",
        steps=[
            WorkflowStep(
                tool="Bash",
                command="git log --oneline -5",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Read",
                command="Read: src/models.py",
                show_thinking=True,
                duration=0.4,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/models.py",
                show_thinking=True,
                duration=0.6,
                context_updates={"modified_files": ["src/models.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="pytest tests/",
                show_thinking=False,
                duration=1.5,
            ),
            WorkflowStep(
                tool="Bash",
                command="git diff",
                show_thinking=True,
                duration=0.3,
            ),
        ],
    )

    # Docker debug: docker ps -> docker logs -> docker exec -> fix
    WORKFLOW_TEMPLATES["docker_debug"] = Workflow(
        name="docker_debug",
        description="docker ps → logs → exec → fix",
        steps=[
            WorkflowStep(
                tool="Bash",
                command="docker ps",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Bash",
                command="docker logs api-server --tail 20",
                show_thinking=True,
                duration=0.5,
            ),
            WorkflowStep(
                tool="Bash",
                command="docker exec -it api-server /bin/sh",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/config.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"modified_files": ["src/config.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="docker restart api-server",
                show_thinking=False,
                duration=1.0,
            ),
        ],
    )

    # K8s debug: kubectl get pods -> describe -> logs -> fix
    WORKFLOW_TEMPLATES["k8s_debug"] = Workflow(
        name="k8s_debug",
        description="kubectl get pods → describe → logs → fix",
        steps=[
            WorkflowStep(
                tool="Bash",
                command="kubectl get pods",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Bash",
                command="kubectl describe pod api-server-7d8f9c6b5-x2k9p",
                show_thinking=True,
                duration=0.4,
            ),
            WorkflowStep(
                tool="Bash",
                command="kubectl logs api-server-7d8f9c6b5-x2k9p --tail=30",
                show_thinking=True,
                duration=0.5,
            ),
            WorkflowStep(
                tool="Edit",
                command="Edit: src/api.py",
                show_thinking=True,
                duration=0.5,
                context_updates={"modified_files": ["src/api.py"]},
            ),
            WorkflowStep(
                tool="Bash",
                command="kubectl rollout restart deployment/api-server",
                show_thinking=False,
                duration=1.0,
            ),
        ],
    )

    # Commit changes: git status -> diff -> add -> commit
    WORKFLOW_TEMPLATES["commit_changes"] = Workflow(
        name="commit_changes",
        description="git status → diff → add → commit",
        steps=[
            WorkflowStep(
                tool="Bash",
                command="git status",
                show_thinking=True,
                duration=0.3,
            ),
            WorkflowStep(
                tool="Bash",
                command="git diff",
                show_thinking=True,
                duration=0.5,
            ),
            WorkflowStep(
                tool="Bash",
                command="git add .",
                show_thinking=True,
                duration=0.2,
            ),
            WorkflowStep(
                tool="Bash",
                command='git commit -m "fix: resolve race condition in request handler"',
                show_thinking=False,
                duration=0.3,
                context_updates={
                    "modified_files": [],
                    "recent_commits": ["fix: resolve race condition in request handler"],
                },
            ),
        ],
    )


_init_workflows()


class WorkflowSelector:
    """Selects appropriate workflow based on current state."""

    def select(self, state: "ProjectState") -> str:
        """Return name of workflow to run next."""
        # If tests are failing, run bug fix workflow
        if not state.tests_pass and state.failing_test:
            return "bug_fix"

        # If there are uncommitted changes, offer commit workflow
        if state.modified_files:
            return random.choice(["commit_changes", "refactor"])

        # Default to variety
        return random.choice([
            "test_driven_development",
            "feature_development",
            "refactor",
            "docker_debug",
            "k8s_debug",
        ])


class WorkflowEngine:
    """Runs multi-step workflows with context awareness."""

    def __init__(self, state: "ProjectState", output_manager: "OutputManager"):
        self.state = state
        self.output_manager = output_manager
        self.selector = WorkflowSelector()
        self.current_workflow_name: Optional[str] = None

    def run_workflow(self, workflow_name: str) -> tuple[list[dict], "ProjectState"]:
        """Execute a workflow and return the steps with their outputs.

        Returns:
            Tuple of (list of step results, updated state)
        """
        if workflow_name not in WORKFLOW_TEMPLATES:
            return [], self.state

        workflow = WORKFLOW_TEMPLATES[workflow_name]
        self.current_workflow_name = workflow_name
        results = []

        for step in workflow.steps:
            result = {
                "tool": step.tool,
                "command": step.command,
                "show_thinking": step.show_thinking,
                "output": self.output_manager.get_output(step.tool, step.command, self.state),
                "thinking": random.choice(REASONING_TEMPLATES) if step.show_thinking else None,
                "failed": False,
            }

            if step.should_fail():
                result["failed"] = True

            results.append(result)

            # Update state with context updates from step
            if result["failed"]:
                # Apply failure updates if step failed
                for key, value in step.context_updates.items():
                    self.state = self.state.update(**{key: value})
            else:
                # Apply updates if step succeeded
                for key, value in step.context_updates.items():
                    self.state = self.state.update(**{key: value})

        return results, self.state

    def select_and_run(self) -> tuple[list[dict], "ProjectState"]:
        """Select a workflow based on current state and run it."""
        workflow_name = self.selector.select(self.state)
        return self.run_workflow(workflow_name)