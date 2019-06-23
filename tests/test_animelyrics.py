import pytest
import requests
from bs4 import BeautifulSoup

import animelyrics
from animelyrics import InvalidLanguage, MissingTranslatedLyrics, NoLyricsFound

__RENAI_CIRCULATION_URL__ = (
    "https://www.animelyrics.com/anime/bakemonogatari/renaicirculation.htm"
)
__CHOBITS_URL___ = "https://www.animelyrics.com/anime/chobits/letmebewithyou.htm"
__FAIRY_TAIL_URL___ = "https://www.animelyrics.com/anime/fairytail/kokoronokagi.htm"


def test_get_lyrics_url():
    # empty string check
    no_url = animelyrics.get_lyrics_url("")
    assert no_url is None

    # invalid search string check
    garbage_url = animelyrics.get_lyrics_url("omgwtfbbq")
    assert garbage_url is None

    # proper search string check
    renai_circulation_url = animelyrics.get_lyrics_url("renai circulation")
    assert renai_circulation_url == __RENAI_CIRCULATION_URL__


def test_get_lyrics_soup():
    soup = animelyrics.get_lyrics_soup(__RENAI_CIRCULATION_URL__)
    assert type(soup) is BeautifulSoup

    empty_url_soup = animelyrics.get_lyrics_soup("")
    assert type(empty_url_soup) is BeautifulSoup


def test_get_song_info():
    soup = animelyrics.get_lyrics_soup(__RENAI_CIRCULATION_URL__)
    song_info = animelyrics.get_song_info(soup)

    assert song_info == (["Ren'ai Circulation", "Love Circulation"], "Bakemonogatari")

    # test songs with no english translation
    soup = animelyrics.get_lyrics_soup(__FAIRY_TAIL_URL___)
    song_info = animelyrics.get_song_info(soup)

    assert song_info == (["Kokoro no Kagi"], "FAIRY TAIL")

    # test songs with english name
    soup = animelyrics.get_lyrics_soup(__CHOBITS_URL___)
    song_info = animelyrics.get_song_info(soup)

    assert song_info == (["Let Me Be With You"], "Chobits")


def test_search_lyrics():
    with pytest.raises(NoLyricsFound):
        animelyrics.search_lyrics("")

    with pytest.raises(NoLyricsFound):
        animelyrics.search_lyrics("omgwtfbbq")

    with pytest.raises(InvalidLanguage):
        animelyrics.search_lyrics("renai circulation", lang="fr")

    # check song that does not have english translation
    with pytest.raises(MissingTranslatedLyrics):
        lyrics = animelyrics.search_lyrics("kokoro no kagi", lang="en")

    # check whether renai circulation lyrics is correct
    lyrics = animelyrics.search_lyrics("renai circulation")
    assert lyrics.splitlines()[0] == "(se~ no!)"
    assert lyrics.splitlines()[-1] == "zutto zutto"

    # check whether lyrics still showing correct if language is explicitly stated
    lyrics = animelyrics.search_lyrics("renai circulation", lang="jp")
    assert lyrics.splitlines()[0] == "(se~ no!)"
    assert lyrics.splitlines()[-1] == "zutto zutto"

    # check whether lyrics still showing correct if all parameters are stated
    lyrics = animelyrics.search_lyrics("renai circulation", lang="jp", show_title=False)
    assert lyrics.splitlines()[0] == "(se~ no!)"
    assert lyrics.splitlines()[-1] == "zutto zutto"

    # test songs with english translation
    lyrics = animelyrics.search_lyrics("god knows", lang="en")
    assert lyrics.splitlines()[6] == "I face your back and leave without turning back. "
    assert (
        lyrics.splitlines()[-16]
        == "Become strong and you might even be able to change fate, you know."
    )

    # check whether title is shown correctly
    lyrics = animelyrics.search_lyrics("renai circulation", show_title=True)
    assert lyrics.splitlines()[0] == "Ren'ai Circulation - Bakemonogatari"
    assert lyrics.splitlines()[2] == "(se~ no!)"

    # check whether title is shown correctly if language is explicitly stated
    lyrics = animelyrics.search_lyrics("renai circulation", lang="jp", show_title=True)
    assert lyrics.splitlines()[0] == "Ren'ai Circulation - Bakemonogatari"
    assert lyrics.splitlines()[2] == "(se~ no!)"

    # check whether english song names title display correct
    lyrics = animelyrics.search_lyrics("renai circulation", lang="en", show_title=True)
    assert lyrics.splitlines()[0] == "Love Circulation - Bakemonogatari"
    assert lyrics.splitlines()[2] == "(One~ two!)"

    # check whether songs with only english names show up correctly
    lyrics = animelyrics.search_lyrics("let me be with you", lang="en", show_title=True)
    assert lyrics.splitlines()[0] == "Let Me Be With You - Chobits"
    assert lyrics.splitlines()[10] == "I want to hold you tight"
