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
from typing import Any, Iterator, Union

import pytest
from hamcrest import assert_that, greater_than

from tense import TenseParser, from_tense_file, resolvers
from tense.adapters import repository
from tense.application.ports import converters as abc_converters

from ..pyhamcrest import has_attributes

_TENSE_FILEDIR = "tests/e2e/.tense"


class DoubleConverter(abc_converters.AbstractConverter[Union[int, float]]):
    def convert(self, value: Any) -> Union[int, float]:
        if not isinstance(value, (int, float)):
            return NotImplemented
        return value * 2


@pytest.fixture(name="converter_mock")
def converter_mock_fixture() -> Iterator[DoubleConverter]:
    yield DoubleConverter()


def test_basic_tense_ui() -> None:
    assert_that(TenseParser, has_attributes("DIGIT"))
    assert_that(TenseParser, has_attributes("TIMEDELTA"))

    parser = TenseParser(
        TenseParser.DIGIT,
        tenses=repository.TenseRepository(from_tense_file(_TENSE_FILEDIR)),
    )

    assert_that(parser.parse("1 decade"), greater_than(0))


def test_advanced_tense_ui(converter_mock: DoubleConverter) -> None:
    parser = TenseParser(
        TenseParser.DIGIT,
        tenses=repository.TenseRepository(from_tense_file(_TENSE_FILEDIR)),
        converter=converter_mock,
        time_resolver=resolvers.smart_resolver,
    )
    assert_that(parser.parse("1decade + 1decade"), greater_than(0))
