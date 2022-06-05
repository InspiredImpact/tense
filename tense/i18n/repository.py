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
"""Internationalization alias repository."""
from __future__ import annotations

__all__ = ["AbstractAliasRepository", "AliasRepository"]

import abc
from typing import TYPE_CHECKING, Any, Hashable, Iterable

import yaml

from .i18n import _ALIASES_DIR, _open_aliases

if TYPE_CHECKING:
    from tense import types


class AbstractAliasRepository(abc.ABC):
    def __init__(self) -> None:
        self.aliases: dict[Hashable, Any] = _open_aliases()

    @abc.abstractmethod
    def add_alias(
        self, locale: types.LocaleType, unit: types.UnitType, alias: str
    ) -> None:
        ...

    @abc.abstractmethod
    def get_aliases(
        self, locale: types.LocaleType, unit: types.UnitType
    ) -> Iterable[str]:
        ...


class AliasRepository(AbstractAliasRepository):
    def add_alias(
        self, locale: types.LocaleType, unit: types.UnitType, alias: str
    ) -> None:
        self.aliases[locale][unit].append(alias)

        with open(_ALIASES_DIR, "w") as yaml_file:
            yaml_file.write(yaml.safe_dump(self.aliases, default_flow_style=False))

    def get_aliases(
        self, locale: types.LocaleType, unit: types.UnitType
    ) -> Iterable[str]:
        return self.aliases[locale][unit]
