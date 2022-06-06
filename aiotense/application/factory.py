from __future__ import annotations

import copy
import dataclasses
from typing import Any

from aiotense import PARSERS
from aiotense.domain import model, units

from .ports import parsers


class InvalidParserType(Exception):
    ...


class TenseHandler:
    _config = {
        "model.Tense": {
            "multiplier": 1,
            "virtual": [],
        },
        "units.Minute": {
            "duration": 60,
            "aliases": [
                "m",
                "min",
                "mins",
                "minute",
                "minutes",
            ],
        },
        "units.Hour": {
            "duration": 60 * 60,
            "aliases": [
                "h",
                "hour",
                "hours",
            ],
        },
        "units.Day": {
            "duration": 60 * 60 * 24,
            "aliases": [
                "d",
                "day",
                "days",
            ],
        },
        "units.Week": {
            "duration": 60 * 60 * 24 * 7,
            "aliases": [
                "w",
                "week",
                "weeks",
            ],
        },
    }

    def create(self) -> model.Tense:
        tense_attrs = {}
        for key, attrs in self._config.items():
            module, cls_name = key.split(".")
            module = globals()[module]
            cls = getattr(module, cls_name)

            if cls is model.Tense:
                if not isinstance(attrs, dict):
                    continue

                tense_attrs.update(attrs)
                continue

            tense_attrs[cls_name.lower()] = cls(**attrs)
            continue

        return model.Tense(**tense_attrs)

    def change_existing(self, key, value):
        if key not in self._config:
            raise KeyError(f"Key {key} not found.")

        self._config[key] = value

    def get_config(self):
        return copy.deepcopy(self._config)

    def set_config(self, config):
        if "model.Tense" not in config:
            raise ValueError(f"Needs to implement 'model.Tense' key.")

        self._config = config

    def add_virtual_unit(self, unit: units.VirtualUnit) -> None:
        self._config["model.Tense"]["virtual"].append(dataclasses.asdict(unit))

    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> None:
        self._config["model.Tense"]["virtual"].append(unit_dict)


tenses = TenseHandler()


class TenseParser:
    DATE = PARSERS["utcdate"]
    DIGIT = PARSERS["digit"]

    def __new__(
        cls, parser_cls: Any = DIGIT, *, tense: model.Tense = tenses.create(),
    ) -> parsers.AbstractParser:
        if not issubclass(parser_cls, parsers.AbstractParser):
            raise InvalidParserType(
                f"Invalid parser type, you can only use {list(PARSERS)}."
            )
        instance = parser_cls.__new__(parser_cls)
        instance.__init__(tense=tense)
        return instance
