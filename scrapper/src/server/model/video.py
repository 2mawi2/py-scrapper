from dataclasses import dataclass


@dataclass
class Video:
    Url: str = ""
    Preview: str = ""
    Title: str = ""
    Actor: str = ""
    Date: str = ""
    IsFavourite: bool = False
    Description: str = ""
    Keywords: str = ""


