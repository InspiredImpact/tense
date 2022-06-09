import asyncio
from typing import Any

from hamcrest import assert_that, instance_of, greater_than

from aiotense import TenseParser, from_tense_file, resolvers
from aiotense.application.ports import converters as abc_converters
from ..pyhamcrest import has_attributes

_TENSE_FILEDIR = "tests/e2e/.aiotense"


def test_from_file() -> None:
    assert_that(from_tense_file(_TENSE_FILEDIR), instance_of(dict))


def test_basic_ui() -> None:
    assert_that(TenseParser, has_attributes("DIGIT"))
    assert_that(TenseParser, has_attributes("TIMEDELTA"))

    parser = TenseParser(TenseParser.DIGIT, config=from_tense_file(_TENSE_FILEDIR))
    result = asyncio.run(parser.parse("1 decade"))

    assert_that(result, greater_than(0))


def test_advanced_ui() -> None:
    class DoubleConverter(abc_converters.AbstractConverter[int | float]):
        async def convert(self, value: Any) -> int | float:
            if not isinstance(value, (int, float)):
                return NotImplemented
            return value * 2

    parser = TenseParser(
        TenseParser.DIGIT,
        config=from_tense_file(_TENSE_FILEDIR),
        converter=DoubleConverter(),
        time_resolver=resolvers.smart_resolver,
    )

    result = asyncio.run(parser.parse("1decade and 1decade"))
    assert_that(result, greater_than(0))
