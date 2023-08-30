from bs4 import BeautifulSoup
import requests


def get_soup(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def print_eng_lyrics():
    url = "https://aldaron.ru/song/the-pretty-reckless-house-on-a-hill"
    soup = get_soup(url)

    # getting only p tags with 'eng_lyrics' class
    p_eng_lyrics = soup.find_all('p', class_="eng_lyrics")
    for p in p_eng_lyrics:
        print(p.text)


def print_products(soup, i):
    products = soup.find_all('div', class_="product-wrap")
    for product in products:
        i += 1
        name_wrap = product.find('div', class_="product-wrap__name")
        name = name_wrap.find('h3').text

        sku_wrap = product.find('div', class_="quant-sku")
        sku = sku_wrap.find('div', class_="product-sku").text[12:]

        price_wrap = product.find('div', class_="product-wrap__price")
        price = price_wrap.find('li', class_="product-wrap__price-new").text

        product_info = f"{i}) {name} | {sku} | {price}"
        print(product_info)

    return i


def ovk_term_products():
    i = 0
    last_page = '55'
    url = "https://ovk-term.ru/sanfayans/smesiteli/"
    soup = get_soup(url)

    i = print_products(soup, i)

    pagination = soup.find('ul', class_="pagination")
    link_li = pagination.find_all('li')[-2]
    link = link_li.find('a', href=True)
    new_url = link['href']
    current_page = new_url[-2:]

    while True:
        soup = get_soup(new_url)
        i = print_products(soup, i)

        if current_page == last_page:
            break

        pagination = soup.find('ul', class_="pagination")
        link_li = pagination.find_all('li')[-2]
        link = link_li.find('a', href=True)
        new_url = link['href']
        current_page = new_url[-2:]


def main():
    ovk_term_products()


if __name__ == "__main__":
    main()
