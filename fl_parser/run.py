import xml.etree.ElementTree as ET
import logging as lg
from util import get_html
from datetime import datetime
from models import TaskItem
from pydantic import ValidationError
from database import add_sub_categories


def parse_items(html: str) -> list[TaskItem]:
    '''Parsint data from html-string to list of object of the class
    TaskItem'''

    root = ET.fromstring(html).find('channel')
    all_items = root.findall('item')
    task_items = []

    for item in all_items:
        title = item.find('title').text
        link = item.find('link').text
        descr = item.find('description').text

        id_ = int(link.split('/')[-2])

        cat_str = item.find('category').text
        category, sub_category = cat_str.split(' / ')

        date_str = item.find('pubDate').text
        date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')

        try:
            task_item = TaskItem(
                fl_id=id_, title=title, link=link, descr=descr,
                category=category, sub_category=sub_category, date=date
            )
        except ValidationError as error:
            errors_list = [
                f"Input must be {err['type']} in {err['loc']}, "
                f"but {err['input']} is given. {err['msg']}."
                for err in error.errors()
            ]

            lg.error('\n'.join(errors_list))
            continue

        task_items.append(task_item)

    return task_items


def main():
    CATEGORIES = {'programming': 5, 'webdev': 2}

    htmls = []
    for key in CATEGORIES:
        link = f"https://www.fl.ru/rss/all.xml?category={CATEGORIES[key]}"
        html = get_html(link)
        htmls.append(html)

    task_items = []
    for html in htmls:
        task_items.extend(parse_items(html))

    cat_set = {(el.category, el.sub_category) for el in task_items}
    add_sub_categories(cat_set)


if __name__ == "__main__":
    lg.basicConfig(
        level=lg.INFO, filename='logs', filemode='a', encoding='utf-8',
        format="%(asctime)s - %(levelname)s\n%(message)s\n",
        datefmt="%d-%m-%Y %H:%M:%S"
    )

    main()
