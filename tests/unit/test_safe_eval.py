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
from typing import Final

from hamcrest import assert_that, equal_to, is_in

from tense.service_layer import safe_eval

_CONSTANT: Final[float] = 3.14
_CONSTANT_NAME: Final[str] = "_CONSTANT"


def test_eval_basics() -> None:
    exp = "2 + 2 * 2"
    assert_that(safe_eval.SafelyExpEvalute(exp).safe_evalute(), equal_to(6))


def test_eval_flexibility() -> None:
    deps = {"minute": 60}
    exp = "minute * 60"
    assert_that(
        safe_eval.SafelyExpEvalute(exp, eval_locals=deps).safe_evalute(), equal_to(3600)
    )


def test_eval_safety() -> None:
    from operator import itemgetter

    safe_eval.SafelyExpEvalute(f"globals().pop('{_CONSTANT_NAME}')")
    assert_that(_CONSTANT_NAME, is_in(globals()))

    safe_eval.SafelyExpEvalute("delattr(__builtins__, 'int')")
    assert_that(itemgetter("int")(__builtins__), equal_to(int))
