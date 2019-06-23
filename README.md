# animelyrics

[![Build Status](https://travis-ci.com/colorfusion/animelyrics.svg?branch=master)](https://travis-ci.com/colorfusion/animelyrics) [![Coverage Status](https://coveralls.io/repos/github/colorfusion/animelyrics/badge.svg?branch=master)](https://coveralls.io/github/colorfusion/animelyrics?branch=master) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

>Python API to retrieve song lyrics from [animelyrics](https://www.animelyrics.com).

## Features
- Search for lyrics from [animelyrics](https://www.animelyrics.com) website
- Japanese (romaji) and english translated text support
- Show title on top of lyrics

## Prerequisties
- Python >=3.0.0

## Install
```sh
pip install animelyrics
```

Simple! 🎉

## Usage
```python
import animelyrics

print(animelyrics.search_lyrics("renai circulation"))
```

### Multi-language search
The language of the lyrics can be specified using the `lang` argument during the function call:
```python
import animelyrics

print(animelyrics.search_lyrics("god knows", lang="en"))
```

Currently the API only supports the following inputs
- `jp` - romaji text
- `en` - translated english text

### Song Titles
To add the song title and the anime where it came from to the lyrics, use the `show_title` argument
```python
import animelyrics

print(animelyrics.search_lyrics("snow halation", show_title=True))
```

### Exceptions
The API contains the following exception that will be raised in different scenarios
- `InvalidLanguage`
- `MissingTranslatedLyrics`
- `NoLyricsFound`

The following example shows how to cover all exceptions while searching for lyrics:
```python
import animelyrics

try:
    lyrics = animelyrics.search_lyrics("song lyrics")
except animelyrics.MissingTranslatedLyrics:
    # case when english language is used but no translation is found
except animelyrics.NoLyricsFound:
    # case when no lyrics are found
```

## Test
```sh
python setup.py test
```

## Author
### 🕺 Melvin Yeo
- GitHub: [@colorfusion](https://github.com/colorfusion)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!"<br>
Check out the [issues page](https://github.com/colorfusion/animelyrics/issues)

## Support

Please ⭐ this repository if it is helpful to you!

## License

Copyright © 2019 Melvin Yeo.<br>
This project is [MIT](https://github.com/colorfusion/animelyrics/blob/master/LICENSE) licensed.
