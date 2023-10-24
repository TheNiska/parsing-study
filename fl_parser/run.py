from util import get_html
import xml.etree.ElementTree as ET


def main():
    CATEGORIES = {'programming': 5}

    htmls = []
    for key in CATEGORIES:
        link = f"https://www.fl.ru/rss/all.xml?category={CATEGORIES[key]}"
        html = get_html(link)
        htmls.append(html)

    root = ET.fromstring(htmls[0]).find('channel')
    all_items = root.findall('item')

    for i, item in enumerate(all_items):
        title = item.find('title').text
        link = item.find('link').text
        descr = item.find('description').text
        category = item.find('category').text
        date = item.find('pubDate').text

        res = f"{i}\n{title}\n{link}\n{descr}\n{category}\n{date}\n\n"
        print(res)


if __name__ == "__main__":
    main()
