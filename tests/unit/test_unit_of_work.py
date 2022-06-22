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
from contextlib import AbstractContextManager

from hamcrest import assert_that, equal_to, greater_than, has_length, is_, is_in, not_

from tense.service_layer import unit_of_work as uow

from ..pyhamcrest import has_attributes, in_, subclass_of

_BASE_SETTING_GROUP = "model.Tense"
_MULTIPLIER_SETTING = "multiplier"
_SECOND_SETTING = "units.Second"
_ALIASES_SETTING = "aliases"


class TestTenseUnitOfWork:
    def test_tense_unit_of_work(self) -> None:
        assert_that(uow.TenseUnitOfWork, is_(subclass_of(uow.AbstractTenseUnitOfWork)))
        assert_that(
            uow.AbstractTenseUnitOfWork, is_(subclass_of(AbstractContextManager))
        )

        tense_uow = uow.TenseUnitOfWork()
        assert_that(tense_uow, not_(has_attributes("products")))

        with tense_uow:
            assert_that(tense_uow, has_attributes("products"))

    def test_update_config(self) -> None:
        tense_uow = uow.TenseUnitOfWork()

        with tense_uow:
            before_multiplier = tense_uow.products.config[_BASE_SETTING_GROUP][
                _MULTIPLIER_SETTING
            ]
            assert_that(before_multiplier, equal_to(1))

            tense_uow.update_config(
                {
                    _BASE_SETTING_GROUP: {
                        _MULTIPLIER_SETTING: 2,
                    }
                }
            )

            # multiplier changed
            after_multiplier = tense_uow.products.config[_BASE_SETTING_GROUP][
                _MULTIPLIER_SETTING
            ]
            assert_that(after_multiplier, equal_to(2))

            # other values are saved
            assert_that(tense_uow.products.config, has_length(greater_than(1)))

    def test_delete_aliases(self) -> None:
        from tense import units

        tense_uow = uow.TenseUnitOfWork()

        with tense_uow:
            before_second_aliases = tense_uow.products.get_setting(
                _SECOND_SETTING, _ALIASES_SETTING
            )
            assert_that("s", is_in(before_second_aliases))

            tense_uow.delete_aliases(units.Second, ["s"])
            after_second_aliases = tense_uow.products.get_setting(
                _SECOND_SETTING, _ALIASES_SETTING
            )
            assert_that("s", not_(in_(after_second_aliases)))

    def test_replace_aliases(self) -> None:
        from tense import units

        tense_uow = uow.TenseUnitOfWork()

        with tense_uow:
            before_second_aliases = tense_uow.products.get_setting(
                _SECOND_SETTING, _ALIASES_SETTING
            )
            assert_that("sec", is_in(before_second_aliases))

            tense_uow.replace_aliases(units.Second, {"sec": "ssec"})
            after_second_aliases = tense_uow.products.get_setting(
                _SECOND_SETTING, _ALIASES_SETTING
            )
            assert_that("sec", not_(in_(after_second_aliases)))
            assert_that("ssec", is_in(after_second_aliases))
