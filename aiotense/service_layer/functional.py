__all__ = ["async_lru"]

import functools
from collections import OrderedDict
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar, cast

P = ParamSpec("P")
RT = TypeVar("RT")


def async_lru(
    size: int = 128,
) -> Callable[[Callable[P, Awaitable[RT]]], Callable[P, Awaitable[RT]]]:
    """
    !!! Sources taken from
        ~ https://gist.github.com/jaredLunde/7a118c03c3e9b925f2bf
    """
    cache: OrderedDict[str, Any] = OrderedDict()

    def decorator(
        fn: Callable[P, Awaitable[RT]]
    ) -> Callable[P, Coroutine[Any, Any, RT]]:
        @functools.wraps(fn)
        async def memoizer(*args: P.args, **kwargs: P.args) -> RT:
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
