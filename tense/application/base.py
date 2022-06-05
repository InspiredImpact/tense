from tense.domain import model, units

tenses = {
    "model.Tense": {
        "base_unit_value": 1,
    },
    "units.Minute": {
        "duration": 60,
    },
    "units.Hour": {
        "duration": 60 * 60,
    },
    "units.Day": {
        "duration": 60 * 60 * 24,
    },
    "units.Week": {
        "duration": 60 * 60 * 24 * 7,
    },
    "units.Minute.aliases": [
        "m",
        "min",
        "mins",
        "minute",
        "minutes",
    ],
    "units.Hour.aliases": [
        "h",
        "hour",
        "hours",
    ],
    "units.Day.aliases": [
        "d",
        "day",
        "days",
    ],
    "units.Week.aliases": [
        "w",
        "week",
        "weeks",
    ],
}

# 0 - убрать и обработать команды
# 1 - Соединить алиасы и юниты
# 2 - Создать обьекты

def build_tense() -> model.Tense:
    ...
