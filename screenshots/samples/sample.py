"""Small synthetic example for the theme screenshots."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    name: str
    passed: bool


def summarize(results: list[Result]) -> str:
    """Keep the useful details easy to scan."""
    passed = sum(result.passed for result in results)
    total = len(results)
    return f"Checks: {passed}/{total}\n"


results = [
    Result("Contrast on selected text", True),
    Result("Visible tabs and pane borders", True),
    Result("Consistent success and error colours", True),
]

print(summarize(results))
