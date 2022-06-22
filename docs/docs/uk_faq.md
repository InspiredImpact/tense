<img src="../tense-logo.jpg" align="left" width="200px"/>
Проект: aiotense
<br>
Ліцензія: Apache 2.0
<br>
Про проект: Інструмент для парсингу часу
<br>
Операційна система: Незалежний
<br>
Python: 3.9+
<br>
Typing: Typed
<br>
Тема: Утиліти
<br />
    <p align="center">
    <br />
    <a href="https://pypi.org/project/aiotense/">PyPi</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Сповістити про Баг</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Запропонувати Ідею</a>
    </p>

# Що являє собою aiotense?
`aiotense` - інструмент для парсингу часу. Чи потрібно Вам було конвертувати рядок
типу "1день1хвилина 20 секунд" в кількість секунд або об'єкт datetime.timedelta? Ні?
Тоді порадьте нас своїм друзям:) А якщо ви все ще тут – давайте продовжимо!

# Як спроектований aiotense?
`aiotense` спроектований так, щоб забезпечити максимальну **гнучкість**, **практичність** та **зручність** користувачеві.
Деяка логіка імпортується одразу, як клас або функція:

```py
from tense import TenseParser, from_tense_file, from_tense_file_source
```
А деякі частини імпортуються як модулі:

```py
from tense import units, model, unit_of_work, resolvers,

...
from tense.adapters import repository
```
Такий інтерфейс зроблено, щоб уникнути будь-яких циклічних імпортів і є основним стилем проекту.

# З чого почати?
Почнемо з основ, припустимо, у нас є рядок "1день1хвилина 20 секунд", як нам її перетворити на,
як раніше говорилося, у секунд або об'єкт datetime.timedelta?
- Давайте розглянемо!

```py
>> > import asyncio
>> > from tense import TenseParser

>> > time_string = "1день1хвилина 20 секунд"

>> > parser = TenseParser(TenseParser.DIGIT)
>> > asyncio.run(parser.parse(time_string))
0
```
Зачекайте, 0? І це все? - Ні. За замовчуванням підтримуються лише деякі аліаси англійської
мови, решту ви можете додати самі! Див. приклад нижче:

```py
>> > import asyncio
>> > from tense import TenseParser, units
>> > from tense.adapters import repository

>> > tenses = repository.TenseRepository()
>> > (
    ...    tenses.add_aliases_to(units.Day, ["день"])
    ....add_aliases_to(units.Minute, ["хвилина"])
    ....add_aliases_to(units.Second, ["секунд"])
    ... )

>> > time_string = "1день1хвилина 20 секунд"

>> > parser = TenseParser(TenseParser.DIGIT, config=tenses.config)
>> > asyncio.run(parser.parse(time_string))
86480
```
Ось інша справа!

