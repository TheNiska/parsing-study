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


class Query:
    QUERIES = {'SELECT', 'INSERT'}

    def __init__(
            self,
            query_type: str,
            tbl_name: str,
            fields: tuple[str] = None,
            values: Iterable = None,
            where: str = None
            ):

        if not isinstance(query_type, str):
            raise ValueError('Query must be a string')

        self.query_type = query_type.upper()

        if self.query_type not in self.QUERIES:
            raise ValueError('Unsupported query type')

        if not (isinstance(fields, tuple) and isinstance(fields[0], str)):
            raise ValueError('Fields must be tuple of strings')

        if not isinstance(values, Iterable) and self.query_type != 'SELECT':
            raise ValueError('Values must be an iterable')

        self.tbl_name = tbl_name
        self.fields = fields
        self.values = values
        self.where = where

        if self.query_type == 'SELECT':
            self._query = self._get_select_query()

    def __str__(self):
        return self._query

    def _get_select_query(self):
        query = (
            f"{self.query_type} {', '.join(self.fields)} "
            f"FROM {self.tbl_name}"
        )
        if self.where:
            query += self.where
        return query


if __name__ == '__main__':
    q = Query('select', 'my_table', fields=('name', 'id'))
    print(str(q))
