from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sashiko_pat.models import Offsets, Steps
from sashiko_pat.render import render_grid

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass
class AxisConfig:
    steps_raw: str = "1"
    steps: Steps = field(default_factory=lambda: Steps.parse("1"))
    offsets_raw: str = "0"
    offsets: Offsets = field(default_factory=lambda: Offsets.parse("0"))


@dataclass
class GridConfig:
    x: AxisConfig = field(default_factory=AxisConfig)
    y: AxisConfig = field(default_factory=AxisConfig)

    @classmethod
    def default(cls) -> GridConfig:
        return cls(x=AxisConfig(), y=AxisConfig())


def prompt_param[T](
    label: str,
    current_raw: str,
    parser: Callable[[str], T],
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> tuple[str, T]:
    while True:
        raw = input_func(f"{label} [{current_raw}]: ")
        cleaned = raw.strip()
        if not cleaned:
            return current_raw, parser(current_raw)
        try:
            parsed = parser(cleaned)
        except ValueError as err:
            print_func(str(err))
        else:
            return cleaned, parsed


def run_interactive_loop(
    config: GridConfig | None = None,
    input_func: Callable[[str], str] = input,
    print_func: Callable[[str], None] = print,
) -> None:
    cfg = config if config is not None else GridConfig.default()
    while True:
        cfg.x.steps_raw, cfg.x.steps = prompt_param(
            "X steps", cfg.x.steps_raw, Steps.parse, input_func, print_func
        )
        cfg.x.offsets_raw, cfg.x.offsets = prompt_param(
            "X offsets", cfg.x.offsets_raw, Offsets.parse, input_func, print_func
        )
        cfg.y.steps_raw, cfg.y.steps = prompt_param(
            "Y steps", cfg.y.steps_raw, Steps.parse, input_func, print_func
        )
        cfg.y.offsets_raw, cfg.y.offsets = prompt_param(
            "Y offsets", cfg.y.offsets_raw, Offsets.parse, input_func, print_func
        )
        print_func(render_grid(cfg))
