from aiotense.adapters.parsers import DigitParser, UtcDateParser

PARSERS = {
    UtcDateParser.name: UtcDateParser,
    DigitParser.name: DigitParser,
}
