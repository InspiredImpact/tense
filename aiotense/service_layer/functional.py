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
"""Functional project tools."""
__all__ = ["async_lru"]

import functools
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar, cast

P = ParamSpec("P")
RT = TypeVar("RT")


def async_lru(
    size: int = 128,
) -> Callable[[Callable[P, Awaitable[RT]]], Callable[P, Awaitable[RT]]]:
    """LRU cache wrapper for coroutines.

    Parameters:
    -----------
    size: :class:`int` = 128
        Cache size.

    !!! Sources taken from
        ~ https://gist.github.com/jaredLunde/7a118c03c3e9b925f2bf

        Typed by Animatea.

    Returns
    -------
    Callable
        Wrapped coroutine.
    """
    cache: OrderedDict[str, Any] = OrderedDict()

    def decorator(
        fn: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Coroutine[Any, Any, RT]]:
        @functools.wraps(fn)
        async def memoizer(*args: P.args, **kwargs: P.kwargs) -> RT:
            key = str((args, kwargs))
            try:
                cache[key] = cache.pop(key)
            except KeyError:
                if len(cache) >= size:
                    cache.popitem(last=False)
                cache[key] = await fn(*args, **kwargs)
            return cast(RT, cache[key])

        return memoizer

    return decorator
