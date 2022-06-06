def _open_config():
    with open(".aiotense", "r") as cfg:
        return cfg.read()


CFG = _open_config()

from aiotense.service_layer.dot_tense.step_chain import from_tense_file

a = """
[model.Tense]
multiplier = 1

[units.Minute]
duration = 60
aliases = m, min, mins

[virtual]
duration = 666
aliases = alisher,
"""
import pprint
pprint.pprint(from_tense_file(a))
