# coding: utf-8
from bs4 import BeautifulSoup
import requests
import googlesearch
from urllib.parse import urlparse

BASE_URL = 'www.animelyrics.com'

def search(query, lang="jp"):
    """
    Search the given query string inside AnimeLyrics.

    :param str query: Query string. 
    :param str lang: Language to search 
        jp = Japanese text (romanji)
        en = English translation of lyrics

    :rtype: str
    :return: String of lyrics in given language
    """
    for url in googlesearch.search('site:{} {}'.format(BASE_URL, query), stop=10):
        print(url)