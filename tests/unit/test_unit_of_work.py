from contextlib import AbstractContextManager

from hamcrest import assert_that, equal_to, is_, is_in, not_

from aiotense.service_layer import unit_of_work as uow

from ..pyhamcrest import has_attributes, in_, subclass_of


def test_hierarchy() -> None:
    assert_that(uow.AbstractTenseUnitOfWork, is_(subclass_of(uow.AbstractUnitOfWork)))
    assert_that(uow.TenseUnitOfWork, is_(subclass_of(uow.AbstractTenseUnitOfWork)))


def test_syntax_sugar() -> None:
    assert_that(uow.AbstractTenseUnitOfWork, is_(subclass_of(AbstractContextManager)))


def test_basic() -> None:
    with uow.TenseUnitOfWork() as tense_uow:
        assert_that(tense_uow, has_attributes("tenses"))


class TestAtomicOperations:
    def test_update_config(self) -> None:
        with uow.TenseUnitOfWork() as tense_uow:
            # Before update
            model_tense = tense_uow.tenses.source["model.Tense"]
            assert_that(model_tense["multiplier"], equal_to(1))  # By default

            tense_uow.update_config({"model.Tense": {"multiplier": 2}})

            # After update
            model_tense = tense_uow.tenses.source["model.Tense"]
            assert_that(model_tense["multiplier"], equal_to(2))

    def test_delete_aliases(self) -> None:
        with uow.TenseUnitOfWork() as tense_uow:
            # Before delete
            second = tense_uow.tenses.source["units.Second"]
            assert_that("s", is_in(second["aliases"]))

            tense_uow.delete_aliases("second", ("s",))

            # After delete
            second = tense_uow.tenses.source["units.Second"]
            assert_that("s", not_(in_(second["aliases"])))

    def test_replace_aliases(self) -> None:
        with uow.TenseUnitOfWork() as tense_uow:
            # Before replace
            second = tense_uow.tenses.source["units.Second"]
            assert_that("sec", is_in(second["aliases"]))

            tense_uow.replace_aliases("second", {"sec": "ssec"})

            # After replace
            second_aliases = tense_uow.tenses.source["units.Second"]["aliases"]
            assert_that("sec", not_(in_(second_aliases)))
            assert_that("ssec", is_in(second_aliases))
