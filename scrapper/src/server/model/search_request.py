from dataclasses import dataclass
from enum import Enum


class SearchType(Enum):
    id = 1
    searchType = 2
    title = 3
    actor = 4
    date = 5
    isFavourite = 6
    keywords = 7
    description = 8
    all = 9


@dataclass
class SearchRequest:
    SearchType: SearchType
    SearchField: str

    def __init__(self, iterable=(), **kwargs) -> None:
        self.__dict__.update(iterable, **kwargs)


@dataclass
class PagedRequest:
    PageSize: int
    Skip: int

    def __init__(self, iterable=(), **kwargs) -> None:
        self.__dict__.update(iterable, **kwargs)
