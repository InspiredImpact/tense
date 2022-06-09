<div id="top"></div>
<img src="assets/tense-logo.jpg" align="left" width="200px"/>
Project: aiotense
<br>
License: Apache 2.0
<br>
About: Time Processing Tool
<br>
OS: Independent
<br>
Python: 3.10+
<br>
Typing: Typed
<br>
Topic: Utilities
<br />
    <p align="center">
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">Documentation</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Report Bug</a>
    ·
    <a href="https://github.com/Animatea/aiotense/issues">Request Feature</a>
    </p>
<div id="top"></div>
<p align="center">
   <a href="i18n/ua_README.md"><img height="20" src="https://img.shields.io/badge/language-ua-green?style=social&logo=googletranslate"></a>
   <a href="i18n/ru_README.md"><img height="20" src="https://img.shields.io/badge/language-ru-green?style=social&logo=googletranslate"></a>
</p>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#abstract">Abstract</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#with-pypi">With PyPi</a></li>
        <li><a href="#with-poetry">With Poetry</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#built-in-basic">Built-in basics</a></li>
        <li><a href="#reconfiguring-existing-settings">Reconfiguring existing settings</a></li>
        <li><a href="#adding-new-settings">Adding new settings</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
    </li>
    <li><a href="#examples">Examples</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project
<h5 align="center">Diagram with the main logic of the project</h5>
<img src="assets/tense-uml.jpg" align="left"/>


### Abstract
> Have you ever needed to convert, for example, the string "1d1minute 2 sec" 
to the number of seconds or a datetime.timedelta object?

No? Then advise us to your friends :) And if you really need our tool - let's move on!
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Getting started
### With PyPi
```bash
$ pip3 install aiotense
```

### With Poetry
```bash
install with poetry
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Usage
### Built-in basic
```py
import asyncio
import datetime
from aiotense import TenseParser

time_string = "1d2minutes 5 sec"

# <-- Digit parser -->
digit_parser = TenseParser(TenseParser.DIGIT)
digit_value = asyncio.run(digit_parser.parse(time_string))
# <-- Assertions -->
assert digit_value == 86525

# <-- Timedelta parser -->
delta_parser = TenseParser(TenseParser.TIMEDELTA)
delta_value = asyncio.run(delta_parser.parse(time_string))
# <-- Assertions -->
assert isinstance(delta_value, datetime.timedelta)
assert str(delta_value) == "1 day, 0:02:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### Reconfiguring existing settings
```py
import asyncio
from aiotense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]
multiplier = 2  # each unit of time will be multiplied by 2
# !!! Note: If the multiplier is <= 0, then the parsers will 
# not work correctly. In this case, a warning will be sent to the console.

[units.Minute]
duration = 120  # Why not?...
aliases = my_minute, my_minutes, my_min, my_mins
"""
parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
)
delta_value = asyncio.run(parser.parse("1 my_min 10my_mins 9  my_minutes"))
# <-- Assertions -->
assert str(delta_value) ==  "1:20:00" # (each 120 * 2)
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### Adding new settings
```py
import asyncio
from aiotense import TenseParser, from_tense_file_source

config_emulation = """
[model.Tense]  # This header is required.

[virtual]
duration = exp(year * 10)
aliases = decade, dec, decs, decades
"""

parser = TenseParser(
    TenseParser.TIMEDELTA,
    config=from_tense_file_source(config_emulation),
)
delta_value = asyncio.run(parser.parse("1year 10 decades5   seconds"))
# <-- Assertions -->
assert str(delta_value) == "36865 days, 0:00:05"
```
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

### FAQ
But what if you need to parse a string like: "1year and 10 decades + 5 seconds"?
Let's see:
```py
>>> import asyncio
>>> from aiotense import TenseParser

>>> complex_string = "1day and 10 minutes + 5 seconds"

>>> parser = TenseParser(TenseParser.TIMEDELTA)
>>> asyncio.run(parser.parse(complex_string))
'0:00:05'
```
Wait... What? 5 second? But there are days and minutes...
- It's okay, you're using flexible aiotense! This problem is solved in two ways:
  1) You write your own time_resolver and pass it
  2) Choose an existing one from aiotense.resolvers

Let's demonstrate!
I will use the second option, since the built-in time resolvers in aiotense are suitable for me.
```py
>>> import asyncio
>>> from aiotense import TenseParser, resolvers

>>> complex_string = "1day and 10 minutes + 5 seconds"

>>> parser = TenseParser(TenseParser.TIMEDELTA, time_resolver=resolvers.smart_resolver)
>>> asyncio.run(parser.parse(complex_string)) 
'1 day, 0:10:05'
```
Well, that's better!
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Examples.
If you think that this is where the possibilities of aiotense ends, then you are wrong! 
The possibilities of aiotense are too many for a README, so I suggest you move on to viewing 
the usage examples:
<p align="center">
<br />
<a href="https://github.com/Animatea/aiotense/tree/main/examples">Aiotense Examples</a>
</p>
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>

<!-- LICENSE -->
## License

Distributed under the Apache 2.0 License. See [`LICENSE`](https://github.com/Animatea/aiotense/blob/main/LICENSE) for more information.

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>


<!-- CONTACT -->
## Contact
<div align="left">
    <a href="https://discord.com/invite/KKUFRZCt4f"><img src="https://discordapp.com/api/guilds/744099317836677161/widget.png?style=banner4" alt="" /></a>
</div>

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>


## Acknowledgments
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right"><a href="#top"><img height="20" src="https://img.shields.io/badge/back_to-top-green?style=social&logo=github"></a></p>
