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
__all__ = ["AbstractConverter"]

import abc
from typing import Any, Generic, TypeVar

T_co = TypeVar("T_co", covariant=True)


class AbstractConverter(abc.ABC, Generic[T_co]):
    @abc.abstractmethod
    async def convert(self, value: Any) -> T_co:
        ...
