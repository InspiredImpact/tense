from __future__ import annotations

import copy
import dataclasses
from typing import Any, Type, Optional

from aiotense.domain import units
from aiotense.application.ports.repository import AbstractTenseRepository


class _SingleRepo:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class TenseRepository(AbstractTenseRepository, _SingleRepo):
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

    def __init__(self, source: Optional[dict[str, Any]] = None, /) -> None:
        if source is None:
            source = self._config
        super().__init__(source)

    def get_config(self) -> dict[str, Any]:
        return copy.deepcopy(self._config)

    def get_setting(self, setting: str, /) -> Any:
        return self.source[setting]

    def add_setting(self, setting: str, value: Any, /) -> None:
        if setting in self.source:
            raise KeyError(f"Key {setting!r} already exists.")
        self.source[setting] = value

    def add_virtual_unit(self, unit: units.VirtualUnit) -> None:
        self._config["model.Tense"]["virtual"].append(dataclasses.asdict(unit))

    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> None:
        self._config["model.Tense"]["virtual"].append(unit_dict)
