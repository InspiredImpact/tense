from typing import Any

from tense import TenseParser
from tense.application.ports import converters as abc_converters


class DoubleConverter(abc_converters.AbstractConverter[int | float]):  # <--|
    def convert(self, value: Any) -> int | float:  # <----------------------|
        if not isinstance(value, (int, float)):
            raise ValueError("Value must be instance of (int, float).")
        return value * 2


parser = TenseParser(TenseParser.DIGIT, converter=DoubleConverter())
assert parser.parse("1 minute") == 120  # 1 minute = 60 seconds, 60*2 = 120.
