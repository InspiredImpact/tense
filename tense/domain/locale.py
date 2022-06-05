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
"""Locale domain."""
from __future__ import annotations

__all__ = ["Locale"]

from dataclasses import dataclass
from typing import Iterator, Iterable

from tense.domain import units


@dataclass
class Locale:
    minute: units.Minute
    hour: units.Hour
    day: units.Day
    week: units.Week

    def __post_init__(self) -> None:
        self.iterunits = list(self.__dict__.values())

    def __iter__(self) -> Iterator[units.Unit]:
        for unit in self.iterunits:
            if isinstance(unit, units.Unit):
                yield unit

    def with_virtual_units(self, virtual: Iterable[units.Unit], /) -> Locale:
        self.iterunits.extend(virtual)
        return self
