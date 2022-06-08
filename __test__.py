# def _open_config():
#     with open(".aiotense", "r") as cfg:
#         return cfg.read()
#
#
# CFG = _open_config()
#
from aiotense import from_tense_file

print(from_tense_file(".aiotense"))
# from aiotense import from_tense_file_source
#
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
# duration = exp(hour * minute)
# aliases = alisher,
# """
# import pprint
# pprint.pprint(from_tense_file_source(a))
# from aiotense.domain import model
# from aiotense.adapters import repository
# from aiotense import TenseParser, TenseUnitOfWork
#
# tenses = repository.TenseRepository()
# with TenseUnitOfWork() as uow:
#     uow.update_config(from_tense_file_source(a))
#
# with TenseParser(TenseParser.DIGIT) as tense_parser:
#     tense_parser.update_config(from_tense_file_source(a))
#
# parser = TenseParser(TenseParser.DIGIT, tense=model.Tense.from_dict(tenses.source))
# import asyncio
# print(asyncio.run(parser.parse("1 alisher")))
