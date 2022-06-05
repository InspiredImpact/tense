def _open_config():
    with open(".tense", "r") as cfg:
        return cfg.read()


CFG = _open_config()

from tense.service_layer.dot_tense.service import step_chain

a = """
[model.Tense]
base_unit_value = 1

[units.Minute]
duration = 60

[units.Minute.aliases]
m, min, mins
# or
- m
- min
- mins

[commands.register_unit.Decade]
duration = units.Year.duration * 10

[units.Decade.aliases]
- decade
- decades
- decs
- dec
"""
