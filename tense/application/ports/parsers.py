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
"""Interfaces that are implemented in tense.adapters."""
from __future__ import annotations

__all__ = ["AbstractParser"]

import abc
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional, final

from tense.application.ports import converters

if TYPE_CHECKING:
    from tense.domain import model


class AbstractParser(abc.ABC):
    """Interface for basic parsers.

    Parameters:
    -----------
    tense: :class:`model.Tense`, *
        Configuration repository for time parser.
    resolver: :class:`Optional[Callable[[str, model.Tense], Iterator[str]]]` = None, *
        Raw string resolver.
    converter: :class:`Optional[converters.AbstractConverter]` = None, *
        Value converter.
    iteration_speedup: :class:`bool` = False, *
        If True, then part of the logic will be moved to the `__init__` of the class,
        which will slightly slow down the creation of an instance of the class, but
        speed up the parsing process.
    """

    def __init__(
        self,
        *,
        tense: model.Tense,
        resolver: Optional[Callable[[str, model.Tense], Iterator[str]]] = None,
        converter: Optional[converters.AbstractConverter] = None,
        iteration_speedup: bool = False,
    ) -> None:
        self._tense = tense
        self._converter = converter
        self._resolver = resolver
        self._iterunits = set(tense) if iteration_speedup else tense

    @final
    def parse(self, raw_str: str, /) -> Any:
        """Base method that calls abstract ._parse().
        If the converter is not equal to None, then the value
        will be converted.

        !!! note
            This method is final and cannot be overridden.

        Parameters:
        -----------
        raw_str: :class:`str`, /
            Raw string to parse
        """
        value = self._parse(raw_str)
        if self._converter is not None:
            value = self._converter.convert(value)

        return value

    @abc.abstractmethod
    def _parse(self, raw_str: str, /) -> Any:
        """Abstract method that calls in .parse().
        Methods are implemented this way for hooks (converters, etc).

        Parameters:
        -----------
        raw_str: :class:`str`, /
            Raw string to parse.
        """
        ...

    @property
    def resolver(self) -> Optional[Callable[[str, model.Tense], Iterator[str]]]:
        """Data descriptor that returns current resolver."""
        return self._resolver

    @resolver.setter
    def resolver(
        self, new_resolver: Callable[[str, model.Tense], Iterator[str]], /
    ) -> None:
        """Sets new resolver.

        When sets a new resolver, make sure it matches the base signature of
        all resolvers (2 arguments, the first one takes a string, the second
        one takes a model.Tense object).
        Otherwise, parsers may work incorrectly, or even give an unexpected error.

        !!! dunger
            new_resolver must be callable.
        """
        if not callable(new_resolver):
            raise ValueError("Resolver must be callable.")
        self._resolver = new_resolver
