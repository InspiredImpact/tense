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
from aiotense.adapters.repository import TenseRepository
from aiotense.service_layer.unit_of_work import TenseUnitOfWork

repo = TenseRepository()

with TenseUnitOfWork() as uow:
    print("uow", uow.tenses.source["units.Minute"]["aliases"])

print("repo", repo.source["units.Minute"]["aliases"])

with TenseUnitOfWork() as uow:
    uow.delete_aliases("minute", ("m", "min"))
    print("edited uow", uow.tenses.source["units.Minute"]["aliases"])

print("repo after edit", repo.source["units.Minute"]["aliases"])
