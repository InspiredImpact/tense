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
"""Tense config parser."""
from __future__ import annotations

__all__ = ["from_tense_file", "from_tense_file_source"]

import abc
import difflib
import inspect
import pathlib
from typing import (
    Any,
    Final,
    Generic,
    Hashable,
    Iterable,
    Optional,
    Type,
    TypeVar,
    cast,
    final,
)

from aiotense.domain import model, units
from aiotense.service_layer.dot_tense import converters, domain, exceptions

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

_BASE_SETTING_PATH: Final[str] = "model.Tense"
_VIRTUAL_PREFIX: Final[str] = "virtual"
_VIRTUALS: list[dict[str, Any]] = []

_ONEWORD_HEADER_MATCHES: Final[tuple[str, ...]] = (_VIRTUAL_PREFIX,)
_MODULE_HEADER_MATCHES: Final[tuple[str, ...]] = (
    "model",
    "units",
)
_OBJTYPE_MATCHES: Final[list[str]] = model.__all__ + units.__all__


def sorting_hat(initial: str, /) -> domain.HashableParticle:
    """Converts a string to a particle (token) for further parsing.

    Parameters:
        initial: :class:`str`, /
            String to parse.

    Raises:
        :class:`KeyError`
            If particle for string not found.

    :return: domain.HashableParticle
    """
    for pname in domain.__all__:
        particle = getattr(domain, pname)
        if inspect.isabstract(particle):
            continue

        particle = particle(initial)
        if particle.matches():
            return cast(domain.HashableParticle, particle)

    raise KeyError(f"Particle not found for {initial!s}.")


def inject_particle_converters() -> dict[
    Type[domain.HashableParticle],
    converters.AbstractParticleConverter,
]:
    """

    :return: dict[particle: converter]
    """
    injected = {}
    for pname in domain.__all__:
        particle = getattr(domain, pname)
        if inspect.isabstract(particle):
            continue

        for converter in converters.PARTICLE_CONVERTERS:
            if particle.matches_converter(converter):
                injected[particle] = converter
                continue

    return injected


class AbstractStepChain(abc.ABC, Generic[T, T_co]):
    # ~T - accept value
    # ~T_co - return value
    def __init__(self) -> None:
        self._next_handler: Optional[AbstractStepChain[T, T_co]] = None

    @final
    def set_next(
        self, handler: AbstractStepChain[Any, Any]
    ) -> AbstractStepChain[Any, Any]:
        self._next_handler = handler
        return handler

    @abc.abstractmethod
    def take_a_step(self, target: T) -> T_co:
        ...

    @property
    def next_handler(self) -> Optional[AbstractStepChain[Any, Any]]:
        return self._next_handler


class LexingStep(AbstractStepChain[str, dict[str, Any]]):
    @staticmethod
    def _trim_comment(line: str) -> str:
        if "#" in line:
            return line[: line.find("#")]
        return line

    def take_a_step(self, target: str) -> dict[str, Any]:
        groups: dict[str, Any] = {}
        last_section = ""
        pconverters = inject_particle_converters()

        for line in target.split("\n"):
            line = self._trim_comment(line)
            if not line:
                continue

            particle = sorting_hat(line)
            particle_type = type(particle)
            if isinstance(particle, domain.HeaderParticle):
                section = particle.strip_header(line)
                groups[section] = {}
                last_section = section

            elif isinstance(particle, domain.GetattributeParticle):
                groups[last_section].update(
                    pconverters[particle_type].convert(particle.target)
                )

            continue

        return groups


class AnalyzeStep(AbstractStepChain[dict[str, Any], dict[str, Any]]):
    @staticmethod
    def _with_suggest_to(
        part: str,
        *,
        matches: Iterable[str],
        in_: Optional[str] = None,
    ) -> str:
        base_msg = f"Undefined part {part!r}"
        if in_ is not None:
            base_msg += f" in {in_!r}."

        matches = difflib.get_close_matches(part, matches)
        if matches:
            base_msg += f" Did you mean any of ~{matches}?"
        return base_msg

    def take_a_step(self, target: dict[str, Any]) -> dict[str, Any]:
        _copied_target = target.copy()
        for key, value in _copied_target.items():
            key_parts = key.split(".")
            if len(key_parts) == 1:
                if key_parts[0].lower() != _VIRTUAL_PREFIX:
                    raise exceptions.AnalyzeError(
                        self._with_suggest_to(key, matches=_ONEWORD_HEADER_MATCHES)
                    )
                _VIRTUALS.append(value)
                target.pop(key)
                continue

            key_type, obj_type = key_parts
            module = globals().get(key_type, None)
            if module is None:
                raise exceptions.AnalyzeError(
                    self._with_suggest_to(
                        key_type, in_=key, matches=_MODULE_HEADER_MATCHES
                    )
                )

            obj = getattr(module, obj_type, None)
            if obj is None:
                raise exceptions.AnalyzeError(
                    self._with_suggest_to(obj_type, in_=key, matches=_OBJTYPE_MATCHES)
                )

        return target


class CompilingStep(AbstractStepChain[dict[str, Any], dict[str, Any]]):
    def take_a_step(self, target: dict[str, Any]) -> dict[str, Any]:
        if _VIRTUALS:
            target[_BASE_SETTING_PATH][_VIRTUAL_PREFIX] = _VIRTUALS
        return target


class _ShadowStep(AbstractStepChain[dict[Hashable, Any], dict[Hashable, Any]]):
    def take_a_step(self, target: dict[Hashable, Any]) -> dict[Hashable, Any]:
        return target


def from_tense_file_source(file_source: str, /) -> Any:
    (
        (first_step := LexingStep())
        .set_next(AnalyzeStep())
        .set_next(CompilingStep())
        .set_next(_ShadowStep())
    )
    handler: AbstractStepChain[Any, Any] = first_step
    parsed_source: Any = file_source
    while handler.next_handler is not None:
        parsed_source = handler.take_a_step(parsed_source)
        handler = handler.next_handler

    return parsed_source


def from_tense_file(path: pathlib.Path | str, /) -> Any:
    with open(path, "r") as file:
        return from_tense_file_source(file.read())