# Як працює TenseParser?
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
[Див. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/factory.py#L33-L76)

Першим аргументом `TenseParser` приймає підклас від *aiotense.application.ports.parsers.AbstractParser*.
Спочатку вже є деякі готові реалізації, такі як **TenseParser.DIGIT** - aiotense.adapters.parsers.DigitParser
та **TIMEDELTA** - aiotense.adapters.parsers.TimedeltaParser.

!!! note
    Ви можете створювати і свої кастомні парсери, перш за все успадкувавши **aiotense.application.ports.parsers.AbstractParser**

У `TenseParser.__new__` відбувається невелика "обробка" значень, які надалі будуть передані
в ініціалізатори підкласів **...AbstractParser**, зрештою ми отримуємо готовий підклас **...AbstractParser**.

# Чому мій рядок не парситься?
Якщо ваш рядок є чимось подібним до "1 день + 2 хвилини і 5 секунд", то, швидше за все, у вас буде
конвертувати тільки останнє значення. Запитаєте, чому це так? - Справа в **резольвері** (time_resolver).
За замовчуванням стоїть резольвер, який відмінно справляється з примітивними рядками, цей же рядок є
комплексним (див. наприкінці FAQ Глосарій).

Крім "примітивного" резольвера, що стоїть за замовчуванням, так само є і "розумний".

!!! info
    aiotense.application.resolvers.smart_resolver() також не чутливий до регістру.

[Див. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/application/resolvers.py#L28-L63)

!!! note
     Так само як і з парсерами, ви можете створити свій кастомний резольвер, тільки не забувайте,
     що у резольвера є базова сигнатура (arg1: str, arg2: model.Tense).

```py
>>> import asyncio
>>> from tense import TenseParser, units, resolvers
>>> from tense.adapters import repository

>>> tenses = repository.TenseRepository()
>>> (
 ...    tenses.add_aliases_to(units.Day, ["день"])
 ...    .add_aliases_to(units.Minute, ["хвилини"])
...     .add_aliases_to(units.Second, ["секунд"])
... )

>>> time_string = "1 день + 2 хвилини и 5 секунд"

>>> parser = TenseParser(
...     TenseParser.DIGIT, 
...     config=tenses.config,
...     time_resolver=resolvers.smart_resolver,
... )
>>> asyncio.run(parser.parse(time_string))
86525
```
# А що за аргумент "converter" у TenseParser?
У класу AbstractParser є метод parse, який не можна перевизначити. У цьому методі
перед поверненням значення викликається реалізація абстрактного методу ._parse() з підкласів, значення
якого конвертується відповідно до зазначеного конвертера, якщо той не дорівнює None.

!!! note
    Ми намагаємося зробити `aiotense` якомога гнучкішим, тому практично кожен хук ви можете
    реалізувати по-своєму та передати у відповідне місце. Конвертер не є винятком, Ви
    можете створити свій кастомний, перш успадкувавши його від aiotense.application.ports.converters.AbstractConverter.
    Також варто врахувати той факт, що ...AbstractConverter є дженериком, який набуває типу значення,
    яке буде повернене в результаті конвертації (його ж і повертає в абстрактному методі .convert()).

# А що щодо delete/replace аліасів?
Атомарні операції в `aiotense` реалізовані патерном **UnitOfWork**, який, у свою чергу, взаємодіє з
репозиторієм аліасів.

!!! info "Давайте розглянемо докладніше"
    === "Видалення аліасів"
    ```py
    # <--- Синтаксичний цукор "with" дозволяє розбивати ділянки коду на логічні блоки ---> #
    from aiotense import unit_of_work, units
    
    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Конвертували тип одиниці часу в дорогу для конфігу
        assert "second" in uow.tenses.get_setting(second_str, "aliases")  # Аліас "second" за промовчанням в аліасах units.Second
    
        uow.delete_aliases(units.Second, ["second"])  # Видаляємо аліас у units.Second
    
        assert "second" not in uow.tenses.get_setting(second_str, "aliases")  # Аліас вилучений.
    ```
    === "Замена алиасов"
    ```py
    from aiotense import unit_of_work, units

    with unit_of_work.TenseUnitOfWork() as uow:
        second_str = uow.with_unit_resolve(units.Second)  # Конвертували тип одиниці часу в дорогу для конфігу
        assert "second" in uow.tenses.get_setting(second_str,
                                                  "aliases")  # Аліас "second" за промовчанням в аліасах units.Second
    
        uow.replace_aliases(units.Second, {"second": "секунда"})  # Замінюємо аліас "second" на "секунду"
        
        alias_state = uow.tenses.get_setting(second_str, "aliases")  # Отримуємо стан аліас після заміни
        assert "second" not in alias_state  #Аліас "second" вилучений
        assert "секунда" in alias_state  # Замість "second" з'явився новий аліас - "секунда"
    ```

    __Далі ми передаємо конфігурацію в TenseParser(config=uow.tenses.config)__

# Як додати одиниці часу?
Для кастомних одиниць часу в aiotense.domain.units виділено окремий клас - VirtualUnit. Він нічим не відрізняється
від ..Unit, але зручний для логічного поділу віртуальних одиниць від базових і, можливо, у найближчому майбутньому – новим
функціоналом.

```py
import asyncio
from tense import TenseParser, units
from tense.adapters import repository

tenses = repository.TenseRepository()
(
    tenses.add_virtual_unit(
        units.VirtualUnit(aliases=["двісекунди"], duration=2)
    )
        # або
        .add_virtual_unit_dict(  # TypedDict
        {"aliases": ["трисекунди"], "duration": 3}
    )
)

parser = TenseParser(TenseParser.DIGIT, config=tenses.config)
assert asyncio.run(parser.parse("1 двісекунди 1 трисекунди")) == 5
```

# Файл конфігурації
На перший погляд може здатися незрозумілим, як будь-який інший конфіг без документації. Але для цього вона
(ред. документація) й створена!

Конфіг `aiotense` не прив'язаний до конкретного типу файлів або їх назви, але ми рекомендуємо дотримуватись основного
стандарту – назви ".aiotense".

Парсер конфігфайлів aiotense підтримує буквально кілька патернів, але більше й не потрібно. Давайте розглянемо
кожен з них.

=== "GetattributeParticleConverter"
    ```markdown
    Відповідає всім висловлювання з привласненням типу (variable = value).
    Викликає сабконвертери, якщо сабконвертер для виразу не знайдено, то
    виникне помилка ValueError.
    ```
=== "DigitValueConverter"
    ```markdown
    Відповідає за числові значення об'єктів (variable = 123).
    ```
=== "BooleanValueConverter"
    ```markdown
    Відповідає всі булеві значення об'єктів (variable = True|False|true|false).
    ```
=== "ListValueConverter"
    !!! danger
        Списки в `aiotense` по патерну схожі з кортежами python. Якщо у вас
        всього один елемент списку, то ви повинні вказати його з комою, інакше виникне помилка.

    ```markdown
    Відповідає всі спискові значення об'єктів (variable = 1, 2, 3).
    
    Варто зазначити, що підтримується лише один патерн списку – через кому.
    Патерн python-list з квадратними дужками використовується для визначення заголовків,
    які розбивають конфігурацію на логічні групи.
    ```
=== "ExpressionValueConverter"
    !!! note:
        Усі висловлювання є безпечними.
        Для виразів у парсері використовується маркер “exp(do stuff here)” (exp. від expression – вираз).

    ```markdown
    Відповідає всім значення об'єктів, які містять вираз (variable = exp(6 * 6)).
    ```
    !!! info:
        Для зручності обчислення виразів були додані наступні локальні константи:

        - second: 1
        - minute: 60
        - hour: 60 * 60
        - day: 60 * 60 * 24
        - week: 60 * 60 * 24 * 7
        - year: 60 * 60 * 24 * 365

        Демонстрація: "duration = exp(year * 10)"  # Реалізація тривалості десятиліття!
        
        Також варто відзначити той факт, що якщо навіть ви зміните duration у будь-якої одиниці
        часу з units.Unit, то дані константи у виразах все одно залишаться з вихідним значенням,
        тому що реалізовані вони словником і не взаємопов'язані.

**Якщо** заглиблюватися в процес лексингу, то для кожного патерна, грубо кажучи, є конвертер. Ці ж конвертери діляться
на основні (AbstractParticleConverter) та сабконвертери (AbstractParticleValueConverter). Це всі присутні конвертери
на даний момент, ряди яких, швидше за все, будуть поповнені найближчим часом.

У кожного патерна (токена/партикла, далі використовуватиму "партикл" - dot_tense.domain.HashableParticle) є свій
предікейт (умова), який визначає власний конвертер. У свою чергу, у кожного конвертера є свій
предікейт, який визначає відповідне собі значення.

Сам процес парсингу конфігурації реалізований за допомогою патерну "chain_of_responsibility", де у кожного етапу (кроку)
є своє завдання. У нашому випадку реалізовано три етапи: LexingStep, AnalyzeStep, CompilingStep.

[Див. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/service_layer/dot_tense/step_chain.py#L133-L262)

!!! note
    Перш ніж ми почнемо аналіз етапів парсингу конфігурації, варто уточнити, що аналіз файлу конфігурації (або
    його вмісту, не має різниці) відбувається по рядку зверху вниз. Тому варто дотримуватися черговості заголовків і
    налаштувань, про які ми поговоримо як тільки розглянемо етапи парсингу.

- На першому етапі, LexingStep, відбувається розбір рядків на партикли (токени).
- На другому етапі, AnalyzeStep, конфігурація аналізується на можливі помилки.
- На третьому етапі CompilingStep додаються віртуальні одиниці часу.

??? info "Розгорнути базовий шаблон конфігурації"
    [Див. на github](https://github.com/Animatea/aiotense/blob/3d86a8bd95330bf19289c941d14edbe2d6c30e15/aiotense/adapters/repository.py#L36-L115)
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

## Коментарі в конфігурації
На даний момент підтримується лише один вид коментарів – "#".

## Заголовки у конфігурації
`[model.Tense]`

!!! attention
    Цей заголовок є обов'язковим у будь-якому випадку.

=== "multiplier"
    ```markdown
     - Тип: `integer`
     - Опис: Дане налаштування є в деяких парсерах
     (таких як DigitParser та його підкласи) множником часу.
    ```

`[virtual]`

!!! note
    На відміну від інших одиниць часу, цей заголовок ви можете використовувати необмежену кількість разів
    для створення різних кастомних юнітів.

    ??? "Демонстрація"
        ```asciidoc
        [model.Tense]
        
        [virtual]
        aliases = десятиліття, десятилітть
        duration = year * 10
        
        [virtual]
        aliases = вік, віків
        duration = year * 100
        
        [virtual]
        aliases = тисячоліття, тисячоліть
        duration = year * 1000
        ```

=== "duration"
    ```markdown
    - Тип: `integer`
    - Опис: Дане налаштування відповідає за тривалість
    певної одиниці часу.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку - кастомного юніту).
    ```

`[units.Second]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 1
     - Опис: Дане налаштування відповідає за тривалість секунди.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["s", "sec", "secs", "second", "seconds"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу у даному випадку - секунди).
    ```

`[units.Minute]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 60
     - Опис: Дане налаштування відповідає за тривалість хвилини.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["m", "min", "mins", "minute", "minutes"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку - хвилини).
    ```

`[units.Hour]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 60*60
     - Опис: Дане налаштування відповідає за тривалість години.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["h", "hour", "hours"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку - години).
    ```

`[untits.Day]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 60*60*24
     - Опис: Дане налаштування відповідає за тривалість дня.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["d", "day", "days"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку – дня).
    ```

`[units.Week]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 60*60*24*7
     - Опис: Ця установка відповідає за тривалість тижня.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["w", "week", "weeks"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку - тижня).
    ```

`[units.Year]`
=== "duration"
    ```markdown
     - Тип: `integer`
     - За замовчуванням: 60*60*24*365
     - Опис: Дане налаштування відповідає за тривалість року.
    ```
=== "aliases"
    ```markdown
     - Тип: `list[string]`
     - За замовчуванням у шаблоні: `["y", "year", "years"]`
     - Опис: Дане налаштування містить список всіх аліасів
     певної одиниці часу (у даному випадку - року).
    ```

## Конфігурація – з теорією розібралися, тепер до практики!
Але, перш ніж ми приступимо до практики, варто дізнатися, чим відрізняється `from_tense_file` від `from_tense_file_source`.
Начебто з назви очевидно, а ніби ні... Тому я все зараз поясню!

`from_tense_file` відкриває файл за вказаним шляхом, читає його та повертає виклик `from_tense_file_source`, який
своєю чергою, парсить саме строкове уявлення конфіга.

!!! note
    Якщо виконується завантаження конфігурації з конфігураційного файлу або його строкового уявлення,
    він не замінюється повністю, а оновлює вже існуючий шаблон репозиторію за допомогою методу dict.update().

Я використовуватиму `from_tense_file_source` для емуляції конфіга, але суть Ви зрозуміли.

```py
import asyncio
from tense import TenseParser, from_tense_file_source, resolvers

config_emulation = """
[model.Tense]

[units.Second]
# duration = 60 # Це поле не обов'язкове, адже у секунди за замовчуванням
# тривалість дорівнює 60 секунд, а, як говорилося раніше, конфіг при такому способі
# завантаження **не змінюється** на новий, а **оновлюється** новим за допомогою методу dict.update().
aliases = с, сек, секунда, секунд, секунди  # Але тут уже старі аліаси не збережуться.

[virtual]
aliases = тисячоліття, тисячоліть
duration = exp(year * 1000)
"""

time_string = "1 тисячоліття та 20 секунд..."
parser = TenseParser(
    TenseParser.DIGIT, 
    config=from_tense_file_source(config_emulation), 
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)) == 31536000020  # :D
```

І тут Остапа понесло... Під час написання документації я помітив одну цікаву фішку.
По суті ніхто не забороняє імпортувати `VCONVERTER_CONSTS` (константи для виразів у
конфігурації типу **year * 10**) та додати туди нові значення!

```py
import asyncio
from tense import TenseParser, from_tense_file_source, resolvers
from tense.service_layer.dot_tense.converters import VCONVERTER_CONSTS

VCONVERTER_CONSTS.update({
    "десятиліття": 60 * 60 * 24 * 365 * 10,
})

config_emulation = """
[model.Tense]

[virtual]
aliases = вік, віків
duration = exp(десятиліття * 10)
"""

time_string = "1 вік"
parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
    time_resolver=resolvers.smart_resolver,
)
assert asyncio.run(parser.parse(time_string)).days == 36500
```

# Глосарій
!!! info "Примітивний рядок часу"
    === "Визначення"
        ```markdown
        Рядок із суворою черговістю `(число, одиниця часу)`
        ```
    === "Приклади"
        ```markdown
        1. 1день 2 хвилини5секунд
        ```

!!! info "Комплексний рядок часу"
    === "Визначення"
        ```markdown
        Рядок з нестрогою черговістю `(слово..*, число, слово..*, одиниця часу)`
        ```
    === "Приклади"
        ```markdown
        1. Сконвертуй, будь ласка, 1 вчорашній день
        ```

!!! info "Аліас(и)"
    === "Визначення"
        ```markdown
        Слова-псевдоніми для чогось
        (У контексті нашого проекту - псевдоніми для одиниць часу).
        ```
    === "Приклади"
        ```markdown
        1. units.Second - ["s", "sec", "secs", "second", "seconds"]
        ```

!!! info "Резольвер"
    === "Визначення"
        ```markdown 
        Функція, яка адаптує (підготовляє) рядок для парсера.
        ```
