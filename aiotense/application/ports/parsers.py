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

__all__ = ["AbstractParser"]

import abc
from typing import final, TYPE_CHECKING, Any, Optional

from aiotense.application.ports import converters
if TYPE_CHECKING:
    from aiotense.domain import model


class AbstractParser(abc.ABC):
    def __init__(
        self, *, tense: model.Tense, converter: Optional[converters.AbstractConverter] = None,
    ) -> None:
        self.tense = tense
        self.converter = converter

    @final
    async def parse(self, raw_str: str) -> Any:
        value = await self._parse(raw_str)
        if self.converter is not None:
            value = await self.converter.convert(value)

        return value

    @abc.abstractmethod
    def _parse(self, raw_str: str) -> Any:
        ...
