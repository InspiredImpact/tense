import asyncio
from typing import Any

from aiotense import TenseParser
from aiotense.application.ports import converters as abc_converters


class DoubleConverter(abc_converters.AbstractConverter[int]):  # <--|
    async def convert(self, value: Any) -> int:  # <----------------|
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be instance of (int, float).")
        return value * 2


parser = TenseParser(TenseParser.DIGIT, converter=DoubleConverter())
assert asyncio.run(parser.parse("1 minute")) == 120  # 1 minute = 60 seconds, 60*2 = 120.
