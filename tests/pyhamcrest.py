from __future__ import annotations

__all__ = ["subclass_of", "has_attributes", "in_"]

from typing import TYPE_CHECKING, Any, Optional, Sequence

from hamcrest.core.base_matcher import BaseMatcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description


class IsSubclassOf(BaseMatcher):
    def __init__(self, subclass_of: type, /) -> None:
        self._subcls_of = subclass_of
        self.failed: Optional[str] = None

    def _matches(self, cls: Any) -> bool:
        result = issubclass(cls, self._subcls_of)
        if not result:
            self.failed = cls
        return result

    def describe_to(self, description: Description) -> None:
        (
            description.append_text("failing on ").append_text(
                f"<{self.failed}> attribute"
            )
        )


class HasAttributes(BaseMatcher):
    def __init__(self, *attrs: str) -> None:
        self.attrs = attrs
        self.failed: Optional[str] = None

    def _matches(self, obj: Any) -> bool:
        for attr in self.attrs:
            if not hasattr(obj, attr):
                self.failed = attr
                return False
        return True

    def describe_to(self, description: Description) -> None:
        (
            description.append_text("failing on ").append_text(
                f"<{self.failed}> attribute"
            )
        )


class In(BaseMatcher):
    def __init__(self, seq: Sequence[Any]) -> None:
        self.seq = seq
        self.failed: Optional[str] = None

    def _matches(self, obj: Any) -> bool:
        result = obj in self.seq
        if not result:
            self.failed = obj
        return result

    def describe_to(self, description: Description) -> None:
        (
            description.append_text("failing on ").append_text(
                f"<{self.failed}> attribute"
            )
        )


def subclass_of(subcls_of: type, /) -> IsSubclassOf:
    return IsSubclassOf(subcls_of)


def has_attributes(*attributes: str) -> HasAttributes:
    return HasAttributes(*attributes)


def in_(seq: Sequence[Any], /) -> In:
    return In(seq)
