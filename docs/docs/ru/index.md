<img src="../doc_assets/tense-logo.jpg" align="left" width="200px"/>
Проект: aiotense
<br>
Лицензия: Apache 2.0
<br>
О проекте: Инструмент для парсинга времени
<br>
Операционная система: Независимый
<br>
Python: 3.10+
<br>
Typing: Typed
<br>
Тема: Утилиты
<br />
    <p align="center">
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">PyPi</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Сообщить о Баге</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Предложить Идею</a>
    </p>

# Что из себя представляет aiotense?
`aiotense` - инструмент для парсинга времени. Нужно ли Вам было конвертировать строку 
типа "1день1минута 20 секунд" в кол-во секунд или объект datetime.timedelta? Нет? 
Тогда посоветуйте нас своим друзьям :) А если вы всё ещё здесь - давайте продолжим!

# Как спроектирован aiotense?
`aiotense` спроектирован так, чтоб обеспечить максимальную **гибкость**, **практичность** и **удобство** пользователю.
Некоторая логика импортируется сразу, как класс или функция:
```py
from aiotense import TenseParser, from_tense_file, from_tense_file_source
```
А некоторые части импортируются как модули:
```py
from aiotense import units, model, unit_of_work, resolvers, ...
from aiotense.adapters import repository
```
Такой интерфейс сделан во избежание каких-либо циклических импортов и является основным стилем проекта.

# С чего начать?
Начнём с основ, доспустим, у нас есть строка "1день1минута 20 секунд", как нам её преобразовать в, 
как ранее говорилось, кол-во секунд или объект datetime.timedelta?
- Давайте рассмотрим!
```py
>>> import asyncio
>>> from aiotense import TenseParser

>>> time_string = "1день1минута 20 секунд"

>>> parser = TenseParser(TenseParser.DIGIT)
>>> asyncio.run(parser.parse(time_string))
0
```
Подождите-ка, 0? И это всё? - Нет. По умолчанию поддерживаются только некоторые алиасы английского 
языка, все остальные вы можете добавить сами! См. пример ниже:
```py
>>> import asyncio
>>> from aiotense import TenseParser, units
>>> from aiotense.adapters import repository

>>> tenses = repository.TenseRepository()
>>> (
...    tenses.add_aliases_to(units.Day, ["день"])
...    .add_aliases_to(units.Minute, ["минута"])
...    .add_aliases_to(units.Second, ["секунд"])
... )

>>> time_string = "1день1минута 20 секунд"

>>> parser = TenseParser(TenseParser.DIGIT, config=tenses.config)
>>> asyncio.run(parser.parse(time_string))
86480
```
Вот, другое дело!

