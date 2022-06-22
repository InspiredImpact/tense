from tense import TenseParser

time_string = "1min10second 1 second"

digit_parser = TenseParser(TenseParser.DIGIT)  # returns int
assert digit_parser.parse(time_string) == 71

delta_parser = TenseParser(TenseParser.TIMEDELTA)  # returns datetime.timedelta
assert str(delta_parser.parse(time_string)) == "0:01:11"
