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
"""Tense factory."""
from __future__ import annotations

__all__ = ["TenseParser"]

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterator,
    Optional,
    Type,
    Union,
    overload,
)

from tense.adapters import parsers, repository
from tense.domain import model

if TYPE_CHECKING:
    from .ports import converters as abc_converters
    from .ports import repository as abc_repository

from . import exceptions, resolvers
from .ports import parsers as abc_parsers


class TenseParser:
    """Base parsers factory.

    Parameters:
    -----------
    parser_cls: :class:`Type[abc_parsers.AbstractParser]` = parsers.DigitParser
        Concrete parser type.
    tenses: :class:`Optional[abc_repository.AbstractTenseRepository]` = None, *
        Configuration repository for time parser.
    converter: :class:`Optional[abc_converters.AbstractConverter]` = None, *
        Value converter.
    time_resolver: :class:`Optional[Callable[[str, model.Tense], Iterator[str]]]` = None, *
        Raw string resolver.
    iteration_speedup: :class:`bool` = False, *
        If True, then part of the logic will be moved to the `__init__` of the class,
        which will slightly slow down the creation of an instance of the class, but
        speed up the parsing process.

    Raises:
    -------
    :class:`exceptions.InvalidParserType`
        Raises if 'parser_cls' is not subclass of :class:`abc_parsers.AbstractParser`
    """

    __slots__ = ()

    TIMEDELTA = parsers.TimedeltaParser
    DIGIT = parsers.DigitParser

    @overload
    def __new__(cls) -> abc_parsers.AbstractParser:
        ...

    @overload
    def __new__(
        cls,
        parser_cls: Type[abc_parsers.AbstractParser],
    ) -> abc_parsers.AbstractParser:
        ...

    @overload
    def __new__(
        cls,
        parser_cls: Type[abc_parsers.AbstractParser],
        *,
        tenses: Optional[abc_repository.AbstractTenseRepository],
        converter: Optional[abc_converters.AbstractConverter],
        time_resolver: Optional[Callable[[str, model.Tense], Iterator[str]]],
        iteration_speedup: bool,
    ) -> abc_parsers.AbstractParser:
        ...

    def __new__(
        cls,
        parser_cls: Type[abc_parsers.AbstractParser] = DIGIT,
        *,
        tenses: Optional[
            Union[abc_repository.AbstractTenseRepository, dict[str, Any]]
        ] = None,
        converter: Optional[abc_converters.AbstractConverter] = None,
        time_resolver: Optional[Callable[[str, model.Tense], Iterator[str]]] = None,
        iteration_speedup: bool = False,
    ) -> abc_parsers.AbstractParser:
        tense_repository_cfg = repository.TenseRepository().config
        if tenses is not None:
            tenses = tenses if isinstance(tenses, dict) else tenses.config
            tense_repository_cfg.update(tenses)

        if time_resolver is None:
            time_resolver = resolvers.basic_resolver

        if not issubclass(parser_cls, abc_parsers.AbstractParser):
            raise exceptions.InvalidParserType(
                f"Invalid parser type, you can only use {abc_parsers.AbstractParser.__subclasses__()}."
            )
        instance = parser_cls.__new__(parser_cls)  # type: ignore[call-overload]
        instance.__init__(
            tense=model.Tense.from_dict(tense_repository_cfg),
            resolver=time_resolver,
            converter=converter,
            iteration_speedup=iteration_speedup,
        )
        return instance
