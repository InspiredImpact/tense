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
"""Aiotense factory."""
from __future__ import annotations

__all__ = ["TenseParser"]

from typing import TYPE_CHECKING, Any, Type, Callable, Optional

from aiotense.adapters import parsers, repository
from aiotense.domain import model

if TYPE_CHECKING:
    from aiotense.application.ports import converters, parsers

from . import exceptions, resolvers
from .ports import parsers as abc_parsers

_tenses = repository.TenseRepository()


class TenseParser:
    """Base parsers factory.

    Parameters:
    -----------
    parser_cls: :class:`Any` = DIGIT
        Concrete parser type.
    tense: :class:`model.Tense` = model.Tense.from_dict(_tenses.config), *
        Configuration for concrete parser.

    Raises:
    -------
    :class:`exceptions.InvalidParserType`
        Raises if 'parser_cls' is not subclass of :class:`abc_parsers.AbstractParser`
    """

    TIMEDELTA = parsers.TimedeltaParser
    DIGIT = parsers.DigitParser

    def __new__(
        cls,
        parser_cls: Type[parsers.AbstractParser] = DIGIT,
        *,
        config: Optional[dict[str, Any]] = None,
        converter: Optional[converters.AbstractConverter] = None,
        time_resolver: Optional[Callable[[str, model.Tense], list[str]]] = None,
    ) -> abc_parsers.AbstractParser:
        if config is not None:
            _tenses._config.update(config)

        if time_resolver is None:
            time_resolver = resolvers.basic_resolver

        if not issubclass(parser_cls, abc_parsers.AbstractParser):
            raise exceptions.InvalidParserType(
                f"Invalid parser type, you can only use {parsers.__all__}."
            )
        instance = parser_cls.__new__(parser_cls)
        instance.__init__(
            tense=model.Tense.from_dict(_tenses.config),
            resolver=time_resolver,
            converter=converter,
        )
        return instance
