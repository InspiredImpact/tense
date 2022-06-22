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
from typing import Any

from behave import given, then
from hamcrest import assert_that, is_

from tense.service_layer.dot_tense import domain


@given("we have target {target} for HeaderParticle")
def passing_target_value_to_context(context: Any, target: str) -> None:
    context.target = target


@given("we create HeaderParticle object")
def creating_headerparticle_object(context: Any) -> None:
    context.headerparticle = domain.HeaderParticle(context.target)


@then(
    "we call .matches() method of HeaderParticle and it result will be equal to {matches:Boolean}"
)
def calling_match_headerparticle_method(context: Any, matches: str) -> None:
    assert_that(context.headerparticle.matches(), is_(matches))


@given("we have target {target} for GetattributeParticle")
def passing_target_value_to_context(context: Any, target: str) -> None:
    context.target = target


@given("we create GetattributeParticle object")
def creating_headerparticle_object(context: Any) -> None:
    context.getattributeparticle = domain.GetattributeParticle(context.target)


@then(
    "we call .matches() method of GetattributeParticle and it result will be equal to {matches:Boolean}"
)
def calling_match_getattributeparticle_method(context: Any, matches: str) -> None:
    assert_that(context.getattributeparticle.matches(), is_(matches))
