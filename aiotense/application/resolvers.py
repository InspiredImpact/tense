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
"""Time resolvers."""
from __future__ import annotations

__all__ = ["basic_resolver", "smart_resolver"]

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiotense.domain import model

DIGIT_PATTERN: re.Pattern[str] = re.compile(r"(\d+)")


def basic_resolver(raw_str: str, _: model.Tense) -> list[str]:
    """Example of supported patterns:
    * '1d1min'
    * '1d 1min'
    * '1d1min 2 seconds'
    * etc
    """
    return list(
        filter(
            bool,
            DIGIT_PATTERN.split(raw_str.replace(" ", "")),
        )
    )


def smart_resolver(raw_str: str, tense: model.Tense) -> list[str]:
    """Example of supported patterns:
    * All patterns from `resolve_time_string`
    * 1year and 10 months + 5 seconds
    * etc
    """
    basic_resolve = basic_resolver(raw_str, tense)
    unit_aliases: list[str] = sum((u.aliases for u in tense), [])
    for idx, part in enumerate(basic_resolve):
        if part.isdigit():
            continue

        for alias in unit_aliases:
            if alias in part:
                if len(alias) == 1 and len(part) > 1:
                    # For 'd', 's', 'y', ... aliases.
                    continue
                basic_resolve.pop(idx)
                basic_resolve.insert(idx, alias)

    return basic_resolve
