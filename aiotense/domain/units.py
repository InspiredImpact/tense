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
"""Tense domain."""
from __future__ import annotations

__all__ = ["Unit", "Minute", "Hour", "Day", "Week", "VirtualUnit", "Second"]

import warnings
from dataclasses import dataclass


@dataclass
class Unit:
    aliases: list[str]
    duration: int

    def __post_init__(self) -> None:
        if self.duration <= 0:
            warnings.warn(
                "The unit duration is less than zero, the work of "
                "parsers may be incorrect. It is recommended to set "
                "the value more than zero."
            )


@dataclass
class VirtualUnit(Unit):
    """Used to create custom units of time."""

    pass


@dataclass
class Second(Unit):
    duration: int = 1


@dataclass
class Minute(Unit):
    duration: int = 60


@dataclass
class Hour(Unit):
    duration: int = 60 * 60


@dataclass
class Day(Unit):
    duration: int = 60 * 60 * 24


@dataclass
class Week(Unit):
    duration: int = 60 * 60 * 24 * 7


@dataclass
class Year(Unit):
    duration: int = 60 * 60 * 24 * 365
