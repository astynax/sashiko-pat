from itertools import islice

import pytest

from sashiko_pat import Offsets, Side, Steps


def test_side_enum() -> None:
    assert Side.FRONT != Side.BACK
    assert set(Side) == {Side.FRONT, Side.BACK}


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("", [(1, Side.FRONT), (1, Side.BACK)]),
        ("   ", [(1, Side.FRONT), (1, Side.BACK)]),
        ("1", [(1, Side.FRONT), (1, Side.BACK)]),
        ("2", [(2, Side.FRONT), (1, Side.BACK)]),
        ("3", [(3, Side.FRONT), (1, Side.BACK)]),
        ("12", [(1, Side.FRONT), (2, Side.BACK)]),
        (
            "213",
            [
                (2, Side.FRONT),
                (1, Side.BACK),
                (3, Side.FRONT),
                (1, Side.BACK),
            ],
        ),
        (
            "3211",
            [
                (3, Side.FRONT),
                (2, Side.BACK),
                (1, Side.FRONT),
                (1, Side.BACK),
            ],
        ),
        ("  21  ", [(2, Side.FRONT), (1, Side.BACK)]),
    ],
)
def test_steps_parse_valid(raw: str, expected: list[tuple[int, Side]]) -> None:
    steps = Steps.parse(raw)
    assert list(islice(steps, len(expected))) == expected
    assert steps.items == tuple(expected)


@pytest.mark.parametrize(
    "raw",
    [
        "0",
        "4",
        "abc",
        "-1",
        "1 2",
        "1.5",
        "10",
    ],
)
def test_steps_parse_invalid(raw: str) -> None:
    with pytest.raises(ValueError, match="Invalid character"):
        Steps.parse(raw)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("", [0]),
        ("   ", [0]),
        ("0", [0]),
        ("1", [1]),
        ("2", [2]),
        ("3", [3]),
        ("0123", [0, 1, 2, 3]),
        ("3210", [3, 2, 1, 0]),
        ("  120  ", [1, 2, 0]),
    ],
)
def test_offsets_parse_valid(raw: str, expected: list[int]) -> None:
    offsets = Offsets.parse(raw)
    assert list(islice(offsets, len(expected))) == expected
    assert offsets.items == tuple(expected)


@pytest.mark.parametrize(
    "raw",
    [
        "4",
        "abc",
        "-1",
        "0 1",
        "0.5",
        "9",
    ],
)
def test_offsets_parse_invalid(raw: str) -> None:
    with pytest.raises(ValueError, match="Invalid character"):
        Offsets.parse(raw)


def test_models_iteration_infinite() -> None:
    steps = Steps.parse("12")
    assert list(islice(steps, 6)) == [
        (1, Side.FRONT),
        (2, Side.BACK),
        (1, Side.FRONT),
        (2, Side.BACK),
        (1, Side.FRONT),
        (2, Side.BACK),
    ]

    offsets = Offsets.parse("012")
    assert list(islice(offsets, 7)) == [0, 1, 2, 0, 1, 2, 0]
