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
"""Adapters of aiotense.application.ports."""
from __future__ import annotations

__all__ = ["DigitParser", "TimedeltaParser"]

from typing import TYPE_CHECKING, Callable, Optional

from aiotense.application.ports import parsers

from . import converters

if TYPE_CHECKING:
    from aiotense.application.ports import converters as abc_converters
    from aiotense.domain import model


class DigitParser(parsers.AbstractParser):
    async def _parse(self, raw_str: str) -> int:
        multiplier = self.tense.multiplier
        resolved = self._resolver(raw_str, self.tense)
        duration = 0

        for pos, word in enumerate(resolved):
            for unit in self.tense:
                if word in unit.aliases:
                    prev_entry = resolved[pos - 1]
                    if not prev_entry.isdigit():
                        continue

                    duration += int(prev_entry) * (unit.duration * multiplier)

        return duration


class TimedeltaParser(DigitParser):
    def __init__(
        self,
        *,
        tense: model.Tense,
        resolver: Optional[Callable[[str, model.Tense], list[str]]] = None,
        converter: Optional[abc_converters.AbstractConverter] = None,
    ) -> None:
        super().__init__(
            tense=tense,
            resolver=resolver,
            converter=converters.TimedeltaConverter(),
        )
