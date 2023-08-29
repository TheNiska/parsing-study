from bs4 import BeautifulSoup
import requests

url = "https://aldaron.ru/song/the-pretty-reckless-house-on-a-hill"
html = requests.get(url=url).text

soup = BeautifulSoup(html, 'lxml')

# first element in html text
p_tag = soup.find('p')

# all tags -> list
p_tags = soup.find_all('p')

for paragraph in p_tags:
    # get only content without tags
    print(paragraph.text)
