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
"""Path utils for time parser."""
__all__ = ["walk_up_to"]

import pathlib


def walk_up_to(pathname: str, *, from_: str) -> pathlib.Path:
    current_path = pathlib.Path(from_)
    while pathname != current_path.name:
        current_path = current_path.parent

    return current_path
