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
""" """
__all__ = ["HashableParticle", "HeaderParticle", "GetattributeParticle"]

import abc
from typing import cast


class HashableParticle(abc.ABC):
    def __init__(self, target: str) -> None:
        self.target = target

    def __hash__(self) -> int:
        return hash(self.target)

    @abc.abstractmethod
    def matches(self) -> bool:
        ...

    @classmethod
    def matches_converter(cls, converter: type | object) -> bool:
        if not hasattr(converter, "__name__"):
            converter = converter.__class__

        converter = cast(type, converter)
        return cls.__name__ in converter.__name__


class HeaderParticle(HashableParticle):
    def matches(self) -> bool:
        return self.target.startswith("[") and self.target.endswith("]")

    @staticmethod
    def strip_header(header: str) -> str:
        return header[1:-1]


class GetattributeParticle(HashableParticle):
    def matches(self) -> bool:
        return len(self.target.split("=")) > 1
