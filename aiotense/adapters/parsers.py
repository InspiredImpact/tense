from datetime import datetime, timedelta

from aiotense.application.ports import parsers


class DigitParser(parsers.AbstractParser[int]):
    name = "digit"

    async def _parse(self, number: int) -> int:
        return number


class UtcDateParser(parsers.AbstractParser[datetime]):
    name = "utcdate"

    async def _parse(self, number: int) -> datetime:
        return datetime.utcnow() + timedelta(seconds=number)
