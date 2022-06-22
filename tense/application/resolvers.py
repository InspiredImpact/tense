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
"""Time resolvers.
Resolvers have a basic signature that they must match. Abstract signature
consists of two constant parameters: the first one takes a string to parse,
the second one - a `model.Tense` object as a container for aliases.

It's worth noting that resolvers must return a string iterator.

How can I create my own resolver? You can see examples in:
    - https://github.com/Animatea/aiotense/tree/main/examples
"""
from __future__ import annotations

__all__ = [
    "basic_resolver",
    "smart_resolver",
]

import re
from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from tense.domain import model

DIGIT_PATTERN: re.Pattern[str] = re.compile(r"(\d+)")


def basic_resolver(raw_str: str, _: model.Tense) -> Iterator[str]:
    """Resolves simple strings.

    !!! note
        _: :class:`model.Tense` parameter is not used here, but is required to
        match with the resolver signature.

    Examples:
    ---------
    >>> from tense import model, resolvers
    >>> from tense.adapters import repository

    >>> tense = model.Tense.from_repository(repository.TenseRepository())
    >>> list(resolvers.basic_resolver("1d1min", tense))
    ['1', 'd', '1', 'min']
    >>> list(resolvers.basic_resolver("1d 1min", tense))
    ['1', 'd', '1', 'min']
    >>> list(resolvers.basic_resolver("1d1min 2 seconds", tense))
    ['1', 'd', '1', 'min', '2', 'seconds']
    """
    return filter(
        bool,
        DIGIT_PATTERN.split(raw_str.replace(" ", "")),
    )


def smart_resolver(raw_str: str, tense: model.Tense) -> Iterator[str]:
    """Resolves complex strings.

    !!! note
        Single letter aliases are not supported.

    Examples (extends basic_resolver()):
    --------------------
    >>> from tense import model, resolvers
    >>> from tense.adapters import repository

    >>> tense = model.Tense.from_repository(repository.TenseRepository())
    >>> list(resolvers.smart_resolver("1year and 10 minutes + 5 seconds", tense))
    ['1', 'year', '10', 'min', '5', 'sec']
    """
    basic_resolve = basic_resolver(raw_str, tense)
    if any(not p.isalpha() for p in basic_resolve if not p.isdigit()):
        # Removes any char of string.punctuation
        def _resolve_p(p: str, /) -> str:
            return p if p.isdigit() else "".join(filter(str.isalpha, p))

        basic_resolve = (_resolve_p(p) for p in basic_resolver(raw_str, tense))
    else:
        basic_resolve = basic_resolver(raw_str, tense)

    unit_aliases: list[str] = sum((u.aliases for u in tense), [])
    for part in basic_resolve:
        if part.isdigit():
            yield part
            continue

        part = part.lower()  # case insensitive
        for alias in unit_aliases:
            if alias in part:
                if len(alias) == 1 and len(part) > 1:
                    # For 'd', 's', 'y', ... aliases.
                    continue
                yield alias
                break
