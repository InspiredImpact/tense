import asyncio

from aiotense import TenseParser

time_string = "1min10second 1 second"

digit_parser = TenseParser(TenseParser.DIGIT)  # return int
assert asyncio.run(digit_parser.parse(time_string)) == 71

delta_parser = TenseParser(TenseParser.TIMEDELTA)  # returns datetime.timedelta
assert str(asyncio.run(delta_parser.parse(time_string))) == "0:01:11"
