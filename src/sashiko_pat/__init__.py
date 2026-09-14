import sys

from sashiko_pat.cli import AxisConfig, GridConfig, prompt_param, run_interactive_loop
from sashiko_pat.models import Offsets, Side, Steps
from sashiko_pat.render import DEFAULT_HEIGHT, DEFAULT_WIDTH, render_grid

__all__ = [
    "DEFAULT_HEIGHT",
    "DEFAULT_WIDTH",
    "AxisConfig",
    "GridConfig",
    "Offsets",
    "Side",
    "Steps",
    "main",
    "prompt_param",
    "render_grid",
    "run_interactive_loop",
]


def main() -> None:
    try:
        run_interactive_loop()
    except KeyboardInterrupt:
        sys.exit(1)
