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

__all__ = [
    "AbstractTenseUnitOfWork",
    "TenseUnitOfWork",
]

import abc
from typing import TYPE_CHECKING, Any, Iterable, Type

from tense.adapters import repository
from tense.domain import units

if TYPE_CHECKING:
    from tense.application.ports import repository as abc_repository


class AbstractTenseUnitOfWork(abc.ABC):
    """An abstract class whose subclasses are responsible for
    atomic operations on Tense units (remove unit aliases/replace/...).

    Implements in:
        ~ :class:`TenseUnitOfWork`
    """

    __slots__ = ("products",)

    products: abc_repository.AbstractTenseRepository

    def __enter__(self) -> AbstractTenseUnitOfWork:
        return self

    def __exit__(self, *args: Any) -> None:
        """Stub for syntax sugar `with`. Allows you to group code into
        logical blocks.
        """
        pass

    @staticmethod
    def with_unit_resolve(unit: str | Type[units.Unit], /) -> str:
        if not isinstance(unit, str):
            if not issubclass(unit, units.Unit):
                raise ValueError("Unit must be instance of str or units.Unit.")
            unit = unit.__name__
        if not unit.startswith("units."):
            unit = "units." + unit.title()
        return unit

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
    def delete_aliases(self, unit: Type[units.Unit], aliases: Iterable[str]) -> None:
        """Removes aliases for a concrete unit of time.

        !!! Note:
            Will raise KeyError if you specify a non-existent unit of time.
            See the docs for all valid time units. If you added
            virtual aliases, then you can view the current state of the
            config using the `~self.get_config()` method or by accessing
            the config attribute (`~self.products.config`).

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
    def replace_aliases(
        self,
        unit: Type[units.Unit],
        replacements: dict[str, str],
    ) -> None:
        """Replace aliases for concrete unit of time.

        !!! Note:
            Will raise KeyError if you specify a non-existent unit of time.
            See the docs for all valid time units. If you added
            virtual aliases, then you can view the current state of the
            config using the `~self.get_config()` method or by accessing
            the config attribute (`~self.products.config`).

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

    __slots__ = ("products",)

    def __enter__(self) -> AbstractTenseUnitOfWork:
        self.products = repository.TenseRepository()
        return super().__enter__()

    def update_config(self, config: dict[str, Any]) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        self.products.config.update(config)

    def delete_aliases(self, unit: Type[units.Unit], aliases: Iterable[str]) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        unit = self.with_unit_resolve(unit.__name__)  # type: ignore[assignment]
        unit_aliases = self.products.config[unit]["aliases"]
        for alias in aliases:
            unit_aliases.remove(alias)

    def replace_aliases(
        self,
        unit: Type[units.Unit],
        replacements: dict[str, str],
    ) -> None:
        # <<inherited docstring from :class:`AbstractTenseUnitOfWork`>> #
        unit = self.with_unit_resolve(unit.__name__)  # type: ignore[assignment]
        unit_aliases = self.products.config[unit]["aliases"]
        for old, new in replacements.items():
            for idx, exiting_alias in enumerate(unit_aliases):
                if old == exiting_alias:
                    unit_aliases.pop(idx)
                    unit_aliases.insert(idx, new)
