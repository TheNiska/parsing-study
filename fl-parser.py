from bs4 import BeautifulSoup
import requests


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
        print(self.date)

    def __repr__(self):
        return f"Task -------\n{self.name}\n{self.url}\n"


def get_soup(url):
    with open('headers.txt', 'r', encoding='utf-8') as file:
        user_agent = file.readline()[:-1]
    headers = {'User-Agent': user_agent}

    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_tasks_info(soup):
    item_class = "b-post__grid"
    works = soup.find_all('div', class_=item_class)
    tasks_list = []
    for work in works:
        name = work.h2.a.text
        link = work.h2.a['href']
        id_ = link.split('/')[-2]
        url = "https://www.fl.ru" + link
        task = Task(name=name, link=link, url=url, id_=id_)
        tasks_list.append(task)
    return tasks_list


def main():
    url_1 = "https://www.fl.ru/projects/category/razrabotka-sajtov/"
    url_2 = "https://www.fl.ru/projects/category/programmirovanie/"
    soup = get_soup(url_1)
    tasks = get_tasks_info(soup)
    for task in tasks:
        soup = get_soup(task.url)
        main_id = "project_info_" + task.id_
        text_id = "projectp" + task.id_

        main_wrapper = soup.find('div', id=main_id)
        main = main_wrapper.find('div', class_="b-layout")
        descr = main.find('div', id=text_id).text.strip()
        task.descr = descr
        categories = main.find('div', class_="text-5 mb-4 b-layout__txt_padbot_20")
        if categories:
            categories = categories.text
            category, sub_category = categories.split(' / ')

            task.category = category
            task.sub_category = sub_category

        date_wrapper = main.find('div', class_="b-layout__txt b-layout__txt_padbot_30 mt-32")
        date = date_wrapper.find('div', class_="text-5").text.replace(' ', '')
        date = date.split('[')[0]
        task.set_date(date)


if __name__ == "__main__":
    main()
