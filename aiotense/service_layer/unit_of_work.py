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
"""Unit of work for atomic alias operations."""
from __future__ import annotations

__all__ = ["AbstractTenseUnitOfWork", "TenseUnitOfWork"]

import abc
from typing import Any, Iterable

from aiotense.adapters import repository


class AbstractTenseUnitOfWork(abc.ABC):
    tenses: repository.AbstractTenseRepository

    def __enter__(self) -> AbstractTenseUnitOfWork:
        return self

    def __exit__(self, *args: Any) -> None:
        ...

    @abc.abstractmethod
    def delete_aliases(self, unit: str, aliases: Iterable[str]) -> None:
        ...

    @abc.abstractmethod
    def replace_aliases(self, unit: str, replacements: dict[str, str]) -> None:
        ...


class TenseUnitOfWork(AbstractTenseUnitOfWork):
    def __enter__(self) -> AbstractTenseUnitOfWork:
        self.tenses = repository.TenseRepository()
        return super().__enter__()

    @staticmethod
    def _with_unit_resolve(unit: str, /) -> str:
        if not unit.startswith("units."):
            unit = "units." + unit.title()
        return unit

    def delete_aliases(self, unit: str, aliases: Iterable[str]) -> None:
        unit = self._with_unit_resolve(unit)
        unit_aliases = self.tenses.source[unit]["aliases"]
        for alias in aliases:
            unit_aliases.remove(alias)

    def replace_aliases(self, unit: str, replacements: dict[str, str]) -> None:
        unit = self._with_unit_resolve(unit)
        unit_aliases = self.tenses.source[unit]["aliases"]
        for old, new in replacements.items():
            for idx, exiting_alias in enumerate(unit_aliases):
                if old == exiting_alias:
                    unit_aliases.pop(idx)
                    unit_aliases.insert(idx, new)
