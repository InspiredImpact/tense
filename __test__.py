# import asyncio
# from aiotense import TenseParser
#
# time_string = "1d2minutes 5 sec"
#
# digit_parser = TenseParser(TenseParser.DIGIT)
# a = asyncio.run(digit_parser.parse(time_string)) # 86525
# print(a)
#
# delta_parser = TenseParser(TenseParser.TIMEDELTA)
# a = asyncio.run(delta_parser.parse(time_string)) # 1 day, 0:02:05
# print(a)
import asyncio
from aiotense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]  # Этот заголовок обязателен.

[units.Year]
duration = exp(year)
aliases = год, лет

[units.Second]
duration = exp(second)
aliases = с, сек, секунд

[virtual]
duration = exp(year * 10)
aliases = десятилетие, десятилетий
"""

parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
)
delta_value = asyncio.run(parser.parse("1год 10 десятилетий5   секунд"))
# <-- Assertions -->
assert str(delta_value) == "36865 days, 0:00:05"
# Wait
# import asyncio
# from aiotense import TenseParser, from_tense_file_source
#
# config_emulation = """
# [model.Tense]
# multiplier = 2  # each unit of time will be multiplied by 2
# # !!! Note: If the multiplier is <= 0, then the parsers will
# # not work correctly. In this case, a warning will be sent to the console.
#
# [units.Minute]
# duration = 120  # Why not?...
# aliases = my_minute, my_minutes, my_min, my_mins
# """
# parser = TenseParser(
#     TenseParser.TIMEDELTA,
#     config=from_tense_file_source(config_emulation),
# )
# delta_value = asyncio.run(parser.parse("1 my_min 10my_mins 9  my_minutes"))
# print(str(delta_value))  # 1:20:00 (each 120 * 2)
