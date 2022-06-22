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
from typing import Any, Callable, Iterator, cast

import parse
from behave import register_type
from behave.fixture import fixture, use_fixture_by_tag

from tense.service_layer import safe_eval

config_emulation = """
[model.Tense]

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""

config_emulation_err1 = """
[mmmodel.Tense]  # <---

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""

config_emulation_err2 = """
[model.Tense]

[virtualll]  # <---
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""

config_emulation_err3 = """
[model.Tense]

[units.MMMinute]  # <---
duration = 60
aliases = m, min, mins

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""


@parse.with_pattern(r"\d+")
def parse_number(text: str) -> int:
    return int(text)


@parse.with_pattern(r"(?i)true|false")
def parse_boolean(text: str) -> bool:
    return text.lower() == "true"


@parse.with_pattern(r"T\(\w+\)")
def parse_type(text: str) -> type:
    text = text[text.find("(") + 1 : text.find(")")]
    return cast(type, safe_eval.SafelyExpEvalute(text).safe_evalute())


register_type(Number=parse_number, Boolean=parse_boolean, Type=parse_type)


@fixture()
def config_emulation_fixture(context: Any) -> Iterator[str]:
    context.config_emulation = config_emulation
    yield config_emulation


@fixture()
def config_emulation_errors_fixture(context: Any) -> Iterator[str]:
    config_emulation_errors = (
        config_emulation_err1,
        config_emulation_err2,
        config_emulation_err3,
    )
    context.config_emulation_errors = config_emulation_errors
    yield config_emulation_errors


fixture_registry: dict[str, Callable[..., Any]] = {
    "fixture.config.emulation": config_emulation_fixture,
    "fixture.config.emulation.errors": config_emulation_errors_fixture,
}


def before_tag(context: object, tag: str) -> Any:
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
