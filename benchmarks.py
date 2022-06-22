from __future__ import annotations

import copy
import inspect
import logging
import timeit
from typing import TYPE_CHECKING, Callable, Final, TypeVar

from tense import TenseParser, model, resolvers
from tense.adapters import repository

if TYPE_CHECKING:
    _BT = TypeVar("_BT", bound=Callable[..., None])  # Benchmark Type

logging.basicConfig()
_BENCHMARK: logging.Logger = logging.getLogger(__file__)
_BENCHMARK.setLevel(logging.INFO)

_BASIC_UNRESOLVED_STR1: Final[str] = "1 day 2 seconds"
_BASIC_UNRESOLVED_STR2: Final[str] = "1day 2seconds"

_COMPLEX_UNRESOLVED_STR: Final[str] = "1day and 2minutes + 5 seconds"

_TENSE = model.Tense.from_repository(repository.TenseRepository())
_BASIC_TENSE_DIGIT_PARSER = TenseParser(TenseParser.DIGIT, iteration_speedup=True)
_SMART_TENSE_DIGIT_PARSER = TenseParser(
    TenseParser.DIGIT,
    iteration_speedup=True,
    time_resolver=resolvers.smart_resolver,
)


def benchmark(*, number: int) -> Callable[[_BT], _BT]:
    def _code(_str: str) -> str:  # type: ignore[return]
        for substr in (lst := _str.split("\n")):
            if "def" not in substr:
                continue
            return "\n".join(
                map(
                    str.strip,
                    lst[lst.index(substr) + 1 :],
                )
            )

    def inner(fn: _BT) -> _BT:
        _BENCHMARK.info(f"Running benchmark for {fn.__name__} {number:,} times.")
        _time = timeit.timeit(
            stmt=_code(inspect.getsource(fn)),
            number=number,
            globals=copy.copy(globals()),
        )
        _BENCHMARK.info(f"The benchmark ({number:,} times) for foo took {_time:.8f}µs.")
        return fn

    return inner


@benchmark(number=1)
def basic_resolver_one_time1() -> None:
    resolvers.basic_resolver(_BASIC_UNRESOLVED_STR1, _TENSE)


@benchmark(number=1)
def basic_resolver_one_time2() -> None:
    resolvers.basic_resolver(_BASIC_UNRESOLVED_STR2, _TENSE)


@benchmark(number=1_000_000)
def basic_resolver_1million_times1() -> None:
    resolvers.basic_resolver(_BASIC_UNRESOLVED_STR1, _TENSE)


@benchmark(number=1_000_000)
def basic_resolver_1million_times2() -> None:
    resolvers.basic_resolver(_BASIC_UNRESOLVED_STR2, _TENSE)


@benchmark(number=1)
def smart_resolver_one_time() -> None:
    resolvers.smart_resolver(_COMPLEX_UNRESOLVED_STR, _TENSE)


@benchmark(number=1_000_000)
def smart_resolver_1million_times() -> None:
    resolvers.smart_resolver(_COMPLEX_UNRESOLVED_STR, _TENSE)


@benchmark(number=1)
def basic_tense_parser_one_time() -> None:
    _BASIC_TENSE_DIGIT_PARSER.parse(_BASIC_UNRESOLVED_STR1)


@benchmark(number=1_000_000)
def basic_tense_parser_1million_times() -> None:
    _BASIC_TENSE_DIGIT_PARSER.parse(_BASIC_UNRESOLVED_STR1)


@benchmark(number=1)
def smart_tense_parser_one_time() -> None:
    _SMART_TENSE_DIGIT_PARSER.parse(_COMPLEX_UNRESOLVED_STR)


@benchmark(number=1_000_000)
def smart_tense_parser_1million_times() -> None:
    _SMART_TENSE_DIGIT_PARSER.parse(_COMPLEX_UNRESOLVED_STR)
