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
"""Interfaces that are implemented in tense.adapters."""
from __future__ import annotations

__all__ = ["AbstractTenseRepository"]

import abc
from typing import TYPE_CHECKING, Any, Optional, Type, TypedDict

if TYPE_CHECKING:
    from tense.domain import units

    class _VirtualUnitDict(TypedDict):
        duration: int
        aliases: list[str]


class AbstractTenseRepository(abc.ABC):
    """Interface for tense repository.

    Repositories are a kind of wrapper for get / add operations on
    a specific collection. It is worth noting that atomic operations
    (such as update/delete/replace) for changing repository data are
    implemented using the UnitOfWork pattern in the service layer.

    This repository is a wrapper over the global settings for parsers
    and aliases for time units.

    !!! info
        `Add` operations allows fluent-style.

    Parameters:
    -----------
    config: :class:`Optional[dict[str, Any]]` = None, /
        Repository configuration.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None, /) -> None:
        self._config = config

    @property
    def config(self) -> Optional[dict[str, Any]]:
        """Non-data descriptor that returns repository configuration."""
        return self._config

    @abc.abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Returns deepcopy of repository configuration."""
        ...

    @abc.abstractmethod
    def get_setting(self, group: str, setting: str, /) -> Any:
        """Returns setting value.

        Parameters:
        -----------
        group: :class:`str`, /
            This argument is the name of the group whose settings you want to get.
            Headers in configurations like "model.Tense", "units.Second"... are
            considered as a group.
        setting: :class:`str`, /
            Group setting name.
        """
        ...

    @abc.abstractmethod
    def add_virtual_unit(self, unit: units.VirtualUnit, /) -> AbstractTenseRepository:
        """Adds custom unit of time.

        Parameters:
        -----------
        unit: :class:`units.VirtualUnit`, /
            Virtual unit object.
        """
        ...

    @abc.abstractmethod
    def add_virtual_unit_dict(
        self, unit_dict: _VirtualUnitDict, /
    ) -> AbstractTenseRepository:
        """Adds custom unit of time.

        Alternative method for adding virtual unit to repository.
        Is faster than adding using the units.VirtualUnit object.

        Parameters:
        -----------
        unit_dict: :class:`_VirtualUnitDict`
            VirtualUnit dictionary.
        """
        ...

    @abc.abstractmethod
    def add_aliases_to(
        self,
        unit: Type[units.Unit],
        /,
        aliases: list[str],
    ) -> AbstractTenseRepository:
        """Adds aliases to unit of time.

        Parameters:
        -----------
        unit: :class:`Type[units.Unit]`, /
            Concrete unit of time.
        aliases: :class:`list[str]`
            List of aliases to add.
        """
        ...
