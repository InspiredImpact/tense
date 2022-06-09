from typing import Any

from aiotense import TenseParser
from aiotense.application.ports import parsers as abc_parsers
from aiotense.service_layer import functional


class CachedDigitParser(abc_parsers.AbstractParser):
    @functional.async_lru()  # type: ignore[misc]
    async def _parse(self, raw_str: str) -> Any:
        # Some expensive stuff here...
        ...


cached_digit_parser = TenseParser(CachedDigitParser)
# asyncio.run(cached_digit_parser.parse(string)) ...
