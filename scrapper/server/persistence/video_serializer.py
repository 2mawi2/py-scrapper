from scrapper.server.model.Video import Video


def deserialize(videos: [dict]) -> [Video]:
    return [Video(Url=v["Url"],
                  Preview=v["Preview"],
                  Title=v["Title"],
                  Actor=v["Actor"],
                  Date=v["Date"],
                  IsFavourite=v["IsFavourite"],
                  Description=v["Description"],
                  Keywords=v["Keywords"]) for v in videos]


def serialize(videos: [Video]) -> [dict]:
    return [v.__dict__ for v in videos]
