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
"""Tense domain."""
from __future__ import annotations

__all__ = ["Tense"]

import warnings
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Iterator

from tense.domain import units

if TYPE_CHECKING:
    from tense.application.ports import repository


@dataclass
class Tense:
    """A class that is responsible for aliasing units of time.

    !!! warning
        If the `multiplier` attribute of this class is less than
        or equal to zero, a warning will be issued to the console,
        since in this case the parsers may not work correctly.

    !!! note
        This class adds each virtual unit of time to `self.__dict__`,
        as it filters values from there in `__iter__` ,method.

        For each virtual unit, a name is generated according to the
        following pattern: `virtual_name` + `virtual_number`.

    !!! info
        This class caches time units in the `_cached_units` attribute
        when iterating.

    Parameters:
    -----------
    second: :class:`units.Second`
        Representing the `second` as a unit of time.
    minute: :class:`units.Minute`
        Representing the `minute` as a unit of time.
    hour: :class:`units.Hour`
        Representing the `hour` as a unit of time.
    day: :class:`units.Day`
        Representing the `day` as a unit of time.
    week: :class:`units.Week`
        Representing the `week` as a unit of time.
    year: :class:`units.Year`
        Representing the `year` as a unit of time.
    virtual: :class:`list[dict[str, Any]]` = field(default_factory=list)
        List of custom units of time.
    """

    second: units.Second
    minute: units.Minute
    hour: units.Hour
    day: units.Day
    week: units.Week
    year: units.Year
    multiplier: int = 1
    virtual: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._cached_units: set[units.Unit] = set()
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
        else:
            for unit in self.__dict__.values():
                if isinstance(unit, units.Unit):
                    self._cached_units.add(unit)
                    yield unit

    def _resolve_virtual(self) -> None:
        """Adds virtual units to the current state of the class."""
        for n, unit_dict in enumerate(self.virtual):
            self.__dict__[f"virtual{n}"] = units.VirtualUnit(**unit_dict)

    @classmethod
    def from_dict(cls, tense_dict: dict[str, Any], /) -> Tense:
        """An alternative way to create an instance of a class using
        a configuration dictionary.

        !!! note
            This constructor interacts with the globals() of this module.
            Therefore, when adding new settings that are associated with
            other modules, these modules will need to be imported into this
            one, otherwise they simply will not be found.

        Parameters:
        -----------
        tense_dict: :class:`dict[str, Any]`, /
            Configuration dictionary.
        """
        tense_attrs = {}
        for key, attrs in tense_dict.items():
            module, cls_name = key.split(".")
            if cls_name == cls.__name__:
                # This is the main section with general configuration settings.
                if not isinstance(attrs, dict):
                    # If it's empty.
                    continue

                tense_attrs.update(attrs)
                continue

            module = globals()[module]
            unit_cls = getattr(module, cls_name)
            tense_attrs[cls_name.lower()] = unit_cls(**attrs)
            continue

        return cls(**tense_attrs)

    @classmethod
    def from_repository(
        cls,
        repo: repository.AbstractTenseRepository,
        /,
    ) -> Tense:
        """An alternative way to create an instance of a class using a tense repository.
        Works at a higher level of abstraction than `cls.from_dict`.

        Parameters:
        -----------
        repo: :class:`repository.AbstractTenseRepository`, /
            Tense repository.
        """
        return cls.from_dict(repo.config)

    @property
    def all(self) -> list[str]:
        return sum(u.aliases for u in self)
