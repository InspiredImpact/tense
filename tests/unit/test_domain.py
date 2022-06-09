from hamcrest import assert_that

from aiotense.domain import units
from ..pyhamcrest import subclass_of


def test_hierarchy_units() -> None:
    assert_that(units.VirtualUnit, subclass_of(units.Unit))
    assert_that(units.Second, subclass_of(units.Unit))
    assert_that(units.Minute, subclass_of(units.Unit))
    assert_that(units.Hour, subclass_of(units.Unit))
    assert_that(units.Day, subclass_of(units.Unit))
    assert_that(units.Week, subclass_of(units.Unit))
    assert_that(units.Year, subclass_of(units.Unit))
