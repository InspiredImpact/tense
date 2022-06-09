from typing import Any

from behave import given, then
from hamcrest import assert_that, is_

from aiotense.service_layer.dot_tense import domain


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
