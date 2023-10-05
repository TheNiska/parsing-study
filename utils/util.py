from bs4 import BeautifulSoup
from requests import get


def get_soup(url):
    with open('utils/headers.txt', 'r', encoding='utf-8') as file:
        user_agent = file.readline()[:-1]
    headers = {'User-Agent': user_agent}

    html = get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup
