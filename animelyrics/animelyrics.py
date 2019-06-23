# coding: utf-8
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import googlesearch

__BASE_URL__ = "www.animelyrics.com"


class InvalidLanguage(Exception):
    """Exception class to handle invalid language selection"""

    pass


def search_lyrics(query, lang="jp", show_title=False):
    """
    Search the given query string inside AnimeLyrics.

    :param str query: Query string. 
    :param str lang: Language to search in (jp, en)
    :param bool show_title: Show title at the top of the string

    :rtype: str
    :return: String of lyrics in given language
    """
    if lang != "en" and lang != "jp":
        raise InvalidLanguage("Unsupported language type")

    if lang == "jp":
        class_name = "romaji"
        song_idx = 0
    elif lang == "en":
        class_name = "translation"
        song_idx = 1

    url = get_lyrics_url(query)

    if url is None:
        return "No results found"

    soup = get_lyrics_soup(url)

    center_box = soup.find("div", {"class": "centerbox"})
    lyrics_table = center_box.find("table")
    lyrics = ""

    if lyrics_table is None:
        if lang == "en":
            return "No english translation for lyrics found"

        lyrics = center_box.find("span", {"class": "lyrics"}).get_text()
    else:
        lyrics_divs = lyrics_table.find_all("td", {"class": class_name})
        for div in lyrics_divs:
            print(div)

    if show_title:
        song_name, anime_name = get_song_info(soup)
        return "{} - {}\n{}".format(song_name[song_idx], anime_name, lyrics)
    else:
        return lyrics


def get_song_info(soup):
    """
    Retrieve the song name (english / japanese) and anime name

    :param BeautifulSoup soup: BeautifulSoup4 object of lyrics url

    :rtype [str, str]
    :return Tuple of song and anime name
    """
    crumbs = soup.find("ul", {"id": "crumbs"})
    crumbs_list = crumbs.find_all("li")
    song_name = [name.strip() for name in crumbs_list[-1].get_text().split("-")]
    anime_name = crumbs_list[-2].get_text()

    return (song_name, anime_name)


def get_lyrics_soup(url):
    """
    Get a BeautifulSoup4 representation of a url

    :param str url: URL to read

    :rtype: BeautifulSoup
    :return: BeautifulSoup4 object of the loaded url
    """
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")

    # convert all br into newlines
    for line_break in soup.find_all("br"):
        line_break.replace_with("\n")

    # remove all dt (term) tags in the page
    for term in soup.find_all("dt"):
        term.decompose()

    return soup


def get_lyrics_url(query):
    """
    Finds a url in AnimeLyrics website for a lyric

    :param str query: Query string.

    :rtype: str
    :return: String of the url page for the given query
    """
    for url in googlesearch.search("site:{} {}".format(__BASE_URL__, query), stop=10):
        # return the first page with .htm in the url as it contains lyrics
        if str(url).endswith(".htm"):
            return url

    # return none if query cannot find any pages
    return None
