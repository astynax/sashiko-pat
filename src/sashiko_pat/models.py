from dataclasses import dataclass
from enum import Enum, auto
from itertools import cycle
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Iterator


class Side(Enum):
    FRONT = auto()
    BACK = auto()


@dataclass(frozen=True)
class Steps:
    items: tuple[tuple[int, Side], ...]

    @classmethod
    def parse(cls, raw: str) -> Self:
        cleaned = raw.strip()
        if not cleaned:
            cleaned = "1"

        valid_chars = {"1", "2", "3"}
        for char in cleaned:
            if char not in valid_chars:
                msg = (
                    f"Invalid character '{char}' in steps: "
                    "only digits 1, 2, and 3 are allowed."
                )
                raise ValueError(msg)

        parsed: list[tuple[int, Side]] = []
        for index, char in enumerate(cleaned):
            side = Side.FRONT if index % 2 == 0 else Side.BACK
            parsed.append((int(char), side))

        if len(parsed) % 2 != 0:
            parsed.append((1, Side.BACK))

        return cls(tuple(parsed))

    def __iter__(self) -> Iterator[tuple[int, Side]]:
        return cycle(self.items)


@dataclass(frozen=True)
class Offsets:
    items: tuple[int, ...]

    @classmethod
    def parse(cls, raw: str) -> Self:
        cleaned = raw.strip()
        if not cleaned:
            return cls((0,))

        valid_chars = {"0", "1", "2", "3"}
        for char in cleaned:
            if char not in valid_chars:
                msg = (
                    f"Invalid character '{char}' in offsets: "
                    "only digits 0, 1, 2, and 3 are allowed."
                )
                raise ValueError(msg)

        return cls(tuple(int(char) for char in cleaned))

    def __iter__(self) -> Iterator[int]:
        return cycle(self.items)
