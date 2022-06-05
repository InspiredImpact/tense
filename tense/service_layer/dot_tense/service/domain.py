__all__ = ["HashableParticle", "HeaderParticle", "GetattributeParticle", "ListParticle"]

import abc


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


class ListParticle(HashableParticle):
    def matches(self) -> bool:
        return "-" in self.target or len(self.target.split(",")) > 1

    def is_comma_list(self) -> bool:
        return "-" not in self.target
