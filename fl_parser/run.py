from util import get_html
import xml.etree.ElementTree as ET
from datetime import datetime
from models import TaskItem
from pydantic import ValidationError


def parse_items(html: str) -> list[TaskItem]:
    root = ET.fromstring(html).find('channel')
    all_items = root.findall('item')
    task_items = []

    for i, item in enumerate(all_items):
        title = item.find('title').text
        link = item.find('link').text
        descr = item.find('description').text

        id_ = int(link.split('/')[-2])

        cat_str = item.find('category').text
        category, sub_category = cat_str.split(' / ')

        date_str = item.find('pubDate').text
        date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')

        try:
            task_item = TaskItem(fl_id=id_, title=title, link=link,
                                 descr=descr, category=category,
                                 sub_category=sub_category,
                                 date=date)
        except ValidationError as err:
            for error in err.errors():
                print(error)
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
        # doing something

    print(len(task_items))


if __name__ == "__main__":
    main()
