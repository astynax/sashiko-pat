import sys

from sashiko_pat.cli import AxisConfig, GridConfig, prompt_param, run_interactive_loop
from sashiko_pat.models import Offsets, Side, Steps

__all__ = [
    "AxisConfig",
    "GridConfig",
    "Offsets",
    "Side",
    "Steps",
    "main",
    "prompt_param",
    "run_interactive_loop",
]


def main() -> None:
    try:
        run_interactive_loop()
    except KeyboardInterrupt:
        sys.exit(1)
