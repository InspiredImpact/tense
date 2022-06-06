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

__all__ = ["AbstractAliasUnitOfWork", "AliasUnitOfWork"]

import abc
from typing import TYPE_CHECKING, Any

import yaml

from aiotense.i18n import repository
from aiotense.i18n.i18n import _ALIASES_DIR

if TYPE_CHECKING:
    from aiotense import types


class AbstractAliasUnitOfWork(abc.ABC):
    products: repository.AbstractAliasRepository

    def __enter__(self) -> AbstractAliasUnitOfWork:
        return self

    def __exit__(self, *args: Any) -> None:
        ...

    @abc.abstractmethod
    def delete_alias(
        self, locale: types.LocaleType, unit: types.UnitType, alias: str
    ) -> None:
        ...

    @abc.abstractmethod
    def replace_alias(
        self, locale: types.LocaleType, unit: types.UnitType, *, old: str, new: str
    ) -> None:
        ...


class AliasUnitOfWork(AbstractAliasUnitOfWork):
    def __enter__(self) -> AbstractAliasUnitOfWork:
        self.products = repository.AliasRepository()
        return super().__enter__()

    def delete_alias(
        self, locale: types.LocaleType, unit: types.UnitType, alias: str
    ) -> None:
        unit_path = self.products.aliases[locale][unit]
        for element in unit_path:
            if element == alias:
                unit_path.remove(element)

        with open(_ALIASES_DIR, "w") as yaml_file:
            yaml_file.write(
                yaml.safe_dump(self.products.aliases, default_flow_style=False)
            )

    def replace_alias(
        self, locale: types.LocaleType, unit: types.UnitType, *, old: str, new: str
    ) -> None:
        unit_path = self.products.aliases[locale][unit]
        if old not in unit_path:
            raise KeyError(f"Alias {old!s} not found.")

        for alias in unit_path:
            if alias == old:
                old_idx = unit_path.index(old)
                unit_path.pop(old_idx)
                unit_path.insert(old_idx, new)

        with open(_ALIASES_DIR, "w") as yaml_file:
            yaml_file.write(
                yaml.safe_dump(self.products.aliases, default_flow_style=False)
            )
