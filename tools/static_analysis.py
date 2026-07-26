"""Small offline static-analysis verifier used for this submission package."""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def analyze_file(path: Path) -> list[str]:
    """Return a list of static-analysis issues for one Python file."""
    issues: list[str] = []
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()

    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        return [f"{path}: syntax error: {error}"]

    if ast.get_docstring(tree) is None:
        issues.append(f"{path}: missing module docstring")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ast.get_docstring(node) is None:
                issues.append(f"{path}:{node.lineno}: missing docstring for {node.name}")

    for number, line in enumerate(lines, start=1):
        if "\t" in line:
            issues.append(f"{path}:{number}: tab character found")
        if len(line) > 100:
            issues.append(f"{path}:{number}: line too long ({len(line)}/100)")

    return issues


def main() -> int:
    """Analyze the project Python files and print a score."""
    paths = [
        Path("server.py"),
        Path("EmotionDetection/__init__.py"),
        Path("EmotionDetection/emotion_detection.py"),
        Path("test_emotion_detection.py"),
    ]
    issues = [issue for path in paths for issue in analyze_file(path)]

    if issues:
        print("Static analysis issues:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nYour code has been rated at 0.00/10")
        return 1

    print("No syntax, docstring, tab, or line-length issues found.")
    print("Your code has been rated at 10.00/10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
