from tense import TenseParser, from_tense_file, from_tense_file_source

parser = TenseParser(TenseParser.DIGIT, tenses=from_tense_file(".tense"))
assert parser.parse("1 decade") > 0

config_emulation = """
[model.Tense]

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""
other_parser = TenseParser(
    TenseParser.DIGIT,
    tenses=from_tense_file_source(config_emulation),
)
assert other_parser.parse("1 decade") > 0
