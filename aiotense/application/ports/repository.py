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
""" """
from __future__ import annotations

__all__ = ["AbstractTenseRepository"]

import abc
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aiotense.domain import units


class AbstractTenseRepository(abc.ABC):
    def __init__(self, source: Optional[dict[str, Any]] = None, /) -> None:
        self.source = source

    @abc.abstractmethod
    def get_config(self) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def get_setting(self, setting: str, /) -> Any:
        ...

    @abc.abstractmethod
    def add_setting(self, setting: str, value: Any, /) -> None:
        ...

    @abc.abstractmethod
    def add_virtual_unit(self, unit: units.VirtualUnit) -> None:
        ...

    @abc.abstractmethod
    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> None:
        ...
