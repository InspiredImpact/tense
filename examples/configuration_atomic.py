from aiotense.adapters import repository
from aiotense import TenseUnitOfWork

tenses = repository.TenseRepository()
# By default `multiplier`=1
assert tenses.source["model.Tense"]["multiplier"] == 1

with TenseUnitOfWork() as uow:
    # Updating `multiplier` setting
    uow.update_config({"model.Tense": {"multiplier": 2}})
    # Works.
    assert tenses.source["model.Tense"]["multiplier"] == 2

with TenseUnitOfWork() as uow:
    # By default `s` is alias of `units.Second`.
    initial_aliases = tenses.source["units.Second"]["aliases"]
    assert "s" in initial_aliases

    # Replacing alias `s` to `ss`
    uow.replace_aliases("second", {"s": "ss"})
    # Works.
    assert "s" not in initial_aliases
    assert "ss" in initial_aliases

with TenseUnitOfWork() as uow:
    # By default `s` and `second` are aliases of `units.Second`.
    initial_aliases = tenses.source["units.Second"]["aliases"]
    assert "s" in initial_aliases
    assert "second" in initial_aliases

    # Deleting `s` and `second` aliases
    uow.delete_aliases("second", ("s", "second",))
    # Works.
    assert "s" not in initial_aliases
    assert "second" not in initial_aliases
