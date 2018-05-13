import json

from aiohttp.web_request import Request

from scrapper.src.server.model.video import Video


def to_json(*videos: Video) -> str:
    return json.dumps([i.__dict__ for i in videos])


async def read_request_content(request: Request, type=None) -> dict:
    body: [bytes] = await request.read()
    d = json.loads(body.decode())
    if type is not None:
        return type(d)
    else:
        return d
