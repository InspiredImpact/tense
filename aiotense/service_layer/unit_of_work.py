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
from typing import TYPE_CHECKING, Any, Iterable

from aiotense.adapters import repository

if TYPE_CHECKING:
    from aiotense.application.ports import repository as abc_repository


class AbstractUnitOfWork:
    """Base class for atomic operations. Useful for annotations.

    Implements in:
        ~ :class:`AbstractTenseUnitOfWork`
        ~ :class:`TenseUnitOfWork`
    """
    products: Any
    pass


class AbstractTenseUnitOfWork(AbstractUnitOfWork, abc.ABC):
    """An abstract class whose subclasses are responsible for
    atomic operations on Tense units (remove unit aliases/replace/...).

    Implements in:
        ~ :class:`TenseUnitOfWork`
    """
    products: abc_repository.AbstractTenseRepository

    def __enter__(self) -> AbstractTenseUnitOfWork:
        return self

    def __exit__(self, *args: Any) -> None:
        """Stub for syntax sugar `with`. Allows you to group code into
        logical blocks.
        """
        pass

    @abc.abstractmethod
    def update_config(self, config: dict[str, Any], /) -> None:
        """Replaces the items of the current dictionary config with new
        ones using the dict.update(new) method.

        Parameters:
        -----------
        config: :class:`dict[str, Any]`, /
            New config items.

        Returns:
        --------
        builtins.None
        """
        ...

    @abc.abstractmethod
    def delete_aliases(self, unit: str, aliases: Iterable[str]) -> None:
        """Removes aliases for a concrete unit of time.

        !!! Note:
            Will raise KeyError if you specify a non-existent unit of time.
            See the documentation for all valid time units. If you added
            virtual aliases, then you can view the current state of the
            config using the `~self.get_config()` method or by accessing
            the source attribute (`~self.products.source`).

        Parameters:
        -----------
        unit: :class:`str`
            Concrete unit of time.

        aliases: :class:`Iterable[str]`
            Iterable object that contains string aliases for concrete unit
            of time.

        Returns:
        --------
        builtins.None
        """
        ...

    @abc.abstractmethod
    def replace_aliases(self, unit: str, replacements: dict[str, str]) -> None:
        """Replace aliases for concrete unit of time.

        !!! Note:
            Will raise KeyError if you specify a non-existent unit of time.
            See the documentation for all valid time units. If you added
            virtual aliases, then you can view the current state of the
            config using the `~self.get_config()` method or by accessing
            the source attribute (`~self.products.source`).

        Parameters:
        -----------
        unit: :class:`str`
            Concrete unit of time.

        replacements: :class:`dict[str, str]`
            Dictionary where keys are old aliases and values are new aliases.

        Returns:
        --------
        builtins.None
        """
        ...


class TenseUnitOfWork(AbstractTenseUnitOfWork):
    """Adapter of :class:`AbstractTenseUnitOfWork`."""
    def __enter__(self) -> AbstractTenseUnitOfWork:
        self.tenses = repository.TenseRepository()
        return super().__enter__()

    @staticmethod
    def _with_unit_resolve(unit: str, /) -> str:
        if not unit.startswith("units."):
            unit = "units." + unit.title()
        return unit

    def update_config(self, config: dict[str, Any]) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        self.tenses.source.update(config)

    def delete_aliases(self, unit: str, aliases: Iterable[str]) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        unit = self._with_unit_resolve(unit)
        unit_aliases = self.tenses.source[unit]["aliases"]
        for alias in aliases:
            unit_aliases.remove(alias)

    def replace_aliases(self, unit: str, replacements: dict[str, str]) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        unit = self._with_unit_resolve(unit)
        unit_aliases = self.tenses.source[unit]["aliases"]
        for old, new in replacements.items():
            for idx, exiting_alias in enumerate(unit_aliases):
                if old == exiting_alias:
                    unit_aliases.pop(idx)
                    unit_aliases.insert(idx, new)
