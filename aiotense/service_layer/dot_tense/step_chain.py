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

__all__ = ["from_tense_file", "from_tense_file_source"]

import abc
import inspect
import pathlib
from typing import Any, Generic, Hashable, Optional, Type, TypeVar, cast, final

from aiotense.domain import model, units
from aiotense.service_layer.dot_tense import converters, domain, exceptions

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

_BASE_SETTING_PATH = "model.Tense"
_VIRTUAL_PREFIX = "virtual"
_VIRTUALS = []


def sorting_hat(target: str) -> domain.HashableParticle:
    for pname in domain.__all__:
        particle = getattr(domain, pname)
        if inspect.isabstract(particle):
            continue

        particle = particle(target)
        if particle.matches():
            return cast(domain.HashableParticle, particle)

    raise KeyError(f"Particle not found for {target!s}.")


def inject_particle_converters() -> dict[
    Type[domain.HashableParticle],
    converters.AbstractParticleConverter,
]:
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
    def take_a_step(self, target: dict[str, Any]) -> dict[str, Any]:
        _copied_target = target.copy()
        for key, value in _copied_target.items():
            key_parts = key.split(".")
            if len(key_parts) == 1:
                if key_parts[0].lower() != _VIRTUAL_PREFIX:
                    raise exceptions.AnalyzeError(f"Undefined key {key!r}.")
                _VIRTUALS.append(value)
                target.pop(key)
                continue

            key_type, obj_type = key_parts
            module = globals().get(key_type, None)
            if module is None:
                raise exceptions.AnalyzeError(
                    f"Undefined part {key_type!r} in key {key!r}."
                )

            obj = getattr(module, obj_type, None)
            if obj is None:
                raise exceptions.AnalyzeError(
                    f"Undefined object {obj_type!r} in key {key!r}."
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
