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
"""Adapters of aiotense.application.ports."""
from __future__ import annotations

__all__ = ["TenseRepository"]

import copy
import dataclasses
from typing import Any, Optional, Type

from aiotense.application.ports.repository import AbstractTenseRepository
from aiotense.domain import units


class TenseRepository(AbstractTenseRepository):
    # <inherited docstring from :class:`TenseRepository`> #
    _tense_config: dict[str, Any] = {
        "model.Tense": {
            "multiplier": 1,
            "virtual": [],
        },
        "units.Second": {
            "duration": 1,
            "aliases": [
                "s",
                "sec",
                "secs",
                "second",
                "seconds",
            ],
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
        "units.Year": {
            "duration": 60 * 60 * 24 * 365,
            "aliases": [
                "y",
                "year",
                "years",
            ],
        },
    }

    def __init__(self, config: Optional[dict[str, Any]] = None, /) -> None:
        if config is None:
            config = self._tense_config
        super().__init__(config)

    def get_config(self) -> dict[str, Any]:
        return copy.deepcopy(self._config)

    def get_setting(self, path: str, setting: str, /) -> Any:
        return self._config[path][setting]

    def add_virtual_unit(self, unit: units.VirtualUnit) -> TenseRepository:
        # <inherited docstring from :class:`TenseRepository`> #
        self._config["model.Tense"]["virtual"].append(dataclasses.asdict(unit))
        return self

    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> TenseRepository:
        # <inherited docstring from :class:`TenseRepository`> #
        self._config["model.Tense"]["virtual"].append(unit_dict)
        return self

    def add_aliases_to(
        self, unit: Type[units.Unit], aliases: list[str]
    ) -> TenseRepository:
        # <inherited docstring from :class:`TenseRepository`> #
        self._config["units." + unit.__name__]["aliases"].extend(aliases)
        return self
