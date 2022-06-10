<img src="../doc_assets/tense-logo.jpg" align="left" width="200px"/>
Project: aiotense
<br>
License: Apache 2.0
<br>
About: Time Processing Tool
<br>
OS: Independent
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Topic: Utilities
<br />
    <p align="center">
    <br />
    <a href="https://pypi.org/project/aiotense/">PyPi</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Report Bug</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Request Feature</a>
    </p>

# What is aiotense?
`aiotense` - time parsing tool. Did you need to convert the string 
like "1day1minute 20 seconds" in number of seconds or a datetime.timedelta object? No? 
Then recommend us to your friends :) And if you are still here - let's continue!

# How is aiotense designed?
`aiotense` designed to provide maximum **flexibility**, **practicality** and **convenience** to the user.
Some logic is imported immediately as a class or function:
```py
from aiotense import TenseParser, from_tense_file, from_tense_file_source
```
And some parts are imported as modules:
```py
from aiotense import units, model, unit_of_work, resolvers, ...
from aiotense.adapters import repository
```
Such an interface is made to avoid any cyclic imports and is the main style of the project.

# Quick-Start
Let's start with the basics, let's say we have a string "1day1minute 20 seconds", how do we convert it to,
as previously stated, the number of seconds or a datetime.timedelta object?
- Let's consider!
```py
import asyncio
from aiotense import TenseParser

time_string = "1day1minute 20 seconds"

parser = TenseParser(TenseParser.DIGIT)
assert asyncio.run(parser.parse(time_string)) == 86480  # It works.
```

# How does Tense Parser work?
```py
TenseParser.__new__(
    cls,
    parser_cls: parsers.AbstractParser = DIGIT,
    *,
    config: Optional[dict[str, Any]] = None,
    converter: Optional[converters.AbstractConverter] = None,
    time_resolver: Optional[Callable[[str, model.Tense], list[str]]] = None,
) -> abc_parsers.AbstractParser:
```

