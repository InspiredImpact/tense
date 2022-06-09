from typing import Any, Callable, Hashable, MutableMapping

from behave import use_fixture


def use_fixture_by_tag(
    tag: str,
    context: object,
    fixture_registry: MutableMapping[Hashable, Callable[..., Any]],
) -> Any:
    fixture_data = fixture_registry.get(tag, None)
    if fixture_data is None:
        raise LookupError(f"Unknown fixture-tag: {tag}")

    fixture_func = fixture_data
    return use_fixture(fixture_func, context)
