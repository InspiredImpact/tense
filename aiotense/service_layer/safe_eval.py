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
"""Safely expression execution tool."""
__all__ = ["SafelyExpEvalute"]

import copy
import sys
import textwrap
import traceback
import types
from dataclasses import dataclass, field
from typing import Any, Final

_TAB: Final[str] = " " * 4


def _base_exc_format(exc: BaseException) -> str:
    """Returns formatted error object by traceback."""
    return "\n".join(
        traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__,
        )
    )


@dataclass
class SafelyExpEvalute:
    """Class that represents safely expression evalute tool.

    Parameters:
        exp: :class:`str`
            Expression string.

        eval_locals: :class:`dict[str, Any]` = dict()
            Locals for expression execution.

        frame: :class:`types.FrameType` = sys._getframe(0)
            Frame for safely evalute.

    Examples:
        # Base operations.
        >>> exp = "2 + 2 * 2"
        >>> assert SafelyExpEvalute(exp).safe_evalute() == 6

        # Flexible.
        >>> deps = {"minute": 60}
        >>> exp = "minute * 60"
        >>> assert SafelyExpEvalute(exp, eval_locals=deps).safe_evalute() == 3600
    """
    exp: str
    eval_locals: dict[str, Any] = field(default_factory=dict)
    frame: types.FrameType = field(default=sys._getframe(0))

    def __post_init__(self) -> None:
        self._add_expression_to_func()

    def _evaldict(self) -> dict[str, Any]:
        """Safe dictionary generation to avoid conflicts with globals()."""
        frame = self.frame
        safely_dict = copy.copy(frame.f_globals)
        safely_dict.update(frame.f_locals)
        return safely_dict

    def _add_expression_to_func(self) -> None:
        """Adding expression to func body."""
        deps = {
            "func_name": self.func_name,
            "exp": textwrap.indent("return" + " " + self.exp, _TAB),
        }
        self._exp = "def {func_name}():\n{exp}".format(**deps)

    def safe_evalute(self) -> Any:
        """Safely exp execution method."""
        evaldict = self._evaldict()
        try:
            code = compile(self._exp, self.frame.f_code.co_filename, "single")
            if self.eval_locals:
                evaldict.update(self.eval_locals)

            exec(code, evaldict)
        except BaseException as exc:
            return _base_exc_format(exc)

        func = evaldict[self.func_name]
        return func()

    @property
    def func_name(self) -> str:
        """Returns unique func name to avoid recursion."""
        return "__" + self.__class__.__name__.lower()
