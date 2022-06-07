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

__all__ = ["Tense"]

import warnings
from dataclasses import dataclass, field
from typing import Any, Iterator

from aiotense.domain import units


@dataclass
class Tense:
    minute: units.Minute
    hour: units.Hour
    day: units.Day
    week: units.Week
    multiplier: int = 1
    virtual: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._cached_units: list[units.Unit] = []
        if self.multiplier <= 0:
            warnings.warn(
                "The time multiplier is less than zero, the work of "
                "parsers may be incorrect. It is recommended to set "
                "the value more than zero."
            )
        if self.virtual:
            self._resolve_virtual()

    def __iter__(self) -> Iterator[units.Unit]:
        _cached_units = self._cached_units
        if _cached_units:
            yield from _cached_units

        for unit in self.__dict__.values():
            if isinstance(unit, units.Unit):
                self._cached_units.append(unit)
                yield unit

    def _resolve_virtual(self) -> None:
        for n, unit_dict in enumerate(self.virtual):
            self.__dict__[f"virtual{n}"] = units.VirtualUnit(**unit_dict)

    @classmethod
    def from_dict(cls, tense_dict: dict[str, Any], /) -> Tense:
        tense_attrs = {}
        for key, attrs in tense_dict.items():
            module, cls_name = key.split(".")
            if cls_name == cls.__name__:
                if not isinstance(attrs, dict):
                    continue

                tense_attrs.update(attrs)
                continue

            module = globals()[module]
            unit_cls = getattr(module, cls_name)
            tense_attrs[cls_name.lower()] = unit_cls(**attrs)
            continue

        return cls(**tense_attrs)
