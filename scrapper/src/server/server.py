import json
import sys
from dataclasses import dataclass

import routes as routes
from aiohttp import web
from aiohttp.web_request import Request

from scrapper.src.server.common import utils
from scrapper.src.server.common.static import DB_PRODUCTION, DB_DEVELOPMENT
from scrapper.src.server.persistence.video_repo import VideoRepo


@dataclass
class VideoCtrl:
    video_Repo: VideoRepo

    async def get_by_id(self, request: Request):
        video_id: int = int(request.match_info["video_id"])
        videos = self.video_Repo.get_by_id(video_id)
        payload = utils.to_json(videos)
        return web.Response(status=200, body=payload)

    async def videos(self, request: Request):
        videos = self.video_Repo.all()
        payload = utils.to_json(*videos)
        return web.Response(status=200, body=payload)

    async def favourite(self, request: Request):
        video_id: int = int(request.match_info["video_id"])
        self.video_Repo.favourite(video_id)
        return web.Response(status=202)

    async def unfavourite(self, request: Request):
        video_id: int = int(request.match_info["video_id"])
        self.video_Repo.unfavourite(video_id)
        return web.Response(status=202)



def server(is_development: bool):
    video_ctrl = new_video_ctrl(is_development)
    app = web.Application()
    app.add_routes([
        web.get('/videos', video_ctrl.videos),
        web.get('/videos/{video_id}', video_ctrl.get_by_id),
        web.get('/videos/favourite/{video_id}', video_ctrl.favourite),
        web.get('/videos/unfavourite/{video_id}', video_ctrl.unfavourite)
    ])
    web.run_app(app, host="localhost", port=5000)


def new_video_ctrl(is_development):
    if is_development:
        connection_str = DB_DEVELOPMENT
        print("Running in Development")
    else:
        connection_str = DB_PRODUCTION
        print("Running in Production")
    video_repo = VideoRepo(connection_str)
    video_ctrl = VideoCtrl(video_repo)
    return video_ctrl


if __name__ == '__main__':
    DEVELOPMENT = False
    server(is_development=False)
