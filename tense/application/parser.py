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
"""Main file with time parser."""
__all__ = [
    "resolve_time_string",
    "TimeParser",
    "TimeParserEn",
    "TimeParserRu",
    "TimeParserUa",
]

import abc
import re
from typing import Generic, Literal, TypeVar

from tense import types
from tense.application import locales
from tense.domain import model as locale_model
from tense.service_layer import functional

LT = TypeVar("LT", bound=types.LocaleType)


def resolve_time_string(time_str: str, *, exclude_empty: bool = False) -> list[str]:
    lst = time_str.strip().split(" ")
    if len(lst) == 1:
        lst = re.split(r"(\d+)", time_str)

    if exclude_empty:
        return [e for e in lst if e]
    return lst


class TimeParser(abc.ABC, Generic[LT]):
    def __init__(self, raw_string: str) -> None:
        self._raw_str = resolve_time_string(raw_string, exclude_empty=True)

    async def parse_duration(self) -> int:
        duration = 0
        for pos, char in enumerate(self._raw_str):
            for unit in self.locale:
                if char in unit.aliases:
                    prev_entry = self._raw_str[pos - 1]
                    if not prev_entry.isdigit():
                        continue
                    duration += int(prev_entry) * unit.duration
        return duration

    @functional.cached_property
    @abc.abstractmethod
    def locale(self) -> locale_model.Locale:
        ...


class TimeParserEn(TimeParser[Literal["en"]]):
    @functional.cached_property
    def locale(self) -> locale_model.Locale:
        return locales.build_locale_from_string("en")


class TimeParserRu(TimeParser[Literal["ru"]]):
    @functional.cached_property
    def locale(self) -> locale_model.Locale:
        return locales.build_locale_from_string("ru")


class TimeParserUa(TimeParser[Literal["ua"]]):
    @functional.cached_property
    def locale(self) -> locale_model.Locale:
        return locales.build_locale_from_string("ua")
