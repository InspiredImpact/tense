from __future__ import annotations

from typing import Any


class _VirtualUnitSingleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> _VirtualUnitSingleton:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class VirtualUnits(metaclass=_VirtualUnitSingleton):
    def add(self):