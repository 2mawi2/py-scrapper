from scrapper.src.server.model.video import Video


def deserialize(videos: [dict]) -> [Video]:
    return [Video(video_id=v.doc_id,
                  url=v["url"],
                  preview=v["preview"],
                  title=v["title"],
                  actor=v["actor"],
                  date=v["date"],
                  isFavourite=v["isFavourite"],
                  description=v["description"],
                  keywords=v["keywords"]) for v in videos]


def serialize(videos: [Video]) -> [dict]:
    dicts: [dict] = [v.__dict__ for v in videos]
    [d.pop("video_id", None) for d in dicts]
    return dicts
