from __future__ import annotations

# !!! Note: resolver functions accepts (str, model.Tense) parameters and returns iterator of strings.
from typing import TYPE_CHECKING, Iterator

from tense import TenseParser, resolvers

if TYPE_CHECKING:
    from tense.domain import model

_REVERSED_SECONDS = "seconds"[::-1]
_REVERSED_MINUTE = "minute"[::-1]

# "1 minute10   seconds"
reversed_time_string = "1" + _REVERSED_MINUTE + "10   " + _REVERSED_SECONDS


def reverse_resolver(raw_str: str, _: model.Tense) -> Iterator[str]:
    # Resolves reversed units of time.
    return (
        (w[::-1] if not w.isdigit() else w)
        for w in resolvers.basic_resolver(raw_str, _)
    )


parser = TenseParser(TenseParser.DIGIT, time_resolver=reverse_resolver)
assert parser.parse(reversed_time_string) == 70
