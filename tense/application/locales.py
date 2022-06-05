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
"""Application locale functions."""
from __future__ import annotations

__all__ = ["build_locale_from_string"]

from typing import TYPE_CHECKING

from tense.domain import model, units
from tense.i18n import i18n

if TYPE_CHECKING:
    from tense import types


def build_locale_from_string(locale_string: types.LocaleType) -> locale.Locale:
    _i18n = i18n.ALIASES[locale_string]
    return locale.Locale(
        minute=units.Minute(aliases=_i18n["minute"]),
        hour=units.Hour(aliases=_i18n["hour"]),
        day=units.Day(aliases=_i18n["day"]),
        week=units.Week(aliases=_i18n["week"]),
    )
