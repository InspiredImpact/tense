from __future__ import annotations

import abc
import re
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from aiotense.domain import model

T_co = TypeVar("T_co", covariant=True)


def _resolve_time_string(time_str: str) -> list[str]:
    lst = time_str.strip().split(" ")
    if len(lst) == 1:
        return [e for e in re.split(r"(\d+)", time_str) if e]
    return lst


class AbstractParser(abc.ABC, Generic[T_co]):
    def __init__(self, *, tense: model.Tense) -> None:
        self.tense = tense

    async def parse(self, raw_str: str) -> T_co:
        multiplier = self.tense.multiplier
        raw_str = _resolve_time_string(raw_str)
        duration = 0
        for pos, char in enumerate(raw_str):
            for unit in self.tense:
                if char in unit.aliases:
                    prev_entry = raw_str[pos - 1]
                    if not prev_entry.isdigit():
                        continue
                    duration += int(prev_entry) * (
                        unit.duration * multiplier
                    )

        return await self._parse(duration)

    @abc.abstractmethod
    async def _parse(self, number: int) -> T_co:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...
