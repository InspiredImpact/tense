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
    """Base class for all units of time.

    !!! info
        This dataclass implements `__hash__` method,
        if you want a subclass to inherit it, then
        specify `eq=False` in @dataclass decorator.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int`
        Unit of time duration.
    """

    aliases: list[str]
    duration: int

    def __post_init__(self) -> None:
        if self.duration <= 0:
            warnings.warn(
                "The unit duration is less than zero, the work of "
                "parsers may be incorrect. It is recommended to set "
                "the value more than zero."
            )

    def __hash__(self) -> int:
        return self.duration


@dataclass(eq=False)
class VirtualUnit(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int`
        Unit of time duration.
    """

    pass


@dataclass(eq=False)
class Second(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 1
        Unit of time duration.
    """

    duration: int = 1


@dataclass(eq=False)
class Minute(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 60
        Unit of time duration.
    """

    duration: int = 60


@dataclass(eq=False)
class Hour(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 60 * 60
        Unit of time duration.
    """

    duration: int = 60 * 60


@dataclass(eq=False)
class Day(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 60 * 60 * 24
        Unit of time duration.
    """

    duration: int = 60 * 60 * 24


@dataclass(eq=False)
class Week(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 60 * 60 * 24 * 7
        Unit of time duration.
    """

    duration: int = 60 * 60 * 24 * 7


@dataclass(eq=False)
class Year(Unit):
    """Used to create custom units of time.

    !!! info
        This subclass inherits the `__hash__` method.

    !!! warning
        If the `duration` attribute of this class is
        less than or equal to zero, then a warning will
        be generated to the console, since in this case
        the parsers may not work correctly.

    Parameters:
    -----------
    aliases: :class:`list[str]`
        Aliases of unit of time.
    duration: :class:`int` = 60 * 60 * 24 * 365
        Unit of time duration.
    """

    duration: int = 60 * 60 * 24 * 365
