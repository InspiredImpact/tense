from typing import Iterator

import pytest
from hamcrest import assert_that, has_length, instance_of, greater_than

from aiotense.domain import model, units
from aiotense.adapters import repository

tenses = repository.TenseRepository()


@pytest.fixture(name="tense")
def tense_fixture() -> Iterator[model.Tense]:
    yield model.Tense.from_dict(tenses.source)


def test_tense_cache(tense: model.Tense) -> None:
    assert_that(tense._cached_units, has_length(0))
    for _ in tense:
        continue

    assert_that(len(tense._cached_units), greater_than(0))


def test_tense_from_dict() -> None:
    assert_that(model.Tense.from_dict(tenses.source), instance_of(model.Tense))
