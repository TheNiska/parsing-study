from pydantic.dataclasses import dataclass
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
        self.title = self.title.strip()
        self.link = self.link.strip()
        self.descr = self.descr.strip()
        self.category = self.category.strip()
        self.sub_category = self.sub_category.strip()
