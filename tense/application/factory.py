# Unit storage strategy
from tense import PARSERS


class BaseParser:
    def __init__(self, a, *, b):
        ...

    def parse(self):
        raise NotImplementedError


class InvalidParserType(Exception):
    ...


class Time:
    DATE_BOUNDED_PARSER = ...
    DIGIT_BOUNDED_PARSER = ...

    def __new__(cls, parser_cls, *args, **kwargs):
        if not issubclass(parser_cls, BaseParser):
            raise InvalidParserType(
                f"Invalid cache type, you can only use {list(PARSERS)}"
            )
        instance = parser_cls.__new__(parser_cls)
        instance.__init__(*args, **kwargs)
        return instance

    @classmethod
    def from_url(cls):
        return BaseParser


t = Time(BaseParser, 1, b=2)
