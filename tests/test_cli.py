import pytest

from sashiko_pat import (
    AxisConfig,
    GridConfig,
    Offsets,
    Side,
    Steps,
    main,
    prompt_param,
    run_interactive_loop,
)


def test_axis_config_defaults() -> None:
    axis = AxisConfig()
    assert axis.steps_raw == "1"
    assert axis.steps == Steps.parse("1")
    assert axis.offsets_raw == "0"
    assert axis.offsets == Offsets.parse("0")


def test_grid_config_defaults() -> None:
    grid = GridConfig.default()
    assert grid.x.steps_raw == "1"
    assert grid.x.offsets_raw == "0"
    assert grid.y.steps_raw == "1"
    assert grid.y.offsets_raw == "0"


def test_prompt_param_default() -> None:
    prompts: list[str] = []

    def mock_input(prompt: str) -> str:
        prompts.append(prompt)
        return ""

    raw, parsed = prompt_param("X steps", "1", Steps.parse, mock_input)
    assert raw == "1"
    assert parsed == Steps.parse("1")
    assert prompts == ["X steps [1]: "]


def test_prompt_param_whitespace_uses_default() -> None:
    raw, parsed = prompt_param("X steps", "21", Steps.parse, lambda _: "   ")
    assert raw == "21"
    assert parsed == Steps.parse("21")


def test_prompt_param_custom_value() -> None:
    raw, parsed = prompt_param("X steps", "1", Steps.parse, lambda _: "213")
    assert raw == "213"
    assert parsed.items == (
        (2, Side.FRONT),
        (1, Side.BACK),
        (3, Side.FRONT),
        (1, Side.BACK),
    )


def test_prompt_param_retry_on_invalid_input() -> None:
    inputs = ["invalid", "4", "23"]
    printed: list[str] = []
    prompts: list[str] = []
    expected_attempts = 3
    expected_failures = 2

    def mock_input(prompt: str) -> str:
        prompts.append(prompt)
        return inputs.pop(0)

    raw, parsed = prompt_param(
        "X steps",
        "1",
        Steps.parse,
        mock_input,
        printed.append,
    )
    assert raw == "23"
    assert parsed == Steps.parse("23")
    assert len(prompts) == expected_attempts
    assert all(p == "X steps [1]: " for p in prompts)
    assert len(printed) == expected_failures
    assert "Invalid character 'i' in steps" in printed[0]
    assert "Invalid character '4' in steps" in printed[1]


def test_run_interactive_loop_single_cycle() -> None:
    inputs = ["21", "10", "3", "2"]
    prompts: list[str] = []
    prints: list[str] = []

    def mock_input(prompt: str) -> str:
        if not inputs:
            raise StopIteration
        prompts.append(prompt)
        return inputs.pop(0)

    config = GridConfig.default()
    with pytest.raises(StopIteration):
        run_interactive_loop(config, mock_input, prints.append)

    assert prompts == [
        "X steps [1]: ",
        "X offsets [0]: ",
        "Y steps [1]: ",
        "Y offsets [0]: ",
    ]
    assert prints == ["TODO"]
    assert config.x.steps_raw == "21"
    assert config.x.steps == Steps.parse("21")
    assert config.x.offsets_raw == "10"
    assert config.x.offsets == Offsets.parse("10")
    assert config.y.steps_raw == "3"
    assert config.y.steps == Steps.parse("3")
    assert config.y.offsets_raw == "2"
    assert config.y.offsets == Offsets.parse("2")


def test_run_interactive_loop_preserves_values_across_cycles() -> None:
    # Cycle 1: Enter custom values for X steps ("32") and Y offsets ("1")
    # Cycle 2: Hit Enter for all (empty inputs) -> should keep cycle 1 values
    inputs = ["32", "", "", "1", "", "", "", ""]
    prompts: list[str] = []
    prints: list[str] = []

    def mock_input(prompt: str) -> str:
        if not inputs:
            raise StopIteration
        prompts.append(prompt)
        return inputs.pop(0)

    config = GridConfig.default()
    with pytest.raises(StopIteration):
        run_interactive_loop(config, mock_input, prints.append)

    assert prints == ["TODO", "TODO"]
    assert prompts == [
        # Cycle 1 prompts
        "X steps [1]: ",
        "X offsets [0]: ",
        "Y steps [1]: ",
        "Y offsets [0]: ",
        # Cycle 2 prompts (with updated defaults)
        "X steps [32]: ",
        "X offsets [0]: ",
        "Y steps [1]: ",
        "Y offsets [1]: ",
    ]
    assert config.x.steps_raw == "32"
    assert config.x.steps == Steps.parse("32")
    assert config.y.offsets_raw == "1"
    assert config.y.offsets == Offsets.parse("1")


def test_main_keyboard_interrupt_exit_code_1(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_run_loop() -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("sashiko_pat.run_interactive_loop", mock_run_loop)

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
