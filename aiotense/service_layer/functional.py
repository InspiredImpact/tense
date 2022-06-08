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
    maxsize: int = 128,
) -> Callable[[Callable[P, Awaitable[RT]]], Callable[P, Awaitable[RT]]]:
    """LRU cache wrapper for coroutines.
    A simple LRU cache that based on collections.OrderedDict where the key is the
        ~ function name + (positional arguments) + {keyword arguments}

    Parameters:
    -----------
    maxsize: :class:`int` = 128
        Cache size.
    """
    cache: OrderedDict[str, Any] = OrderedDict()

    def inner(
        fn: Callable[P, Awaitable[RT]],
    ) -> Callable[P, Coroutine[Any, Any, RT]]:
        @functools.wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
            key = getattr(fn, "__name__") + str((args, kwargs))
            if key not in cache:
                if len(cache) >= maxsize:
                    cache.popitem(last=False)

                cache[key] = await fn(*args, **kwargs)
            return cast(RT, cache[key])

        return wrapper

    return inner
