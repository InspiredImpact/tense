from __future__ import annotations

__all__ = [
    "AbstractParticleConverter",
    "DigitConverter",
    "BooleanConverter",
    "ListParticleConverter",
    "AbstractValueConverter",
    "PARTICLE_CONVERTERS",
    "VALUE_CONVERTERS",
]

import abc
from typing import TYPE_CHECKING, Any, Hashable, Literal, SupportsInt

if TYPE_CHECKING:
    _BooleanType = Literal["true", "True", "false", "False"]


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

    def convert(self, value: SupportsInt) -> int:
        return int(value)


class BooleanConverter(AbstractValueConverter):
    def matches(self, value: str) -> bool:
        return value.lower() in {"true", "false"}

    def convert(self, value: _BooleanType) -> bool:
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
