from __future__ import annotations

import abc
import inspect
from typing import Any, Generic, TypeVar, Type, Hashable, final, Optional

from tense.service_layer.dot_tense.service import converters, domain, base

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)


def sorting_hat(target: str) -> domain.HashableParticle:
    for pname in domain.__all__:
        particle = getattr(domain, pname)
        if inspect.isabstract(particle):
            continue

        particle = particle(target)
        if particle.matches():
            return particle

    raise KeyError(f"Particle not found for {target!s}.")


def inject_particle_converters() -> dict[
    Type[domain.HashableParticle], converters.AbstractParticleConverter,
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
        self._next_handler: Optional[AbstractStepChain] = None

    @final
    def set_next(self, handler: Optional[AbstractStepChain]) -> AbstractStepChain:
        self._next_handler = handler
        return handler

    @abc.abstractmethod
    def take_a_step(self, target: T) -> T_co:
        ...

    @property
    def next_handler(self) -> Optional[AbstractStepChain]:
        return self._next_handler


class FirstStep(AbstractStepChain[str, dict[Hashable, Any]]):
    @staticmethod
    def _trim_comment(line: str) -> str:
        if "#" in line:
            return line[: line.find("#")]
        return line

    def take_a_step(self, target: str) -> dict[Hashable, Any]:
        groups = {}
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

            elif isinstance(particle, domain.ListParticle):
                last_section_type = type(groups[last_section])
                if last_section_type is dict:
                    groups[last_section] = []

                converted_value = pconverters[particle_type].convert(particle.target)
                if particle.is_comma_list():
                    groups[last_section] = sum(
                        (groups[last_section], converted_value),
                        [],
                    )
                else:
                    groups[last_section].append(converted_value)

            elif isinstance(particle, domain.GetattributeParticle):
                groups[last_section].update(
                    pconverters[particle_type].convert(particle.target)
                )

            continue

        return groups


class SecondStep(AbstractStepChain[dict[Hashable, Any], dict[Hashable, Any]]):
    def take_a_step(self, target: dict[Hashable, Any]) -> dict[Hashable, Any]:
        base.tenses.update(target)
        return base.tenses


class LastStep(AbstractStepChain[dict[Hashable, Any], dict[Hashable, Any]]):
    def take_a_step(self, target: dict[Hashable, Any]) -> dict[Hashable, Any]:
        return target


def from_tense_file(file_source: str) -> Any:
    first_step = FirstStep()
    (
        first_step
        .set_next(SecondStep())
        .set_next(LastStep())
    )
    handler = first_step
    parsed_source = file_source
    while handler.next_handler is not None:
        parsed_source = handler.take_a_step(parsed_source)
        handler = handler.next_handler

    return parsed_source
