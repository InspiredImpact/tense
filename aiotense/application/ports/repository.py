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
"""Interfaces that are implemented in aiotense.adapters."""
from __future__ import annotations

__all__ = ["AbstractTenseRepository"]

import abc
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aiotense.domain import units


class AbstractTenseRepository(abc.ABC):
    def __init__(self, source: Optional[dict[str, Any]] = None, /) -> None:
        self.source = source

    def __getitem__(self, item: Any) -> Any:
        if not isinstance(item, str):
            return NotImplemented
        return self.source[item]

    def __setitem__(self, key: Any, value: Any) -> Any:
        if not isinstance(key, str) or not isinstance(value, str):
            return NotImplemented
        if key not in self.source:
            raise KeyError(
                f"Key {key} does not exist in config. New keys cannot be added."
            )
        self.source[key] = value

    @abc.abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Returns deepcopy of current config."""
        ...

    @abc.abstractmethod
    def get_setting(self, path: str, setting: str, /) -> Any:
        ...

    @abc.abstractmethod
    def add_virtual_unit(self, unit: units.VirtualUnit) -> None:
        """Adds custom unit of time."""
        ...

    @abc.abstractmethod
    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> None:
        """Adds custom unit of time."""
        ...
