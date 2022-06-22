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
"""
!!! note
    Default `duration` attribute values are not tested because they are not constants.
"""
from collections.abc import Hashable
from typing import Iterator, Union

import pytest
from hamcrest import assert_that, has_length, is_

from tense import units

from ..pyhamcrest import is_dataclass, subclass_of


@pytest.fixture(name="mock_kwargs")
def unit_kwargs_fixture() -> Iterator[dict[str, Union[list[str], int]]]:
    yield {
        "duration": 0,
        "aliases": [],
    }


def test_unit_base(mock_kwargs: dict[str, Union[list[str], int]]) -> None:
    import warnings

    assert_that(units.Unit, is_dataclass())

    with warnings.catch_warnings(record=True) as warns:
        assert_that(warns, has_length(0))

        _ = units.Unit(**mock_kwargs)

        assert_that(warns, has_length(1))

    assert_that(units.Unit, is_(subclass_of(Hashable)))


def test_virtual_unit() -> None:
    assert_that(units.VirtualUnit, is_(subclass_of(units.Unit)))
    assert_that(units.VirtualUnit, is_dataclass())
    # Hashable dataclass
    assert_that(units.VirtualUnit, is_(subclass_of(Hashable)))


def test_second() -> None:
    assert_that(units.Second, is_(subclass_of(units.Unit)))
    assert_that(units.Second, is_dataclass())
    # Hashable dataclass
    assert_that(units.Second, is_(subclass_of(Hashable)))


def test_minute() -> None:
    assert_that(units.Minute, is_(subclass_of(units.Unit)))
    assert_that(units.Minute, is_dataclass())
    # Hashable dataclass
    assert_that(units.Minute, is_(subclass_of(Hashable)))


def test_hour() -> None:
    assert_that(units.Hour, is_(subclass_of(units.Unit)))
    assert_that(units.Hour, is_dataclass())
    # Hashable dataclass
    assert_that(units.Hour, is_(subclass_of(Hashable)))


def test_day() -> None:
    assert_that(units.Day, is_(subclass_of(units.Unit)))
    assert_that(units.Day, is_dataclass())
    # Hashable dataclass
    assert_that(units.Day, is_(subclass_of(Hashable)))


def test_week() -> None:
    assert_that(units.Week, is_(subclass_of(units.Unit)))
    assert_that(units.Week, is_dataclass())
    # Hashable dataclass
    assert_that(units.Week, is_(subclass_of(Hashable)))


def test_year() -> None:
    assert_that(units.Year, is_(subclass_of(units.Unit)))
    assert_that(units.Year, is_dataclass())
    # Hashable dataclass
    assert_that(units.Year, is_(subclass_of(Hashable)))
