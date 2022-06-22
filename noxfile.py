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

import nox

MAIN_PKG: Final[str] = "tense"
TESTS_PKG: Final[str] = "tests"
EXAMPLES_PKG: Final[str] = "examples"

NOX_PKGS: Final[tuple[str, ...]] = (MAIN_PKG, TESTS_PKG, EXAMPLES_PKG)

DEV_REQUIREMENTS: Final[tuple[str, ...]] = ("-r", "dev-requirements.txt")


@nox.session(python=["3.9", "3.10"])
def pytest(session: nox.Session) -> None:
    session.install(*DEV_REQUIREMENTS)
    session.run("pytest")


@nox.session
def reformat_code(session: nox.Session) -> None:
    session.install(*DEV_REQUIREMENTS)
    session.run("black", "--config=pyproject.toml", *NOX_PKGS)
    session.run("isort", "--profile=black", *NOX_PKGS)
