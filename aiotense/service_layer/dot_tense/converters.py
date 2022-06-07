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

__all__ = [
    "AbstractParticleConverter",
    "DigitConverter",
    "BooleanConverter",
    "ListValueConverter",
    "AbstractValueConverter",
    "PARTICLE_CONVERTERS",
    "VALUE_CONVERTERS",
]

import abc
from typing import Any, Hashable


class AbstractParticleConverter(abc.ABC):
    @abc.abstractmethod
    def convert(self, value: Any) -> Any:
        ...


class AbstractValueConverter(abc.ABC):
    @abc.abstractmethod
    def matches(self, value: str) -> bool:
        ...

    @abc.abstractmethod
    def convert(self, value: str) -> Any:
        ...


class GetattributeParticleConverter(AbstractParticleConverter):
    @staticmethod
    def _parse_exp(value: str) -> tuple[str, str]:
        key, value = [_.strip() for _ in value.split("=")]
        return key, value

    def convert(self, value: str) -> dict[Hashable, Any]:
        key, value = self._parse_exp(value)
        for vconverter in VALUE_CONVERTERS:
            if vconverter.matches(value):
                return {key: vconverter.convert(value)}

        raise ValueError(f"Can't find converter for {value!r}")


class DigitConverter(AbstractValueConverter):
    def matches(self, value: str) -> bool:
        return value.isdigit()

    def convert(self, value: str) -> int:
        return int(value)


class BooleanConverter(AbstractValueConverter):
    def matches(self, value: str) -> bool:
        return value.lower() in {"true", "false"}

    def convert(self, value: str) -> bool:
        return value.lower() == "true"


class ListValueConverter(AbstractValueConverter):
    def matches(self, value: str) -> bool:
        return len(value.split(",")) > 1

    def convert(self, value: str) -> list[str] | str:
        by_comma = value.split(",")
        return [i.strip() for i in by_comma if i and not i.isspace()]


PARTICLE_CONVERTERS: frozenset[AbstractParticleConverter] = frozenset(
    (GetattributeParticleConverter(),)
)
VALUE_CONVERTERS: frozenset[AbstractValueConverter] = frozenset(
    (
        BooleanConverter(),
        DigitConverter(),
        ListValueConverter(),
    )
)
