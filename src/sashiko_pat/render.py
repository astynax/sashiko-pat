from typing import TYPE_CHECKING

from sashiko_pat.models import Offsets, Side, Steps

if TYPE_CHECKING:
    from collections.abc import Iterator

    from sashiko_pat.cli import GridConfig

DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 30


def skip[T](iterator: Iterator[T], count: int) -> Iterator[T]:
    if count < 0:
        msg = f"count must be non-negative, got {count}"
        raise ValueError(msg)
    for _ in range(count):
        next(iterator, None)
    return iterator


def generate_stitch_line(steps: Steps, offset: int, length: int) -> list[Side]:
    if length <= 0:
        return []
    it = iter(steps)
    skip(it, offset)
    stitches: list[Side] = []
    while len(stitches) < length:
        step_len, side = next(it)
        stitches.extend([side] * step_len)
    return stitches[:length]


def compute_cumulative_offsets(offsets: Offsets, count: int) -> list[int]:
    if count <= 0:
        return []
    it = iter(offsets)
    result: list[int] = [0]
    total = 0
    for _ in range(count - 1):
        total += next(it)
        result.append(total)
    return result


def render_grid(
    config: GridConfig,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
) -> str:
    if width < 0 or height < 0:
        msg = (
            f"width and height must be non-negative, got width={width}, height={height}"
        )
        raise ValueError(msg)

    x_offsets = compute_cumulative_offsets(config.x.offsets, height + 1)
    y_offsets = compute_cumulative_offsets(config.y.offsets, width + 1)

    col_vertical_stitches: list[list[Side]] = [
        generate_stitch_line(config.y.steps, y_offsets[c], height)
        for c in range(width + 1)
    ]

    lines: list[str] = []
    for r in range(height):
        h_stitches = generate_stitch_line(config.x.steps, x_offsets[r], width)
        h_chars = [" "]
        for s in h_stitches:
            h_chars.append("-" if s is Side.FRONT else " ")
            h_chars.append(" ")
        lines.append("".join(h_chars))

        v_chars: list[str] = []
        for c in range(width):
            v_stitch = col_vertical_stitches[c][r]
            v_chars.append("|" if v_stitch is Side.FRONT else " ")
            v_chars.append(" ")
        last_v_stitch = col_vertical_stitches[width][r]
        v_chars.append("|" if last_v_stitch is Side.FRONT else " ")
        lines.append("".join(v_chars))

    last_h_stitches = generate_stitch_line(config.x.steps, x_offsets[height], width)
    last_h_chars = [" "]
    for s in last_h_stitches:
        last_h_chars.append("-" if s is Side.FRONT else " ")
        last_h_chars.append(" ")
    lines.append("".join(last_h_chars))

    return "\n".join(lines)
