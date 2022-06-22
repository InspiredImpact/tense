<div id="top"></div>
<img src="../assets/tense-logo.jpg" align="left" width="200px"/>
Проект: tense
<br>
Лицензия: Apache 2.0
<br>
Описание: Инструмент для парсинга времени
<br>
OS: Независимый
<br>
Python: 3.9+
<br>
Typing: Аннотирован
<br>
Тема: Утилиты
<br />
    <p align="center">
    <br />
    <a href="https://animatea.github.io/tense/">Документация</a>
    ·
    <a href="https://github.com/Animatea/tense/issues">Сообщить о баге</a>
    ·
    <a href="https://github.com/Animatea/tense/issues">Предложить идею</a>
    </p>
<div id="top"></div>
<p align="center">
   <a href="ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>
   <a href="../README.md"><img height="20" src="https://img.shields.io/badge/language-en-green?style=social&logo=googletranslate"></a>
</p>

<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#о-проекте">О проекте</a>
      <ul>
        <li><a href="#добро-пожаловать">Добро пожаловать</a></li>
      </ul>
    </li>
    <li>
      <a href="#приступить-к-использованию">Приступить к использованию</a>
      <ul>
        <li><a href="#pypi">PyPi</a></li>
        <li><a href="#poetry">Poetry</a></li>
      </ul>
    </li>
    <li>
      <a href="#использование">Использование</a>
      <ul>
        <li><a href="#основные-возможности">Основные возможности</a></li>
        <li><a href="#изменение-существующих-параметров">Изменение существующих параметров</a></li>
        <li><a href="#добавление-новых-настроек">Добавление новых настроек</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </li>
    <li><a href="#примеры">Примеры</a></li>
    <li><a href="#вклад-в-проект">Вклад в проект</a></li>
    <li><a href="#лицензия">Лицензия</a></li>
    <li><a href="#контакт">Контакт</a></li>
    <li><a href="#благодарности">Благодарности</a></li>
    <li><a href="#история">История проекта</a></li>
  </ol>
</details>

## О проекте
<a href="https://circleci.com/gh/Animatea/tense/tree/main"><img height="20" src="https://dl.circleci.com/status-badge/img/gh/Animatea/tense/tree/main.svg?style=svg"></a>
<a href="https://pypi.org/project/tense/"><img height="20" alt="PyPi" src="https://img.shields.io/pypi/v/tense"></a>
<a href="https://pypi.org/project/mypy/"><img height="20" alt="Mypy badge" src="http://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://github.com/psf/black"><img height="20" alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pycqa.github.io/isort/"><img height="20" alt="Supported python versions" src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336"></a>

### Добро пожаловать
> Нужно ли Вам было конвертировать, например, строку "1д1минута 2 сек" 
в кол-во секунд или обьект datetime.timedelta?

Нет? Тогда посоветуйте наш проект своим друзьям :) Если вы всё ещё здесь - давайте двигаться дальше!

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

## Приступить к использованию
### PyPi
```bash
$ pip3 install tense
```

### Poetry
```bash
$ poetry add tense
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

## Использование
### Основные возможности

```py
import datetime
from tense import TenseParser

time_string = "1d2minutes 5 sec"

# <-- Digit parser -->
digit_parser = TenseParser(TenseParser.DIGIT)
assert digit_parser.parse(time_string) == 86525

# <-- Timedelta parser -->
delta_parser = TenseParser(TenseParser.TIMEDELTA)
delta_value = delta_parser.parse(time_string)
# <-- Assertions -->
assert isinstance(delta_value, datetime.timedelta)
assert str(delta_value) == "1 day, 0:02:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

### Изменение существующих параметров

```py
from tense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]
multiplier = 2  # секундное значение каждой единицы времени будет умножено на 2
# !!! Уточнение: Если multiplier <= 0, тогда парсеры могут работать некорректно 
# В данном случае будет выслано предупреждение в консоль.

[units.Minute]
duration = 120  # Почему бы и нет?...
aliases = моя_минута, моя_мин, моих_мин, минут
"""
parser = TenseParser(
    TenseParser.TIMEDELTA,
    tenses=from_tense_file_source(config_emulation),
)
delta_value = parser.parse("1 моя_мин 10моих_мин 9  минут")
assert str(delta_value) == "1:20:00"  # (каждая 120 * 2)
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

### Добавление новых настроек

```py
from tense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]  # Этот заголовок обязателен.

