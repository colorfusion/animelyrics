import pytest
import animelyrics

def test_get_lyrics_url():
    # empty string check
    no_url = animelyrics.get_lyrics_url("")
    assert no_url is None

    # invalid search string check
    garbage_url = animelyrics.get_lyrics_url("omgwtfbbq")
    assert garbage_url is None

    # proper search string check
    lyrics_url = "https://www.animelyrics.com/anime/bakemonogatari/renaicirculation.htm"
    renai_circulation_url = animelyrics.get_lyrics_url("renai circulation")
    assert renai_circulation_url == lyrics_url

