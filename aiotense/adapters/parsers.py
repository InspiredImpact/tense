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

import re
from typing import TYPE_CHECKING

from aiotense.application.ports import parsers
from . import converters
if TYPE_CHECKING:
    from aiotense.domain import model

DIGIT_PATTERN: re.Pattern[str] = re.compile(r"(\d+)")


def resolve_time_string(raw_str: str) -> list[str]:
    """Example of supported patterns:
    * '1d1min'
    * '1d 1min'
    * '1d1min 2 seconds'
    """
    return list(
        filter(
            bool,
            DIGIT_PATTERN.split(raw_str.replace(" ", "")),
        )
    )


class DigitParser(parsers.AbstractParser):
    async def _parse(self, raw_str: str) -> int:
        multiplier = self.tense.multiplier
        resolved = resolve_time_string(raw_str)
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
    def __init__(self, *, tense: model.Tense) -> None:
        super().__init__(tense=tense, converter=converters.TimedeltaConverter())