[See to github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/factory.py#L33-L76)

The first argument to `TenseParser` is a subclass of *aiotense.application.ports.parsers.AbstractParser*.
Initially, there are already some ready-made implementations, such as **TenseParser.DIGIT** - aiotense.adapters.parsers.DigitParser
and **TIMEDELTA** - aiotense.adapters.parsers.TimedeltaParser.

!!! note
    You can also create your own custom parsers inheriting **aiotense.application.ports.parsers.AbstractParser**

In `TenseParser.__new__` there is a little "processing" of values that will be passed later
into the **...AbstractParser** subclass initializers, we end up with a finished **...AbstractParser** subclass.

# Why is my string not being parsed?
If your string is something along the lines of "1 day + 2 minutes and 5 seconds", then most likely you will have
only the last value is converted. Ask why so? - It's about **resolver** (time_resolver).
By default, there is a resolver that does an excellent job with primitive strings, this string is
complex (see terms at the end of the FAQ).

In addition to the "primitive" resolver, which is the default, there is also a "smart" one.

!!! info
     aiotense.application.resolvers.smart_resolver() is also case insensitive.

[See to github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/resolvers.py#L28-L63)

!!! note
    Just like with parsers, you can create **your** custom resolver, just don't forget
    that the resolver has a base signature (arg1: str, arg2: model.Tense).

```py
>>> import asyncio
>>> from aiotense import TenseParser, resolvers

>>> time_string = "1 day + 2 minutes and 5seconds"

>>> parser = TenseParser(
...     TenseParser.DIGIT, 
...     time_resolver=resolvers.smart_resolver,
... )
>>> asyncio.run(parser.parse(time_string))
86525
```
# What is the "converter" argument of TenseParser?
The ...AbstractParser class has a parse method that cannot be overridden. In this method
before returning a value, the implementation of the abstract method ._parse() from subclasses is called, the value
which is converted in accordance with the specified converter, if it is not equal to None.

!!! note
    We try to make `aiotense` as flexible as possible, so almost every hook you can
    implement in your own way and transfer to the appropriate place. Converter is no exception, you
    you can create your own custom one by first deriving it from aiotense.application.ports.converters.AbstractConverter.
    Also worth considering is the fact that ...AbstractConverter is a generic that accepts a value type,
    which will be returned as a result of the conversion (it is also returned in the abstract .convert() method).

# What about delete/replace aliases?
Atomic operations in `aiotense` are implemented by the **UnitOfWork** pattern, which in turn interacts with
alias repository.

!!! info "Let's take a closer look"
    === "Removing aliases"
    ```py
    # <--- Syntax sugar "with" allows you to break sections of code into logical blocks ---> #
    from aiotense import unit_of_work, units
    
    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Converted the type of time unit to the path for the config
        assert "second" in uow.tenses.get_setting(second_str, "aliases")  # Default "second" alias in units.Second aliases
    
        uow.delete_aliases(units.Second, ["second"])  # Remove alias from units.Second
    
        assert "second" not in uow.tenses.get_setting(second_str, "aliases")  # Alias has been removed.
    ```
    === "Replacing aliases"
    ```py
    from aiotense import unit_of_work, units

    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Converted the type of time unit to the path for the config
        assert "second" in uow.tenses.get_setting(second_str,
                                                  "aliases")  # Default "second" alias in units.Second aliases
    
        uow.replace_aliases(units.Second, {"second": "other_second"})  # Change alias "second" to "second"
        
        alias_state = uow.tenses.get_setting(second_str, "aliases")  # Get alias state after replacement
        assert "second" not in alias_state  # Alias "second" removed
        assert "other_second" in alias_state  # Instead of "second" there is a new alias - "other_second"
    ```

    __Next, we pass the repository sources to TenseParser(config=uow.tenses.config)__

# How to add custom time units?
For custom time units, aiotense.domain.units has a separate class - VirtualUnit. He is no different
from ..Unit, but useful for logically separating virtual units from base units, and possibly new ones in the near future
functionality.

```py
import asyncio
from aiotense import TenseParser, units
from aiotense.adapters import repository

tenses = repository.TenseRepository()
(
    tenses.add_virtual_unit(
        units.VirtualUnit(aliases=["twoseconds"], duration=2)
    )
    # or
    .add_virtual_unit_dict(  # TypedDict
        {"aliases": ["threeseconds"], "duration": 3}
    )
)

parser = TenseParser(TenseParser.DIGIT, config=tenses.config)
assert asyncio.run(parser.parse("1 twoseconds 1 threeseconds")) == 5
```

# Configuration file
At first glance, it may seem incomprehensible, like any other config without documentation. But for this, she
(ed. documentation) and created!

The `aiotense` config is not tied to a specific file type or file name, but we recommend sticking to the basic
standard - the name ".aiotense".

The aiotense config file parser supports just a few patterns, but you don't need more. let's consider
each of them.

=== "GetattributeParticleConverter"
    ```markdown
    Responsible for all expressions with type assignment (variable = value).
    Calls subconverters if subconverter for expression is not found -
    raises a ValueError.
    ```
=== "DigitValueConverter"
    ```markdown
    Responsible for all numerical values of objects (variable = 123).
    ```
=== "BooleanValueConverter"
    ```markdown
    Responsible for all boolean values of objects (variable = True|False|true|false).
    ```
=== "ListValueConverter"
    !!! danger
        Lists in `aiotense` are similar in pattern to python tuples. If you have 
        there is only one element of the list, then you must specify it with a comma, otherwise an error will occur.

    ```markdown
    Responsible for all list values of objects (variable = 1, 2, 3).

    It should be noted that only one list pattern is supported - separated by commas.
    the python-list pattern with square brackets is used to define headings,
    which break the configuration into logical groups.
    ```
=== "ExpressionValueConverter"
    !!! note
        All expressions are safe.
        For expressions in the parser, the "exp(do stuff here)" marker is used (exp. from expression - expression).

    ```markdown
    Responsible for all values of objects that contain the expression (variable = exp(6 * 6)).
    ```
    !!! info
        For convenience, the following constants have been added to the local values of expressions:

        - second: 1
        - minute: 60
        - hour: 60 * 60
        - day: 60 * 60 * 24
        - week: 60 * 60 * 24 * 7
        - year: 60 * 60 * 24 * 365

        Demo: "duration = exp(year * 10)" # Decade duration implementation!
        
        It is also worth noting the fact that even if you change the duration of any unit
        time from units.Unit, then these constants in expressions will still remain with the original value,
        because they are implemented by a dictionary and are not interconnected in any way.

**If** to delve into the process of lexing, then for each pattern, roughly speaking, there is a converter. These converters are divided
to main (AbstractParticleConverter) and subconverters (AbstractParticleValueConverter) these are all existing converters
at the moment, the ranks of which are likely to be replenished in the near future.

Each pattern (token/particle, I will use the "particle" - dot_tense.domain.HashableParticle) has its own
predicate (condition) that defines its own converter. In turn, each converter has its own
a predicate that determines its corresponding value.

The configuration parsing process itself is implemented using the "chain_of_responsibility" pattern, where each stage (step)
has its own task. In our case, 3 stages are implemented: LexingStep, AnalyzeStep, CompilingStep.

[See on github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/service_layer/dot_tense/step_chain.py#L133-L262)

!!! note
    Before we start parsing the configuration parsing steps, it is worth clarifying that parsing a configuration file (or
    its contents, no matter) goes from top to bottom in the line. Therefore, it is important to follow the order of the headings and
    settings, which we will talk about as soon as we consider the stages of parsing.

- At the first stage, LexingStep, strings are parsed into particles (tokens).
- In the second step, AnalyzeStep, the configuration is analyzed for possible errors.
- In the third step, CompilingStep, virtual units of time are added.

??? info "Open base configuration template"
    [See on github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/adapters/repository.py#L36-L115)
    ```json
    class TenseRepository(AbstractTenseRepository):
        # <inherited docstring from :class:`TenseRepository`> #
        _tense_config: dict[str, Any] = {
            "model.Tense": {
                "multiplier": 1,
                "virtual": [],
            },
            "units.Second": {
                "duration": 1,
                "aliases": [
                    "s",
                    "sec",
                    "secs",
                    "second",
                    "seconds",
                ],
            },
            "units.Minute": {
                "duration": 60,
                "aliases": [
                    "m",
                    "min",
                    "mins",
                    "minute",
                    "minutes",
                ],
            },
            "units.Hour": {
                "duration": 60 * 60,
                "aliases": [
                    "h",
                    "hour",
                    "hours",
                ],
            },
            "units.Day": {
                "duration": 60 * 60 * 24,
                "aliases": [
                    "d",
                    "day",
                    "days",
                ],
            },
            "units.Week": {
                "duration": 60 * 60 * 24 * 7,
                "aliases": [
                    "w",
                    "week",
                    "weeks",
                ],
            },
            "units.Year": {
                "duration": 60 * 60 * 24 * 365,
                "aliases": [
                    "y",
                    "year",
                    "years",
                ],
            },
        }
    ```

## Comments in configuration
At the moment, only one type of comments is supported - the pound "#".

## Configuration headers
`[model.Tense]`

!!! attention
    This header is mandatory in ANY case.

=== "multiplier"
    ```markdown
     - Type: `integer`
     - Description: This setting is in some parsers
     (such as DigitParser and its subclasses) by a time multiplier.
    ```

`[virtual]`

!!! note
    Unlike other units of time, you can use this heading an unlimited number of times.
    to create various custom units.

    ??? "Demonstration"
        ```asciidoc
        [model.Tense]
        
        [virtual]
        aliases = decade, decades
        duration = year * 10
        
        [virtual]
        aliases = century, centuries
        duration = year * 100
        
        [virtual]
        aliases = millennium,
        duration = year * 1000
        ```

=== "duration"
    ```markdown
     - Type: `integer`
     - Description: This setting is responsible for the duration
     certain unit of time.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case, a custom unit).
    ```

`[units.Second]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 1
     - Description: This setting is responsible for the duration of the second.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in template: `["s", "sec", "secs", "second", "seconds"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case - seconds).
    ```

`[units.Minute]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 60
     - Description: This setting is responsible for the duration of the minute.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in template: `["m", "min", "mins", "minute", "minutes"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case - minutes).
    ```

`[units.Hour]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 60 * 60
     - Description: This setting is responsible for the duration of the hour.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in template: `["h", "hour", "hours"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case - hours).
    ```

`[untits.Day]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 60 * 60 * 24
     - Description: This setting is responsible for the length of the day.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in template: `["d", "day", "days"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case, a day).
    ```

`[units.Week]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 60 * 60 * 24 * 7
     - Description: This setting is responsible for the length of the week.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in pattern: `["w", "week", "weeks"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case - weeks).
    ```

`[units.Year]`
=== "duration"
    ```markdown
     - Type: `integer`
     - Default: 60 * 60 * 24 * 365
     - Description: This setting is responsible for the length of the year.
    ```
=== "aliases"
    ```markdown
     - Type: `list[string]`
     - Default in template: `["y", "year", "years"]`
     - Description: This setting contains a list of all aliases
     a certain unit of time (in this case, years).
    ```

## Configuration - dealt with the theory, now to practice!
But before we get started, it's worth knowing how `from_tense_file` differs from `from_tense_file_source`.
It seems to be obvious from the name, but it seems not... Therefore, I will explain everything now!

`from_tense_file` opens the file at the given path, reads it, and returns a call to `from_tense_file_source` which
in turn, it parses specifically the string representation of the config.

!!! note
    If the configuration is loaded from a configuration file or its string representation,
    then it does not replace completely, but updates an already existing repository template using the dict.update() method.

I will use `from_tense_file_source` to emulate the config, but you get the point.
```py
import asyncio
from aiotense import TenseParser, from_tense_file_source, resolvers

config_emulation = """
[model.Tense]

[units.Second]
# duration = 60 # This field is optional, because the second default
# duration is 60 seconds, and, as mentioned earlier, the config that loads in this way are
# **not changed** to the new one, but **updated** with the new one using the dict.update() method.
aliases = s, sec, seconds # But old aliases won't be saved here.

[virtual]
aliases = millennium,
duration = exp(year * 1000)
"""

time_string = "1 millennium and 20 seconds..."
parser = TenseParser(
    TenseParser.DIGIT, 
    config=from_tense_file_source(config_emulation), 
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)) == 31536000020  # :D
```

In the course of writing the documentation, I noticed one interesting feature.
In fact, no one forbids importing `VCONVERTER_CONSTS` (constants for expressions in
configuration type **year * 10**) and add new values there!

```py
import asyncio
from aiotense import TenseParser, from_tense_file_source, resolvers
from aiotense.service_layer.dot_tense.converters import VCONVERTER_CONSTS

VCONVERTER_CONSTS.update({
    "decade": 60 * 60 * 24 * 365 * 10,
})

config_emulation = """
[model.Tense]

[virtual]
aliases = century, centuries
duration = exp(decade * 10)
"""

time_string = "1 century"
parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)).days == 36500
```

# Terms
!!! info "Primitive time string"
    === "Definition"
        ```markdown
        Strong precedence string `(number, time unit)`
        ```
    === "Examples"
        ```markdown
        1. 1day 2 minutes5 seconds
        ```

!!! info "Complex time string"
    === "Definition"
        ```markdown
        String with loose order `(word..*, number, word..*, time unit)`
        ```
    === "Examples"
        ```markdown
        1. Please convert 1 week and 2 days
        ```

!!! info "Alias"
    === "Definition"
        ```markdown
        Alias words for something
        (in the context of our project - aliases for units of time).
        ```
    === "Examples"
        ```markdown
        1. units.Second - ["s", "sec", "secs", "second", "seconds"]
        ```

!!! info "Resolver"
    === "Definition"
        ```markdown
        A function that adapts (prepares) a string for the parser.
        ```
