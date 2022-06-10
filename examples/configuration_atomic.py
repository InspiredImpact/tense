from aiotense import unit_of_work, units

with unit_of_work.TenseUnitOfWork() as uow:
    # Updating `multiplier` setting
    uow.update_config({"model.Tense": {"multiplier": 2}})
    # Works.
    assert uow.tenses.config["model.Tense"]["multiplier"] == 2

with unit_of_work.TenseUnitOfWork() as uow:
    # By default `s` is alias of `units.Second`.
    initial_aliases = uow.tenses.config["units.Second"]["aliases"]
    assert "s" in initial_aliases

    # Replacing alias `s` to `ss`
    uow.replace_aliases(units.Second, {"s": "ss"})
    # Works.
    assert "s" not in initial_aliases
    assert "ss" in initial_aliases

with unit_of_work.TenseUnitOfWork() as uow:
    # By default `s` and `second` are aliases of `units.Second`.
    initial_aliases = uow.tenses.config["units.Second"]["aliases"]

    assert "ss" in initial_aliases
    assert "second" in initial_aliases

    # Deleting `s` and `second` aliases
    uow.delete_aliases(
        units.Second,
        (
            "ss",
            "second",
        ),
    )
    # Works.
    assert "ss" not in initial_aliases
    assert "second" not in initial_aliases
