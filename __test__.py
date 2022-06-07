def _open_config():
    with open(".aiotense", "r") as cfg:
        return cfg.read()


CFG = _open_config()

# from aiotense.service_layer.dot_tense.step_chain import from_tense_file
#
# a = """
# [model.Tense]
# multiplier = 1
#
# [units.Minute]
# duration = 60
# aliases = m, min, mins
#
# [virtual]
# duration = 666
# aliases = alisher,
# """
# import pprint
# pprint.pprint(from_tense_file(a))

import timeit
import cProfile
from aiotense import TenseParser, TenseUnitOfWork
from aiotense.adapters import repository
from aiotense.application.ports import parsers
from aiotense.service_layer import functional
import asyncio


parser = TenseParser(TenseParser.DIGIT)
import timeit
#print(timeit.timeit("asyncio.run(parser.parse('1 min'))", globals=globals(), number=1_000))
# no - 1.1775783999910345
# yes - 0.39019660001213197
print(asyncio.run(parser.parse('1 min')))