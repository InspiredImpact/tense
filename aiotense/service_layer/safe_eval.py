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
    return "\n".join(
        traceback.format_exception(
            type(exc),
            exc,
            exc.__traceback__,
        )
    )


@dataclass
class SafelyExpEvalute:
    exp: str
    eval_locals: dict[str, Any] = field(default_factory=dict)
    frame: types.FrameType = field(default=sys._getframe(0))

    def __post_init__(self) -> None:
        self._add_expression_to_func()

    def evaldict(self) -> dict[str, Any]:
        frame = self.frame
        safely_dict = copy.copy(frame.f_globals)
        safely_dict.update(frame.f_locals)
        return safely_dict

    def _add_expression_to_func(self) -> None:
        deps = {
            "func_name": self.func_name,
            "exp": textwrap.indent("return" + " " + self.exp, _TAB),
        }
        self._exp = "def {func_name}():\n{exp}".format(**deps)

    def safe_evalute(self) -> Any:
        evaldict = self.evaldict()
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
        return "__" + self.__class__.__name__.lower()
