from dataclasses import dataclass
from enum import Enum


class SearchType(Enum):
    Id = 1
    SearchType = 2
    Title = 3
    Actor = 4
    Date = 5
    IsFavourite = 6
    Keywords = 7
    Description = 8
    All = 9


@dataclass
class SearchRequest:
    SearchType: SearchType
    SearchField: str


@dataclass
class PagedRequest:
    PageSize: int
    Skip: int

    def __init__(self, iterable=(), **kwargs) -> None:
        self.__dict__.update(iterable, **kwargs)
