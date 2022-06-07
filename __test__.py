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
from aiotense import TenseParser
parser = TenseParser(TenseParser.DIGIT)
import asyncio

async def _parse_alisher(some_str: str) -> int:
    return await parser.parse(some_str)

async def run(coro_func):
    results = []
    for _ in range(1_000_000):
        s = timeit.default_timer()
        await coro_func("1 alisher")
        e = timeit.default_timer()
        results.append(e-s)
    print(sum(results) / len(results))

async def test(a):  # 1.5078479872317983e-07  # 2.492795797021245e-06 # 2.3552455006429228e-06
    ...
# 0.0010063999943668023  # 0.000890900002559647

asyncio.run(run(parser.parse))
