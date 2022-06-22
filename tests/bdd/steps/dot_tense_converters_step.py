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
from hamcrest import assert_that, equal_to

from tense.service_layer.dot_tense import converters


@given(
    "we have {expression} and the potential {exp_type:Type} of the value it will be converted to"
)
def passing_values_to_context(context: Any, expression: str, exp_type: type) -> None:
    context.expression = expression
    context.exp_type = exp_type


@then(
    "we assert that the result of converting a certain expression corresponds to a certain type"
)
def assert_converted_type_from_expression(context: Any) -> None:
    converted_exp = converters.GetattributeParticleConverter().convert(
        context.expression
    )
    converted_exp_value = converted_exp[list(converted_exp.keys())[0]]

    assert_that(type(converted_exp_value), equal_to(context.exp_type))