# Как работает TenseParser?
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
[См. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/factory.py#L33-L76)

Первым аргументом `TenseParser` принимает подкласс от *aiotense.application.ports.parsers.AbstractParser*. 
Изначально есть уже некоторые готовые реализации, такие как **TenseParser.DIGIT** - aiotense.adapters.parsers.DigitParser 
и **TIMEDELTA** - aiotense.adapters.parsers.TimedeltaParser.

!!! note
    Вы можете создавать и свои кастомные парсеры, прежде унаследовав **aiotense.application.ports.parsers.AbstractParser**

В `TenseParser.__new__` происходит небольшая "обработка" значений, которые в дальнейшем будут переданы 
в инициализаторы подклассов **...AbstractParser**, в конечном итоге мы получаем готовый подкласс **...AbstractParser**.

# Почему моя строка не парсится?
Если ваша строка является чем-то на подобии "1 день + 2 минуты и 5 секунд", то, скорее всего, у вас будет 
конвертироваться только последнее значение. Спросите, почему так? - Дело в **резольвере** (time_resolver). 
По умолчанию стоит резольвер, который отлично справляется с примитивными строками, данная же строка является 
комплексной (см. в конце FAQ термины).

Помимо "примитивного" резольвера, который стоит по умолчанию, так же есть и "умный".

!!! info
    aiotense.application.resolvers.smart_resolver() так же не чувствителен к регистру.

[См. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/resolvers.py#L28-L63)

!!! note
    Так же как и с парсерами, вы можете создать **свой** кастомный резольвер, только не забывайте, 
    что у резольвера есть базовая сигнатура (arg1: str, arg2: model.Tense).

```py
>>> import asyncio
>>> from aiotense import TenseParser, units, resolvers
>>> from aiotense.adapters import repository

>>> tenses = repository.TenseRepository()
>>> (
 ...    tenses.add_aliases_to(units.Day, ["день"])
 ...    .add_aliases_to(units.Minute, ["минуты"])
...     .add_aliases_to(units.Second, ["секунд"])
... )

>>> time_string = "1 день + 2 минуты и 5 секунд"

>>> parser = TenseParser(
...     TenseParser.DIGIT, 
...     config=tenses.config,
...     time_resolver=resolvers.smart_resolver,
... )
>>> asyncio.run(parser.parse(time_string))
86525
```
# А что за аргумент "converter" у TenseParser?
У класса ...AbstractParser есть метод parse, который нельзя переопределить. В данном методе 
перед возвратом значения вызывается реализация абстрактного метода ._parse() из подклассов, значение 
которого конвертируется в соответствии с указанными конвертером, если тот не равен None.

!!! note
    Мы стараемся сделать `aiotense` как можно более гибким, поэтому практически каждый хук вы можете 
    реализовать по-своему и передать в соответствующее место. Конвертер не является исключением, Вы
    можете создать свой, кастомный, прежде унаследовав его от aiotense.application.ports.converters.AbstractConverter.
    Так же стоит учесть тот факт, что ...AbstractConverter является дженериком, который принимает тип значения,
    которое будет возвращено в результате конвертации (его же и возвращает в абстрактном методе .convert()).

# А что насчёт delete/replace алиасов?
Атомарные операции в `aiotense` реализованы паттерном **UnitOfWork**, который, в свою очередь, взаимодействует с 
репозиторием алиасов.

!!! info "Давайте рассмотрим детальнее"
    === "Удаление алиасов"
    ```py
    # <--- Синтаксический сахар "with" позволяет разбивать участки кода на логические блоки ---> #
    from aiotense import unit_of_work, units
    
    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Конвертировали тип единицы времени в путь для конфига
        assert "second" in uow.tenses.get_setting(second_str, "aliases")  # Алиас "second" по умолчанию в алиасах units.Second
    
        uow.delete_aliases(units.Second, ["second"])  # Удаляем алиас у units.Second
    
        assert "second" not in uow.tenses.get_setting(second_str, "aliases")  # Алиас удалён.
    ```
    === "Замена алиасов"
    ```py
    from aiotense import unit_of_work, units

    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Конвертировали тип единицы времени в путь для конфига
        assert "second" in uow.tenses.get_setting(second_str,
                                                  "aliases")  # Алиас "second" по умолчанию в алиасах units.Second
    
        uow.replace_aliases(units.Second, {"second": "секунда"})  # Заменяем алиас "second" на "секунда"
        
        alias_state = uow.tenses.get_setting(second_str, "aliases")  # Получаем состояние алиас после замены
        assert "second" not in alias_state  # Алиас "second" удалён
        assert "секунда" in alias_state  # Вместо "second" появился новый алиас - "секунда"
    ```

    __Далее мы передаём исходники репозитория в TenseParser(config=uow.tenses.config)__

# Как добавить свои единицы времени?
Для кастомных единиц времени в aiotense.domain.units выделен отдельный класс - VirtualUnit. Он ничем не отличается 
от ..Unit, но удобен для логического разделения виртуальных единиц от базовых и, возможно, в ближайшем будущем - новым 
функционалом.

```py
import asyncio
from aiotense import TenseParser, units
from aiotense.adapters import repository

tenses = repository.TenseRepository()
(
    tenses.add_virtual_unit(
        units.VirtualUnit(aliases=["двесекунды"], duration=2)
    )
    # или
    .add_virtual_unit_dict(  # TypedDict
        {"aliases": ["трисекунды"], "duration": 3}
    )
)

parser = TenseParser(TenseParser.DIGIT, config=tenses.config)
assert asyncio.run(parser.parse("1 двесекунды 1 трисекунды")) == 5
```

# Файл конфигурации
На первый взгляд может показаться непонятным, как и любой другой конфиг без документации. Но для этого ж она 
(ред. документация) и создана!

Конфиг `aiotense` не привязан к конкретному типу файлов или их названию, но мы рекомендуем придерживаться основного 
стандарта - названия ".aiotense".

Парсер конфигфайлов aiotense поддерживает буквально несколько паттернов, но больше и не нужно. Давайте рассмотрим 
каждый из них.
=== "GetattributeParticleConverter"
    ```markdown
    Отвечает за все выражения с присваиванием типа (variable = value).
    Вызывает сабконвертеры, если сабконвертер для выражения не найден - 
    возбудит ошибку ValueError.
    ```
=== "DigitValueConverter"
    ```markdown
    Отвечает за все числовые значения объектов (variable = 123).
    ```
=== "BooleanValueConverter"
    ```markdown
    Отвечает за все булевые значения объектов (variable = True|False|true|false).
    ```
=== "ListValueConverter"
    !!! danger
        Списки в `aiotense` по паттерну схожи с кортежами python. Если у вас 
        всего один элемент списка, то вы должны указать его с запятой, иначе возникнет ошибка.

    ```markdown
    Отвечает за все списковые значения объектов (variable = 1, 2, 3).

    Стоит отметить, что поддерживается только один паттерн списка - через запятую. 
    паттерн python-list с квадратными скобками используется для определения заголовков,
    которые разбивают конфигурацию на логические группы.
    ```
=== "ExpressionValueConverter"
    !!! note:
        Все выражения являются безопасными.
        Для выражений в парсере используется маркер "exp(do stuff here)" (exp. от expression - выражение).

    ```markdown
    Отвечает за все значения объектов, которые содержат выражение (variable = exp(6 * 6)).
    ```
    !!! info:
        Для удобства в локальные значения выражений были добавлены следующие константы:

        - second: 1
        - minute: 60
        - hour: 60 * 60
        - day: 60 * 60 * 24
        - week: 60 * 60 * 24 * 7
        - year: 60 * 60 * 24 * 365

        Демонстрация: "duration = exp(year * 10)"  # Реализация продолжительности десятилетия!
        
        Так же стоит отметить тот факт, что если даже вы измените duration у какой-либо единицы 
        времени из units.Unit, то данные константы в выражениях всё равно останутся с исходным значением, 
        потому что реализованы они словарём и никак не взаимосвязаны.

**Если** углубляться в процесс лексинга, то для каждого паттерна, грубо говоря, есть свой конвертер. Эти же конвертеры делятся 
на основные (AbstractParticleConverter) и сабконвертеры (AbstractParticleValueConverter) это все существующие конвертеры 
на данный момент, ряды которых, скорее всего, будут пополнены в ближайшем будущем.

У каждого паттерна (токена/партикла, дальше буду использовать "партикл" - dot_tense.domain.HashableParticle) есть свой 
предикейт (условие), который определяет собственный конвертер. В свою же очередь, у каждого конвертера есть свой 
предикейт, который определяет соответствующее себе значения.

Сам процесс парсинга конфигурации реализован с помощью паттерна "chain_of_responsibility", где у каждого этапа (шага) 
есть своя задача. В нашем случае реализовано 3 этапа: LexingStep, AnalyzeStep, CompilingStep.

[См. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/service_layer/dot_tense/step_chain.py#L133-L262)

!!! note
    Прежде чем мы начнём разбор этапов парсинга конфигурации, стоит уточнить, что анализ файла конфигурации (или 
    его содержимого, без разницы) происходит по строке сверху вниз. Поэтому стоит соблюдать очередность заголовков и 
    настроек, про которые мы поговорим как только-вот рассмотрим этапы парсинга.

- На первом этапе, LexingStep, происходит разбор строк на партиклы (токены).
- На втором этапе, AnalyzeStep, конфигурация анализируется на возможные ошибки.
- На третьем этапе, CompilingStep, добавляются виртуальные единицы времени. 

??? info "Развернуть базовый шаблон конфигурации"
    [См. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/adapters/repository.py#L36-L115)
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

## Комментарии в конфигурации
На данный момент поддерживается только один вид комментариев - решётка "#".

## Заголовки в конфигурации
`[model.Tense]`

!!! attention
    Данный заголовок является обязательным в ЛЮБОМ случае.

=== "multiplier"
    ```markdown
    - Тип: `integer`
    - Описание: Данная настройка является в некоторых парсерах 
    (таких как DigitParser и его подклассы) множителем времени.
    ```

`[virtual]`

!!! note
    В отличие от других единиц времени, данный заголовок вы можете использовать неограниченное количество раз 
    для создания различных кастомных юнитов.
    
    ??? "Демонстрация"
        ```asciidoc
        [model.Tense]
        
        [virtual]
        aliases = десятилетие, десятилетий
        duration = year * 10
        
        [virtual]
        aliases = век, веков
        duration = year * 100
        
        [virtual]
        aliases = тысячелетие, тысячелетия
        duration = year * 1000
        ```

=== "duration"
    ```markdown
    - Тип: `integer`
    - Описание: Данная настройка отвечает за длительность 
    определённой единицы времени.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - кастомного юнита).
    ```

`[units.Second]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 1
    - Описание: Данная настройка отвечает за длительность секунды.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["s", "sec", "secs", "second", "seconds"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - секунды).
    ```

`[units.Minute]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 60
    - Описание: Данная настройка отвечает за длительность минуты.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["m", "min", "mins", "minute", "minutes"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - минуты).
    ```

`[units.Hour]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 60 * 60
    - Описание: Данная настройка отвечает за длительность часа.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["h", "hour", "hours"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - часа).
    ```

`[untits.Day]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 60 * 60 * 24
    - Описание: Данная настройка отвечает за длительность дня.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["d", "day", "days"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - дня).
    ```

`[units.Week]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 60 * 60 * 24 * 7
    - Описание: Данная настройка отвечает за длительность недели.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["w", "week", "weeks"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - недели).
    ```

`[units.Year]`
=== "duration"
    ```markdown
    - Тип: `integer`
    - По умолчанию: 60 * 60 * 24 * 365
    - Описание: Данная настройка отвечает за длительность года.
    ```
=== "aliases"
    ```markdown
    - Тип: `list[string]`
    - По умолчанию в шаблоне: `["y", "year", "years"]`
    - Описание: Данная настройка содержит в себе список всех алиасов 
    определённой единицы времени (в данном сучае - года).
    ```

## Конфигурация - с теорией разобрались, теперь к практике!
Но, прежде чем мы приступим к практике, стоит узнать чем отличается `from_tense_file` от `from_tense_file_source`.
Вроде бы с названия очевидно, а вроде и нет... Поэтому я всё сейчас объясню!

`from_tense_file` открывает файл по указанному пути, читает его и возвращает вызов `from_tense_file_source`, который 
в свою очередь, парсит конкретно строковое представление конфига.

!!! note
    Если выполняется загрузка конфигурации с конфигурационного файла или его строкового представления, 
    то он не заменяется полностью, а обновляет уже существующий шаблон репозитория с помощью метода dict.update().

Я буду использовать `from_tense_file_source` для эмуляции конфига, но суть Вы поняли.
```py
import asyncio
from aiotense import TenseParser, from_tense_file_source, resolvers

config_emulation = """
[model.Tense]

[units.Second]
# duration = 60 # Данное поле не обязательно, ведь у секунды по умолчанию
# длительность равна 60 секундам, а, как говорилось ранее, конфиг при таком виде 
# загрузки **не меняется** на новый, а **обновляется** новым с помощью метода dict.update(). 
aliases = с, сек, секунда, секунд, секунды  # Но тут уже старые алиасы не сохранятся.

[virtual]
aliases = тысячелетие, тысячелетия
duration = exp(year * 1000)
"""

time_string = "1 тысячелетие и 20 секунд..."
parser = TenseParser(
    TenseParser.DIGIT, 
    config=from_tense_file_source(config_emulation), 
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)) == 31536000020  # :D
```

И тут Остапа понесло... По ходу написания документации я заметил одну интересную фишку.
По сути-то никто не запрещает импортировать `VCONVERTER_CONSTS` (константы для выражений в 
конфигурации типа **year * 10**) и добавить туда новые значения!

```py
import asyncio
from aiotense import TenseParser, from_tense_file_source, resolvers
from aiotense.service_layer.dot_tense.converters import VCONVERTER_CONSTS

VCONVERTER_CONSTS.update({
    "десятилетие": 60 * 60 * 24 * 365 * 10,
})

config_emulation = """
[model.Tense]

[virtual]
aliases = век, веков
duration = exp(десятилетие * 10)
"""

time_string = "1 век"
parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)).days == 36500
```

# Термины
!!! info "Примитивная строка времени"
    === "Определение"
        ```markdown
        Строка со строгой очередностью `(число, единица времени)`
        ```
    === "Примеры"
        ```markdown
        1. 1день 2 минуты5секунд
        ```

!!! info "Комплексная строка времени"
    === "Определение"
        ```markdown
        Строка с нестрогой очередностью `(слово..*, число, слово..*, единица времени)`
        ```
    === "Примеры"
        ```markdown
        1. Сконвертируй, пожалуйста, 1 вчерашний день
        ```

!!! info "Алиас(ы)"
    === "Определение"
        ```markdown
        Слова-псевдонимы для чего-либо 
        (в контексте нашего проекта - псевдонимы для едениц времени).
        ```
    === "Примеры"
        ```markdown
        1. units.Second - ["s", "sec", "secs", "second", "seconds"]
        ```

!!! info "Резольвер"
    === "Определение"
        ```markdown
        Функция, которая адаптирует (подготавливает) строку для парсера. 
        ```
