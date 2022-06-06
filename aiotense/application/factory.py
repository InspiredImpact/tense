from __future__ import annotations

from typing import Any

from aiotense import PARSERS
from aiotense.domain import model
from aiotense.adapters import repository
from .ports import parsers
from . import exceptions

tenses = repository.TenseRepository()


class TenseParser:
    DATE = PARSERS["utcdate"]
    DIGIT = PARSERS["digit"]

    def __new__(
        cls, parser_cls: Any = DIGIT, *, tense: model.Tense = model.Tense.from_dict(tenses.source),
    ) -> parsers.AbstractParser:
        if not issubclass(parser_cls, parsers.AbstractParser):
            raise exceptions.InvalidParserType(
                f"Invalid parser type, you can only use {list(PARSERS)}."
            )
        instance = parser_cls.__new__(parser_cls)
        instance.__init__(tense=tense)
        return instance
