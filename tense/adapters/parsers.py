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
"""Adapters of tense.application.ports."""
from __future__ import annotations

__all__ = ["DigitParser", "TimedeltaParser"]

from typing import TYPE_CHECKING, Callable, Optional

from tense.application.ports import parsers as abc_parsers

from . import converters

if TYPE_CHECKING:
    from tense.application.ports import converters as abc_converters
    from tense.domain import model


class DigitParser(abc_parsers.AbstractParser):
    def _parse(self, raw_str: str, /) -> int:
        resolved = self._resolver(raw_str, self._tense)
        duration = 0
        last_num: Optional[int] = None
        try:
            while 1:
                part = next(resolved)
                if part.isdigit():
                    last_num = int(part)
                    continue
                if last_num is None:
                    continue
                for unit in self._iterunits:
                    if part in unit.aliases:
                        duration += last_num * (unit.duration * self._tense.multiplier)
        except StopIteration:
            return duration
        return duration


class TimedeltaParser(DigitParser):
    def __init__(
        self,
        *,
        tense: model.Tense,
        resolver: Optional[Callable[[str, model.Tense], list[str]]] = None,
        iteration_speedup: bool = False,
        converter: Optional[abc_converters.AbstractConverter] = None,
    ) -> None:
        super().__init__(
            tense=tense,
            resolver=resolver,
            iteration_speedup=iteration_speedup,
            converter=converters.TimedeltaConverter(),
        )