[units.Year]
duration = exp(year)
aliases = год, лет

[units.Second]
duration = exp(second)
aliases = с, сек, секунд

[virtual]
duration = exp(year * 10)
aliases = десятилетие, десятилетий
"""

parser = TenseParser(
    TenseParser.TIMEDELTA,
    tenses=from_tense_file_source(config_emulation),
)
delta_value = parser.parse("1год 10 десятилетий5   секунд")
assert str(delta_value) == "36865 days, 0:00:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

### FAQ
Но что если нам нужно парсить строку типа: "1day and 10 minutes + 5 seconds"?
Давайте посмотрим:

```py
>> > from tense import TenseParser

>> > complex_string = "1day and 10 minutes + 5 seconds"

>> > parser = TenseParser(TenseParser.TIMEDELTA)
>> > parser.parse(complex_string)
'0:00:05'
```
Подождите... Что? 5 секунд? Но там же дни и минуты...
- Всё окей, вы же используете гибкий tense! Проблему решить можно двумя способами:
  1) Вы пишете свой time_resolver
  2) Вы выбираете из уже существующих tense.resolvers

Давайте продемонстрирую!
Я буду использовать второй вариант, так как существующие резольверы мне подходят.

```py
>> > from tense import TenseParser, resolvers

>> > complex_string = "1day and 10 minutes + 5 seconds"

>> > parser = TenseParser(TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver)
>> > parser.parse(complex_string)
'1 day, 0:10:05'
```
Ну, так-то лучше!

**tense.application.resolvers.smart_resolver()** так же является не чувствительным к регистру!

```py
>> > from tense import TenseParser, resolvers

>> > complex_string = "1DAY and 10 MINUTES + 5 SECONDS"

>> > parser = TenseParser(TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver)
>> > parser.parse(complex_string)
'1 day, 0:10:05'
```

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

## Примеры
Если Вы думаете, что на этом возможности tense заканчиваются, то вы ошибаетесь!
Возможностей tense слишком много для README, поэтому я предлагаю Вам продолжить просмотр 
примеров использования тут:
<p align="center">
<br />
<a href="https://github.com/Animatea/tense/tree/main/examples">Tense Примеры</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

## Вклад в проект

Вклады — это то, что делает сообщество с открытым исходным кодом таким замечательным местом для обучения, вдохновения и творчества. Любой ваш вклад **очень ценится**.

Если у вас есть предложение, которое могло бы улучшить это, разветвите репозиторий и создайте запрос на включение. Вы также можете просто открыть вопрос с тегом «enhancement».
Не забудьте поставить звезду проекту! Спасибо ещё раз!

1. Создайте форк проекта
2. Создайте вашу ветку с нововведением (`git checkout -b feature/AmazingFeature`)
3. Подтвердите изменения (`git commit -m 'Add some AmazingFeature'`)
4. Внесите изменения на ветку (`git push origin feature/AmazingFeature`)
5. Создайте пулл реквест
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

<!-- LICENSE -->
## Лицензия

Распространяется под лицензией Apache 2.0. См. детальнее [`LICENSE`](https://github.com/Animatea/tense/blob/main/LICENSE).

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>


<!-- CONTACT -->
## Контакт
<div align="left">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner4" alt="" /></a>
</div>

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>


## Благодарности
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Python](https://www.python.org)
* [Python Community](https://www.python.org/community/)
* [MkDocs](https://www.mkdocs.org)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>

## История
Изначально проект был сделан асинхронным, что существенно замедляло процесс парсинга, ведь tense является CPU-bound модулем.

Отрефакторив проект, мы получили `~x22.31` ускорение в обработке сложных строк (с помощью `smart_resolver`).
> Было: `~0.00095030...`μs | Стало: `~0.00004260...`μs

И `~x38.28` ускорение в обработке простых строк, соответственно (с помощью `basic_resolver`).
> Было: `~0.00062400...`μs | Стало: `~0.00001630...`μs

Предыдущая (асинхронная) версия по-прежнему доступна в ветках репозитория - https://github.com/Animatea/tense/tree/async-final, 
но сайт с документацией будет изменён.

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/вернуться в-начало-green?style=social&logo=github"></a></p>
