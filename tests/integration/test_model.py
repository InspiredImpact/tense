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
from typing import Iterator

import pytest
from hamcrest import assert_that, greater_than, has_length, instance_of, is_

from tense.adapters import repository
from tense.domain import model

from ..pyhamcrest import is_dataclass, subclass_of


@pytest.fixture(name="tense_repository")
def tense_repository_fixture() -> Iterator[repository.TenseRepository]:
    yield repository.TenseRepository()


class TestTense:
    def test_tense(self) -> None:
        from collections.abc import Iterable

        assert_that(model.Tense, is_dataclass())
        assert_that(model.Tense, is_(subclass_of(Iterable)))

    def test_cache(self, tense_repository: repository.TenseRepository) -> None:
        tense = model.Tense.from_repository(tense_repository)
        assert_that(tense._cached_units, has_length(0))

        for _ in tense:
            continue

        assert_that(len(tense._cached_units), greater_than(0))

    def test_from_dict(self, tense_repository: repository.TenseRepository) -> None:
        assert_that(
            model.Tense.from_dict(tense_repository.config), instance_of(model.Tense)
        )

    def test_from_repository(
        self, tense_repository: repository.TenseRepository
    ) -> None:
        assert_that(
            model.Tense.from_repository(tense_repository), instance_of(model.Tense)
        )
