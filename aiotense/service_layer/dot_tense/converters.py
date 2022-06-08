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
"""Dot_tense service converters."""
from __future__ import annotations

__all__ = [
    "AbstractParticleConverter",
    "DigitValueConverter",
    "BooleanValueConverter",
    "ListValueConverter",
    "AbstractParticleValueConverter",
    "PARTICLE_CONVERTERS",
    "GETATTRIBUTE_VALUE_CONVERTERS",
]

import abc
from typing import Any, Final, Hashable

from aiotense.service_layer.safe_eval import SafelyExpEvalute

_VCONVERTER_CONSTS: Final[dict[str, int]] = {
    "second": 1,
    "minute": 60,
    "hour": 60 * 60,
    "day": 60 * 60 * 24,
    "week": 60 * 60 * 24 * 7,
    "year": 60 * 60 * 24 * 365,
}


class AbstractParticleConverter(abc.ABC):
    """Base converter for particles (tokens)."""

    @abc.abstractmethod
    def convert(self, value: Any) -> Any:
        ...


class AbstractParticleValueConverter(abc.ABC):
    """Base converter for particle values.

    We can say that it is a subconverter.
    For example, if AbstractParticleConverter
    will convert the expression `variable = value`,
                                            ^^^^^
    then AbstractParticleValueConverter will convert
    the value of `variable` -- `value`.
                                ^^^^^
    """
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
        for vconverter in GETATTRIBUTE_VALUE_CONVERTERS:
            if vconverter.matches(value):
                return {key: vconverter.convert(value)}

        raise ValueError(f"Can't find converter for {value!r}")


class DigitValueConverter(AbstractParticleValueConverter):
    def matches(self, value: str) -> bool:
        return value.isdigit()

    def convert(self, value: str) -> int:
        return int(value)


class BooleanValueConverter(AbstractParticleValueConverter):
    def matches(self, value: str) -> bool:
        return value.lower() in {"true", "false"}

    def convert(self, value: str) -> bool:
        return value.lower() == "true"


class ListValueConverter(AbstractParticleValueConverter):
    def matches(self, value: str) -> bool:
        return len(value.split(",")) > 1

    def convert(self, value: str) -> list[str] | str:
        by_comma = value.split(",")
        return [i.strip() for i in by_comma if i and not i.isspace()]


class ExpressionValueConverter(AbstractParticleValueConverter):
    def matches(self, value: str) -> bool:
        return value.startswith("exp(") and value.endswith(")")

    def convert(self, value: str) -> Any:
        exp = value[value.find("(") + 1 : value.find(")")]
        return SafelyExpEvalute(exp, eval_locals=_VCONVERTER_CONSTS).safe_evalute()


PARTICLE_CONVERTERS: frozenset[AbstractParticleConverter] = frozenset(
    (GetattributeParticleConverter(),)
)
GETATTRIBUTE_VALUE_CONVERTERS: frozenset[AbstractParticleValueConverter] = frozenset(
    (
        BooleanValueConverter(),
        DigitValueConverter(),
        ListValueConverter(),
        ExpressionValueConverter(),
    )
)
