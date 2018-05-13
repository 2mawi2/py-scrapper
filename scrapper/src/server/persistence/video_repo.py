from collections import defaultdict
from dataclasses import dataclass
from tinydb import TinyDB, Query
from scrapper.src.server.common.errors import NotFoundError, BadRequestError
from scrapper.src.server.common.static import video_table
from scrapper.src.server.model.search_request import SearchRequest, SearchType
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_serializer import serialize, deserialize
from pyxtension.streams import stream


@dataclass
class VideoRepo:
    connection_str: str

    def open(self) -> TinyDB:
        return TinyDB(self.connection_str)

    def insert(self, videos: [Video]) -> [int]:
        serialized = serialize(videos)
        with self.open() as db:
            return db.table(video_table).insert_multiple(serialized)

    def all(self) -> [Video]:
        with self.open() as db:
            videos = db.table(video_table)

            if videos is None:
                raise NotFoundError()

            return deserialize(videos)

    def delete_all(self):
        with self.open() as db:
            db.purge_table(video_table)

    def get_by_id(self, video_id) -> Video:
        with self.open() as db:
            result = db.table(video_table).get(doc_id=video_id)

            if result is None:
                raise NotFoundError(video_id)

            return deserialize([result])[0]

    def favourite(self, video_id: int):
        self._change_favourite(video_id, True)

    def unfavourite(self, video_id):
        self._change_favourite(video_id, False)

    def _change_favourite(self, video_id: int, value: bool):
        with self.open() as db:
            db.table(video_table).update({"isFavourite": value}, doc_ids=[video_id])

    def search(self, search_rq: SearchRequest) -> [Video]:
        validate_request(search_rq)

        st = search_rq.SearchType
        sf = search_rq.SearchField

        if st is SearchType.isFavourite:
            return self.search_favourite()

        search_words = [word.strip(" ").lower() for word in sf.split(" ") if word.strip(" ") != ""]
        videos = stream([self.search_by_word(st, word) for word in search_words]).flatMap()

        return self.rank_distinct(videos)

    def rank_distinct(self, videos: [Video]):
        groups = defaultdict(list)

        for video in videos:
            groups[video.url].append(video)

        new_list = sorted(groups.values(), key=len, reverse=True)
        return [i[0] for i in new_list]

    def search_favourite(self):
        return [v for v in self.all() if v.isFavourite is True]

    def search_by_attribute(self, sf: str, attribute: str):
        return [v for v in self.all() if sf in getattr(v, attribute).lower()]

    def search_by_word(self, st, sf):
        if st is SearchType.description:
            return self.search_by_attribute(sf, "description")
        if st is SearchType.actor:
            return self.search_by_attribute(sf, "actor")
        if st is SearchType.date:
            return self.search_by_attribute(sf, "date")
        if st is SearchType.keywords:
            return self.search_by_attribute(sf, "keywords")
        if st is SearchType.title:
            return self.search_by_attribute(sf, "title")
        if st is SearchType.all:
            return self.search_by_attribute(sf, "description") \
                   + self.search_by_attribute(sf, "keywords") \
                   + self.search_by_attribute(sf, "actor") \
                   + self.search_by_attribute(sf, "date") \
                   + self.search_by_attribute(sf, "title")
        else:
            raise BadRequestError("Invalid SearchType")


def validate_request(search_rq: SearchRequest):
    st: SearchType = search_rq.SearchType
    sf: str = search_rq.SearchField

    if st in [SearchType.keywords, SearchType.all, SearchType.description,
              SearchType.title, SearchType.date, SearchType.actor]:
        if sf == "":
            raise BadRequestError("SearchField must be set")

    if st is SearchType.id:
        try:
            int(sf)
        except ValueError:
            raise BadRequestError("SearchField must contain a valid int id")
