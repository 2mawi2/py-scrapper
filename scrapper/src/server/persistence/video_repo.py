from dataclasses import dataclass
import tinydb

from scrapper.src.server.common.static import video_table
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_serializer import serialize, deserialize


@dataclass
class VideoRepo:
    db: tinydb.TinyDB

    def insert(self, videos: [Video]) -> [int]:
        serialized = serialize(videos)
        return self.db.table(video_table).insert_multiple(serialized)

    def all(self) -> [Video]:
        videos = self.db.table(video_table)
        return deserialize(videos)

    def delete_all(self):
        self.db.purge_table(video_table)

    def get_by_id(self, video_id) -> Video:
        result = self.db.table(video_table).get(doc_id=video_id)
        return deserialize([result])[0]

    def favourite(self, video_id: int):
        self.db.table(video_table).update({"IsFavourite": True}, doc_ids=[video_id])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.db:
            self.db.close()
