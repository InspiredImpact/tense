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
"""Internationalization for time parser."""
__all__ = ["ALIASES"]

import io
import pathlib
from typing import Any, Final, Hashable, Optional

import yaml

from tense.service_layer import path_utils

_ALIASES_FILE: Final[str] = "unit_aliases.yaml"
_ALIASES_DIR: Final[pathlib.Path] = (
    path_utils.walk_up_to("memorize-it", from_=__file__) / "timeparse" / _ALIASES_FILE
)


def _open_aliases(
    path: Optional[pathlib.Path] = None,
    *,
    encoding: Optional[str] = None,
) -> dict[Hashable, Any]:
    encoding = io.text_encoding(encoding)
    if path is None:
        path = _ALIASES_DIR

    with open(path, "r", encoding=encoding) as stream:
        return yaml.safe_load(stream)


ALIASES: dict[Hashable, Any] = _open_aliases()
