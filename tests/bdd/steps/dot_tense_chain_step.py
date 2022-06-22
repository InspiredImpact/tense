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
from functools import partial
from typing import Any

from behave import given, then
from hamcrest import assert_that, calling, instance_of, is_not, raises

from tense.service_layer.dot_tense import exceptions, step_chain
from tests.pyhamcrest import has_attributes


@given('we have "config_emulation" value')
def first_step_tests(context: Any) -> None:
    assert_that(context, has_attributes("config_emulation"))


@then(
    "we create LexingStep object and .take_a_step() method should return instance of dict"
)
def lexing_take_a_step_tests(context: Any) -> None:
    lex_step = step_chain.LexingStep().take_a_step(context.config_emulation)
    assert_that(lex_step, instance_of(dict))


@given('we have instance of str "config_emulation" value for AnalyzeStep')
def second_step_tests(context: Any) -> None:
    assert_that(context.config_emulation, instance_of(str))


@then(
    "we create AnalyzeStep object and .take_a_step() method should return instance of dict"
)
def analyze_take_a_step_tests(context: Any) -> None:
    analyze_step = step_chain.AnalyzeStep().take_a_step(
        step_chain.LexingStep().take_a_step(context.config_emulation)
    )
    assert_that(analyze_step, instance_of(dict))


@given('we have "config_emulation_errors" value')
def second_step_raises_test(context: Any) -> None:
    assert_that(context, has_attributes("config_emulation_errors"))


@then("we can make sure that when parsing each of the configs, an error will be raised")
def second_step_raises_test(context: Any) -> None:
    analyze = step_chain.AnalyzeStep().take_a_step
    for emulated_error in context.config_emulation_errors:
        emulated_error = step_chain.LexingStep().take_a_step(emulated_error)
        assert_that(
            calling(partial(analyze, emulated_error)), raises(exceptions.AnalyzeError)
        )


@given('we have instance of str "config_emulation" value for CompilingStep')
def third_step_tests(context: Any) -> None:
    assert_that(context.config_emulation, instance_of(str))


@then(
    "we create CompilingStep object and .take_a_step() method should return instance of dict"
)
def compiling_take_a_step_tests(context: Any) -> None:
    compiling_step = step_chain.CompilingStep().take_a_step(
        step_chain.AnalyzeStep().take_a_step(
            step_chain.LexingStep().take_a_step(
                context.config_emulation,
            )
        )
    )
    assert_that(compiling_step, instance_of(dict))

    context.config_emulation = compiling_step


@then("the value of virtual units will change")
def compiling_take_a_step_tests(context: Any) -> None:
    virtuals = context.config_emulation[step_chain._BASE_SETTING_PATH][
        step_chain._VIRTUAL_PREFIX
    ]
    assert_that(bool(virtuals), is_not(False))
