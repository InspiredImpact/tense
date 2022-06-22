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
from hamcrest import assert_that, equal_to

from tense import model, resolvers
from tense.adapters import repository


@pytest.fixture(name="tense")
def tense_fixture() -> Iterator[model.Tense]:
    yield model.Tense.from_repository(repository.TenseRepository())


@pytest.mark.parametrize(
    "string_to_parse,result",
    (
        ("1d1min", ["1", "d", "1", "min"]),
        ("1d 1min", ["1", "d", "1", "min"]),
        ("1d1min 2 seconds", ["1", "d", "1", "min", "2", "sec"]),
    ),
)
def test_smart_resolver(
    string_to_parse: str, result: list[str], tense: model.Tense
) -> None:
    assert_that(
        list(resolvers.smart_resolver(string_to_parse, tense)), equal_to(result)
    )


@pytest.mark.parametrize(
    "string_to_parse,result",
    (
        ("1d1min", ["1", "d", "1", "min"]),
        ("1d 1min", ["1", "d", "1", "min"]),
        ("1d1min 2 seconds", ["1", "d", "1", "min", "2", "seconds"]),
        (
            "1year and 10 minutes + 5 seconds",
            ["1", "yearand", "10", "minutes+", "5", "seconds"],
        ),
    ),
)
def test_basic_resolver(
    string_to_parse: str, result: list[str], tense: model.Tense
) -> None:
    assert_that(
        list(resolvers.basic_resolver(string_to_parse, tense)), equal_to(result)
    )
