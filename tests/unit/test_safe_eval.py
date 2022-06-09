from typing import Final

from hamcrest import assert_that, equal_to

from aiotense.service_layer import safe_eval

CONSTANT: Final[float] = 3.14


def test_eval_basics() -> None:
    exp = "2 + 2 * 2"
    assert_that(safe_eval.SafelyExpEvalute(exp).safe_evalute(), equal_to(6))


def test_eval_flexibility() -> None:
    deps = {"minute": 60}
    exp = "minute * 60"
    assert_that(
        safe_eval.SafelyExpEvalute(exp, eval_locals=deps).safe_evalute(), equal_to(3600)
    )


def test_eval_safety() -> None:
    safe_eval.SafelyExpEvalute("globals().pop('CONSTANT')")
    assert "CONSTANT" in globals()
