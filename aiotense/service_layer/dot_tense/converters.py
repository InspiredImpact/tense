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


class ExpressionValueConverter(AbstractValueConverter):
    def matches(self, value: str) -> bool:
        return value.startswith("exp(") and value.endswith(")")

    def convert(self, value: str) -> Any:
        exp = value[value.find("(") + 1 : value.find(")")]
        return SafelyExpEvalute(exp, eval_locals=_VCONVERTER_CONSTS).safe_evalute()


PARTICLE_CONVERTERS: frozenset[AbstractParticleConverter] = frozenset(
    (GetattributeParticleConverter(),)
)
VALUE_CONVERTERS: frozenset[AbstractValueConverter] = frozenset(
    (
        BooleanConverter(),
        DigitConverter(),
        ListValueConverter(),
        ExpressionValueConverter(),
    )
)
