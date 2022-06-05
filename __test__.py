def _open_config():
    with open(".tense", "r") as cfg:
        return cfg.read()


CFG = _open_config()

from tense.service_layer.dot_tense.service import step_chain

a = """
[settings]
base_unit_value = 1

[settings.unit]
case_sensitive = False  # supports lowercase booleans

[settings.unit.Minute.locale=en]
- m
- min
- mins

[settings.unit.Minute.settings]
duration = 60
"""
print(step_chain.from_tense_file(a))
# 1 - словарь + парсить значения с конвертацией -------- DONE
# 2 - обновить базовый конфиг новым, проверить как-то на валидность с помощью scheme и соеденить в 1 словарь
# 3 - создать обьекты f
