from dataclasses import dataclass


@dataclass
class Video:
    video_id: int = None
    url: str = ""
    preview: str = ""
    title: str = ""
    actor: str = ""
    date: str = ""
    isFavourite: bool = False
    description: str = ""
    keywords: str = ""
