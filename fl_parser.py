import sys
from bs4 import BeautifulSoup
import requests
from utils.util import get_soup

CAT_CLASSES = ['text-5 mb-4 b-layout__txt_padbot_20', 'text-5 mb-4']
MAX_PAGE = 2


class Task:
    def __init__(self, name=None, link=None, url=None, id_=None, descr=None,
                 category=None, sub_category=None):
        self.name = name
        self.link = link
        self.url = url
        self.id_ = id_
        self.descr = descr
        self.category = category
        self.sub_category = sub_category

    def set_date(self, str_date):
        days, hours = str_date.split('|')
        day, month, year = map(int, days.split('.'))
        hour, minute = map(int, hours.split(':'))
        self.date = {'day': day, 'month': month, 'year': year,
                     'hour': hour, 'minute': minute}

    def __repr__(self):
        return f"Task ---------\n{self.name}\n{self.category}\n" \
               f"{self.sub_category}\n{self.id_}\n" \
               f"--------------"

    def __str__(self):
        return f"Name: {self.name}\nCategory: {self.category}\n" \
               f"Sub_category: {self.sub_category}\nLink: {self.link}\n" \
               f"Id: {self.id_}\nDate: {self.date}"


def get_tasks_info(url, tasks, page=None):
    soup = get_soup(url)
    item_class = "b-post__grid"
    works = soup.find_all('div', class_=item_class)
    for work in works:
        name = work.h2.a.text
        link = work.h2.a['href']
        id_ = link.split('/')[-2]
        task_url = "https://www.fl.ru" + link
        task = Task(name=name, link=link, url=task_url, id_=id_)
        tasks.append(task)

    if page is None:
        next_url = f"{url}page-2/"
        next_page = 2
    else:
        next_page = page + 1
        next_url = f"{url[:-2]}{next_page}/"

    if next_page > MAX_PAGE:
        return tasks
    get_tasks_info(next_url, tasks, page=next_page)


def main():
    url_1 = "https://www.fl.ru/projects/category/razrabotka-sajtov/"
    url_2 = "https://www.fl.ru/projects/category/programmirovanie/"
    tasks = []
    get_tasks_info(url_1, tasks)
    get_tasks_info(url_2, tasks)
    for task in tasks:
        soup = get_soup(task.url)
        main_id = "project_info_" + task.id_
        text_id = "projectp" + task.id_

        main_wrapper = soup.find('div', id=main_id)
        main = main_wrapper.find('div', class_="b-layout")
        descr = main.find('div', id=text_id).text.strip()
        task.descr = descr

        for cat_class in CAT_CLASSES:
            categories = main.find('div', cat_class)
            if categories:
                break

        if categories:
            categories = categories.text
            category, sub_category = categories.split(' / ')

            task.category = category
            task.sub_category = sub_category

        date_wrapper = main.find('div', class_="b-layout__txt b-layout__txt_padbot_30 mt-32")
        date = date_wrapper.find('div', class_="text-5").text.replace(' ', '')
        date = date.split('[')[0]
        task.set_date(date)

    counter = {}
    for task in tasks:
        if task.sub_category is not None:
            theme = f"{task.category} // {task.sub_category}"
            if theme not in counter:
                counter[theme] = 1
            else:
                counter[theme] += 1

    for task in tasks:
        print(str(task))
        print()


if __name__ == "__main__":
    main()
