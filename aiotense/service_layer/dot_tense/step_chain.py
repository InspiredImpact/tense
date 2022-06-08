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
import io
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

_COMMENT: Final[str] = "#"
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
    Checks all domain names, if the class is abstract then skips it.

    Parameters
    -----------
    initial: :class:`str`, /
        String to parse.

    Raises
    ------
    :class:`KeyError`
        If particle for string is not found.
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
    """Injects converters for particles.
    Abstract particles are skipped.
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
    """Abstract class - chain of responsibility pattern.
    Used to step by step parse the configuration file into a working state.

    !!! Note:
        This class is Generic in which:
        ~T - accept value.
        ~T_co - return value.
    """

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
        """Converts the current value - (~T) to another value - (~T_co)."""
        ...

    @property
    def next_handler(self) -> Optional[AbstractStepChain[Any, Any]]:
        return self._next_handler


class LexingStep(AbstractStepChain[str, dict[str, Any]]):
    """At this step, a string representation of the configuration is received.
    Breaks the string config into particles (tokens) for further parsing.

    !!! Note:
        * The parser goes through the configuration from top to bottom, one line
          at a time. Therefore, it is important to observe the order of settings.
        * Each header is a dictionary.
    """

    @staticmethod
    def _trim_comment(line: str, /) -> str:
        """Removes comments from a string line."""
        if _COMMENT in line:
            return line[: line.find(_COMMENT)]
        return line

    def take_a_step(self, target: str) -> dict[str, Any]:
        # <inherited docstring from :class:`AbstractStepChain`> #
        groups: dict[str, Any] = {}
        last_section = ""
        pconverters = inject_particle_converters()

        for line in target.split("\n"):
            line = self._trim_comment(line).strip()
            if not line:
                # Line is empty.
                continue

            particle = sorting_hat(line)  # Parsing line to particle (token).
            particle_type = type(particle)
            if isinstance(particle, domain.HeaderParticle):
                # Currently, supports only comma lists
                # | alias, alias, alias
                section = particle.strip_header(line)
                groups[section] = {}
                last_section = section

            elif isinstance(particle, domain.GetattributeParticle):
                # Currently, supports only with exp() wrapper.
                # | exp(2 + 2 * 2)
                groups[last_section].update(
                    pconverters[particle_type].convert(particle.target)
                )

            continue

        return groups


class AnalyzeStep(AbstractStepChain[dict[str, Any], dict[str, Any]]):
    """At this stage, the already converted configuration into a dictionary
    is accepted. Checks for validity all names and in case of failure gives
    an error (often with a suggestion of possible variants of the word).
    """

    @staticmethod
    def _with_suggest_to(
        part: str,
        *,
        matches: Iterable[str],
        in_: Optional[str] = None,
    ) -> str:
        """Suggest possible word options."""
        base_msg = f"Undefined part {part!r}"
        if in_ is not None:
            base_msg += f" in {in_!r}."

        matches = difflib.get_close_matches(part, matches)
        if matches:
            base_msg += f" Did you mean any of ~{matches}?"
        return base_msg

    def take_a_step(self, target: dict[str, Any]) -> dict[str, Any]:
        # <inherited docstring from :class:`AbstractStepChain`> #
        _copied_target = target.copy()
        for key, value in _copied_target.items():
            key_parts = key.split(".")
            if len(key_parts) == 1:
                # In this case, the line is a one-word header, something like [virtual].
                # For such it is necessary to make a separate check.
                key = key_parts[0].lower()
                if key not in _ONEWORD_HEADER_MATCHES:
                    raise exceptions.AnalyzeError(
                        self._with_suggest_to(key, matches=_ONEWORD_HEADER_MATCHES)
                    )
                # Currently, supports only one one-word header.
                if key == _VIRTUAL_PREFIX:
                    _VIRTUALS.append(value)
                    target.pop(key)
                    continue

            key_type, obj_type = key_parts
            module = globals().get(key_type, None)
            if module is None:
                # Prefix like `model.Tense` or `units.Minute`.
                #              ^^^^^^           ^^^^^^
                raise exceptions.AnalyzeError(
                    self._with_suggest_to(
                        key_type, in_=key, matches=_MODULE_HEADER_MATCHES
                    )
                )

            obj = getattr(module, obj_type, None)
            if obj is None:
                # Object like `model.Tense` or `units.Minute`
                #                    ^^^^^            ^^^^^^
                raise exceptions.AnalyzeError(
                    self._with_suggest_to(obj_type, in_=key, matches=_OBJTYPE_MATCHES)
                )

        return target


class CompilingStep(AbstractStepChain[dict[str, Any], dict[str, Any]]):
    """At this step, virtual values are added to the already converted dictionary."""

    def take_a_step(self, target: dict[str, Any]) -> dict[str, Any]:
        # <inherited docstring from :class:`AbstractStepChain`> #
        if _VIRTUALS:
            target[_BASE_SETTING_PATH][_VIRTUAL_PREFIX] = _VIRTUALS
        return target


class _ShadowStep(AbstractStepChain[dict[Hashable, Any], dict[Hashable, Any]]):
    """The shadow step, which is necessary for the chain of responsibilities to work correctly."""

    def take_a_step(self, target: dict[Hashable, Any]) -> dict[Hashable, Any]:
        # <inherited docstring from :class:`AbstractStepChain`> #
        return target


def from_tense_file_source(file_source: str, /) -> Any:
    """Parses a configuration file into a dictionary.

    Parameters:
    -----------
    file_source: :class:`str`, /
        Config file string representation.
    """
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


def from_tense_file(
    path: pathlib.Path | str,
    /,
    encoding: Optional[str] = None,
) -> Any:
    """Opens the configuration file and parses source into a dictionary.

    Parameters:
    -----------
    path: :class:`Union[pathlib.Path, str]`, /
        Path to configuration file.
    encoding: :class:`Optional[str]` = None
        File encoding.
    """
    with open(path, "r", encoding=io.text_encoding(encoding)) as file:  # type: ignore[attr-defined]
        return from_tense_file_source(file.read())
