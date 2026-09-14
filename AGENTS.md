# AGENTS.md

Guidelines and architectural principles for AI agents working on **Sashiko-Pat**.

---

## Project Overview

**Sashiko-Pat** is a proof-of-concept (PoC) generator for traditional Japanese Sashiko stitching patterns on a square grid.

The CLI application interactively collects parameters for both grid axes (horizontal and vertical):
- **Steps (`FRONT[BACK[FRONT[...]]]`)**: Sequence of digits (1–3) specifying stitch lengths.
  - `FRONT`: Length of visible stitch on the front side.
  - `BACK`: Length of space/stitch on the reverse side.
  - Repeating behavior: Sequence repeats endlessly across rows/columns. If input ends with `FRONT`, an implicit single `BACK` is inserted between repetitions.
  - Default: Empty input defaults to `"1"` (1 FRONT, 1 BACK).
- **Offsets (`N[N[...]]`)**: Sequence of numbers (0–3) indicating how many steps to advance the step sequence at the start of each subsequent row/column.
  - Repeating behavior: Sequence repeats continuously across successive rows/columns.
  - Default: Empty input defaults to `"0"` (no offset, identical step alignment across all rows).

---

## Architecture & Design Principles

- **Proof of Concept (PoC)**: Prioritize simplicity, readability, and pragmatic code over heavy abstractions.
  - Avoid over-engineering, deep inheritance hierarchies, or excessive generic wrappers.
  - Keep data structures lightweight (e.g., tuples, dataclasses, simple functions, iterators/generators).
- **Zero Runtime Dependencies**:
  - **Strictly use Python built-ins only** at runtime.
  - Do not introduce external runtime packages.
- **Python Version**: Target Python `>= 3.14`.

---

## Development Tools & Workflow

Development dependencies and toolchain:
- **Package Manager / Runner**: `uv`
- **Testing**: `pytest`
- **Linter & Formatter**: `ruff`
- **Type Checker**: `ty`

### Common Commands

- **Code Quality Check (Lint, Format Check, Type Check)**:
  ```bash
  make check
  ```
  *(Runs `ruff format --check`, `ruff check`, and `ty check` via `uv`)*

- **Auto-formatting & Fixes**:
  ```bash
  make format
  ```
  *(Runs `ruff format` and `ruff check --fix --select I,Q`)*

- **Run Tests**:
  ```bash
  uv run pytest
  ```

- **Run Application**:
  ```bash
  uv run sashiko-pat
  ```

---

## Agent Guidelines & Expectations

1. **Keep Code Clean and Typed**:
   - Always verify type annotations with `ty check`.
   - Ensure all files adhere to the strict `ruff` lint rules configured in `pyproject.toml`.
   - Always run `make check` before submitting changes and ensure it passes cleanly.
2. **Implement Focused Tests**:
   - Add unit tests with `pytest` for input parsing, sequence cycling, offset calculations, and grid rendering logic.
3. **Stick to the Domain Model**:
   - Keep pattern generation logic modular and testable without introducing unnecessary frameworks.
