from pydantic.dataclasses import dataclass
from typing import Iterable
from datetime import datetime


@dataclass(kw_only=True)
class TaskItem:
    fl_id: int
    title: str
    link: str
    descr: str
    category: str
    sub_category: str
    date: datetime

    def __post_init__(self):
        self.title = self.title.strip().lower()
        self.link = self.link.strip()
        self.descr = self.descr.strip().lower()
        self.category = self.category.strip()
        self.sub_category = self.sub_category.strip()

    def to_tuple(self, category_id: int) -> tuple:
        return (
            self.fl_id, self.title, self.link, self.descr,
            self.date.strftime('%Y-%m-%d %H:%M:%S'), category_id
        )
