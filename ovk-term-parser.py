from bs4 import BeautifulSoup
import requests


def get_soup(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, 'lxml')
    return soup


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


def main():
    k = 0
    for i in range(1, 56):
        url = f"https://ovk-term.ru/sanfayans/smesiteli/?page={i}"
        soup = get_soup(url)
        k = print_products(soup, k)


if __name__ == "__main__":
    main()
