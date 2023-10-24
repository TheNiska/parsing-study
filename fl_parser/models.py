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
               f"Id: {self.id_}\nDate: {self.date}\nDescr: {self.descr}"