"""Project state tracking for context-aware workflows"""

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProjectState:
    """Immutable-ish project state for context-aware workflows."""

    project_name: str = "api-server"
    language: str = "python"
    framework: str = "fastapi"
    test_framework: str = "pytest"
    container_runtime: str = "docker"

    # File tracking
    modified_files: list[str] = field(default_factory=list)
    new_files: list[str] = field(default_factory=list)
    deleted_files: list[str] = field(default_factory=list)

    # Git state
    current_branch: str = "main"
    recent_commits: list[str] = field(default_factory=list)

    # Test state
    tests_pass: bool = True
    failing_test: Optional[str] = None

    # Build/deploy state
    build_success: bool = True
    deployment_target: Optional[str] = None

    # Code tracking
    imports: set[str] = field(default_factory=set)
    functions_defined: set[str] = field(default_factory=set)

    def update(self, **kwargs) -> "ProjectState":
        """Return a new state with updates applied (immutable pattern)."""
        return ProjectState(
            **{**self.__dict__, **kwargs}
        )


PROJECT_NAMES = [
    "api-server", "data-pipeline", "ml-training", "web-frontend",
    "auth-service", "user-service", "payment-gateway", "notification-service",
]

LANGUAGES = ["python", "javascript", "typescript", "go", "rust"]

FRAMEWORKS = {
    "python": ["fastapi", "django", "flask", "pytest"],
    "javascript": ["express", "nextjs", "react"],
    "typescript": ["express", "nestjs", "nextjs"],
    "go": ["gin", "fiber"],
    "rust": ["actix", "axum"],
}

TEST_FRAMEWORKS = {
    "python": "pytest",
    "javascript": "jest",
    "typescript": "jest",
    "go": "testing",
    "rust": "cargo test",
}

CONTAINER_RUNTIMES = ["docker", "kubernetes", "none"]


def create_initial_state() -> ProjectState:
    """Create a randomized initial project state."""
    project_name = random.choice(PROJECT_NAMES)
    language = random.choice(LANGUAGES)
    framework = random.choice(FRAMEWORKS.get(language, ["fastapi"]))
    test_framework = TEST_FRAMEWORKS.get(language, "pytest")
    container_runtime = random.choice(CONTAINER_RUNTIMES)
    current_branch = random.choice(["main", "develop", "feature/auth", "fix/bug"])

    # Generate some initial recent commits
    commit_templates = [
        "feat: add user authentication flow",
        "fix: resolve memory leak in worker",
        "refactor: simplify API endpoints",
        "docs: update README and API docs",
        "test: add unit tests for auth module",
        "chore: update dependencies",
        "perf: optimize database queries",
        "feat: implement rate limiting",
    ]
    recent_commits = random.sample(commit_templates, k=min(3, len(commit_templates)))

    # Generate initial files based on project
    base_files = ["main.py", "config.py", "requirements.txt", "README.md"]
    src_files = ["models.py", "views.py", "database.py", "middleware.py"]
    all_files = [f"src/{f}" for f in src_files] + base_files

    return ProjectState(
        project_name=project_name,
        language=language,
        framework=framework,
        test_framework=test_framework,
        container_runtime=container_runtime,
        current_branch=current_branch,
        recent_commits=recent_commits,
        modified_files=random.sample(all_files, k=random.randint(1, 3)),
        new_files=[],
        deleted_files=[],
        tests_pass=True,
        failing_test=None,
        build_success=True,
        deployment_target=None,
        imports=set(),
        functions_defined=set(),
    )