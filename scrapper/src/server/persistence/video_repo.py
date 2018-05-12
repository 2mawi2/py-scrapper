from dataclasses import dataclass
from tinydb import TinyDB

from scrapper.src.server.common.static import video_table
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_serializer import serialize, deserialize


class NotFoundError(Exception):
    pass


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


