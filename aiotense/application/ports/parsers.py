# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" """
from __future__ import annotations

__all__ = ["AbstractParser"]

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
        resolved = _resolve_time_string(raw_str)
        duration = 0
        for pos, char in enumerate(resolved):
            for unit in self.tense:
                if char in unit.aliases:
                    prev_entry = resolved[pos - 1]
                    if not prev_entry.isdigit():
                        continue
                    duration += int(prev_entry) * (unit.duration * multiplier)

        return await self._parse(duration)

    @abc.abstractmethod
    async def _parse(self, number: int) -> T_co:
        ...
