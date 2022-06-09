import asyncio

from aiotense import TenseParser, resolvers
from aiotense.domain import units
from aiotense.adapters import repository

tenses = repository.TenseRepository()
tenses2 = repository.TenseRepository()


def singleton_demonstration() -> None:
    assert not tenses.get_setting("model.Tense", "virtual")  # no virtual units by default

    tenses.add_virtual_unit_dict({"duration": 100, "aliases": ["custom_virtual"]})
    assert tenses2.get_setting("model.Tense", "virtual")  # +1 virtual from ~tenses to ~tenses2


def add_virtual_units_demonstration() -> None:
    tenses.add_virtual_unit(
        units.VirtualUnit(
            aliases=["decade", "decades"],
            duration=60 * 60 * 24 * 365 * 10,
        )
    )
    # or in other way:
    tenses.add_virtual_unit_dict(
        {
            "aliases": ["century"],
            "duration": 60 * 60 * 24 * 365 * 100,
        }
    )

    integration_time_string = "1 century and 2 decades"
    parser = TenseParser(
        TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver,
    )

    assert asyncio.run(parser.parse(integration_time_string)).days > 0


if __name__ == "__main__":
    singleton_demonstration()
    add_virtual_units_demonstration()
