from typing import TYPE_CHECKING

from sashiko_pat.models import Offsets, Side, Steps

if TYPE_CHECKING:
    from collections.abc import Iterator

    from sashiko_pat.cli import GridConfig

DEFAULT_WIDTH = 50
DEFAULT_HEIGHT = 30

HORIZONTAL_STITCH = "─"
VERTICAL_STITCH = "│"

CROSSING_CHARS: dict[tuple[bool, bool, bool, bool], str] = {
    # 4 stitches
    (True, True, True, True): "┼",
    # 3 stitches
    (False, True, True, True): "┬",
    (True, False, True, True): "┴",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    # 2 stitches
    (True, True, False, False): "│",
    (False, False, True, True): "─",
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    # 1 stitch
    (True, False, False, False): " ",
    (False, True, False, False): " ",
    (False, False, True, False): " ",
    (False, False, False, True): " ",
    # 0 stitches
    (False, False, False, False): " ",
}


def get_crossing_char(*, up: bool, down: bool, left: bool, right: bool) -> str:
    return CROSSING_CHARS.get((up, down, left, right), " ")


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

    all_h_stitches = [
        generate_stitch_line(config.x.steps, x_offsets[r], width)
        for r in range(height + 1)
    ]
    col_vertical_stitches: list[list[Side]] = [
        generate_stitch_line(config.y.steps, y_offsets[c], height)
        for c in range(width + 1)
    ]

    def render_h_line(r: int) -> str:
        chars: list[str] = []
        for c in range(width + 1):
            up = r > 0 and col_vertical_stitches[c][r - 1] is Side.FRONT
            down = r < height and col_vertical_stitches[c][r] is Side.FRONT
            left = c > 0 and all_h_stitches[r][c - 1] is Side.FRONT
            right = c < width and all_h_stitches[r][c] is Side.FRONT
            chars.append(get_crossing_char(up=up, down=down, left=left, right=right))
            if c < width:
                chars.append(
                    HORIZONTAL_STITCH if all_h_stitches[r][c] is Side.FRONT else " "
                )
        return "".join(chars)

    def render_v_line(r: int) -> str:
        chars: list[str] = []
        for c in range(width + 1):
            v_stitch = col_vertical_stitches[c][r]
            chars.append(VERTICAL_STITCH if v_stitch is Side.FRONT else " ")
            if c < width:
                chars.append(" ")
        return "".join(chars)

    lines: list[str] = []
    for r in range(height):
        lines.append(render_h_line(r))
        lines.append(render_v_line(r))

    lines.append(render_h_line(height))

    return "\n".join(lines)
