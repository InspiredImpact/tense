from typing import Any

from behave import given, then
from hamcrest import assert_that, equal_to

from aiotense.service_layer.dot_tense import converters


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
