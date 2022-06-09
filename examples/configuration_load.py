import asyncio

from aiotense import TenseParser, from_tense_file, from_tense_file_source

parser = TenseParser(TenseParser.DIGIT, config=from_tense_file(".aiotense"))
assert asyncio.run(parser.parse("1 decade")) > 0

config_emulation = """
[model.Tense]

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""
other_parser = TenseParser(
    TenseParser.DIGIT, config=from_tense_file_source(config_emulation)
)
assert asyncio.run(other_parser.parse("1 decade")) > 0
