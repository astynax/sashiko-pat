import pytest

from sashiko_pat import (
    DEFAULT_HEIGHT,
    DEFAULT_WIDTH,
    AxisConfig,
    GridConfig,
    Offsets,
    Side,
    Steps,
    render_grid,
)
from sashiko_pat.render import (
    compute_cumulative_offsets,
    generate_stitch_line,
    skip,
)


def test_skip_zero() -> None:
    it = iter([1, 2, 3])
    res = skip(it, 0)
    assert res is it
    assert list(it) == [1, 2, 3]


def test_skip_positive() -> None:
    it = iter([10, 20, 30, 40, 50])
    res = skip(it, 2)
    assert res is it
    assert list(it) == [30, 40, 50]


def test_skip_more_than_length() -> None:
    it = iter([1, 2])
    skip(it, 5)
    assert list(it) == []


def test_skip_negative() -> None:
    it = iter([1, 2])
    with pytest.raises(ValueError, match="count must be non-negative"):
        skip(it, -1)


def test_generate_stitch_line_steps_1() -> None:
    steps = Steps.parse("1")
    result = generate_stitch_line(steps, offset=0, length=5)
    assert result == [
        Side.FRONT,
        Side.BACK,
        Side.FRONT,
        Side.BACK,
        Side.FRONT,
    ]


def test_generate_stitch_line_steps_12() -> None:
    steps = Steps.parse("12")
    result = generate_stitch_line(steps, offset=0, length=6)
    assert result == [
        Side.FRONT,
        Side.BACK,
        Side.BACK,
        Side.FRONT,
        Side.BACK,
        Side.BACK,
    ]


def test_generate_stitch_line_steps_213() -> None:
    steps = Steps.parse("213")
    result = generate_stitch_line(steps, offset=0, length=8)
    assert result == [
        Side.FRONT,
        Side.FRONT,
        Side.BACK,
        Side.FRONT,
        Side.FRONT,
        Side.FRONT,
        Side.BACK,
        Side.FRONT,
    ]


def test_generate_stitch_line_with_offset() -> None:
    steps = Steps.parse("12")
    # offset 1 skips first front stitch, starting at back
    result = generate_stitch_line(steps, offset=1, length=5)
    assert result == [
        Side.BACK,
        Side.BACK,
        Side.FRONT,
        Side.BACK,
        Side.BACK,
    ]

    # offset 2 skips front and back, cycling back to front
    result_offset_2 = generate_stitch_line(steps, offset=2, length=4)
    assert result_offset_2 == [
        Side.FRONT,
        Side.BACK,
        Side.BACK,
        Side.FRONT,
    ]


def test_generate_stitch_line_zero_length() -> None:
    steps = Steps.parse("1")
    assert generate_stitch_line(steps, offset=0, length=0) == []
    assert generate_stitch_line(steps, offset=0, length=-5) == []


def test_compute_cumulative_offsets() -> None:
    assert compute_cumulative_offsets(Offsets.parse("0"), 0) == []
    assert compute_cumulative_offsets(Offsets.parse("0"), 1) == [0]
    assert compute_cumulative_offsets(Offsets.parse("0"), 4) == [0, 0, 0, 0]
    assert compute_cumulative_offsets(Offsets.parse("1"), 4) == [0, 1, 2, 3]
    assert compute_cumulative_offsets(Offsets.parse("120"), 7) == [
        0,
        1,
        3,
        3,
        4,
        6,
        6,
    ]


def test_render_grid_invalid_dimensions() -> None:
    config = GridConfig.default()
    with pytest.raises(ValueError, match="width and height must be non-negative"):
        render_grid(config, width=-1, height=5)
    with pytest.raises(ValueError, match="width and height must be non-negative"):
        render_grid(config, width=5, height=-1)


def test_render_grid_small_default_pattern() -> None:
    config = GridConfig(
        x=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("0")),
        y=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("0")),
    )
    rendered = render_grid(config, width=3, height=2)
    expected = "┌─┐ ┌─┐\n│ │ │ │\n└─┘ └─┘\n       \n ─   ─ "
    assert rendered == expected


def test_render_grid_horizontal_spacing_steps_12() -> None:
    config = GridConfig(
        x=AxisConfig(steps=Steps.parse("12"), offsets=Offsets.parse("0")),
        y=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("0")),
    )
    rendered = render_grid(config, width=4, height=1)
    expected = "┌─┐   ┌─┐\n│ │ │ │ │\n└─┘   └─┘"
    assert rendered == expected


def test_render_grid_row_offsets() -> None:
    config = GridConfig(
        x=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("1")),
        y=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("0")),
    )
    rendered = render_grid(config, width=3, height=2)
    expected = "┌─┐ ┌─┐\n│ │ │ │\n  └─┘  \n       \n ─   ─ "
    assert rendered == expected


def test_render_grid_column_offsets() -> None:
    config = GridConfig(
        x=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("0")),
        y=AxisConfig(steps=Steps.parse("1"), offsets=Offsets.parse("1")),
    )
    rendered = render_grid(config, width=3, height=2)
    expected = "┌─  ┌─ \n│   │  \n└─┐ └─┐\n  │   │\n ─┘  ─┘"
    assert rendered == expected


def test_render_grid_zero_dimensions() -> None:
    config = GridConfig.default()
    assert render_grid(config, width=0, height=0) == " "
    assert render_grid(config, width=0, height=2) == " \n│\n \n \n "
    assert render_grid(config, width=2, height=0) == " ─   "


def test_render_grid_4way_crossings_and_tees() -> None:
    config = GridConfig(
        x=AxisConfig(steps=Steps.parse("2"), offsets=Offsets.parse("0")),
        y=AxisConfig(steps=Steps.parse("2"), offsets=Offsets.parse("0")),
    )
    rendered = render_grid(config, width=2, height=2)
    expected = "┌─┬─┐\n│ │ │\n├─┼─┤\n│ │ │\n└─┴─┘"
    assert rendered == expected


def test_render_grid_default_dimensions_line_counts_and_lengths() -> None:
    config = GridConfig.default()
    rendered = render_grid(config)
    lines = rendered.split("\n")
    assert len(lines) == 2 * DEFAULT_HEIGHT + 1
    for line in lines:
        assert len(line) == 2 * DEFAULT_WIDTH + 1
