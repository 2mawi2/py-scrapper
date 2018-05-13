from dataclasses import dataclass

from aiohttp import web
from aiohttp.web_request import Request

from scrapper.src.server.common import utils
from scrapper.src.server.common.static import DB_PRODUCTION, DB_DEVELOPMENT
from scrapper.src.server.model.search_request import PagedRequest, SearchRequest, SearchType
from scrapper.src.server.model.video import Video
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

    async def paged(self, request: Request):
        paged_rq: PagedRequest = await utils.read_request_content(request, PagedRequest)
        videos = self.video_Repo.all()
        videos = limit(videos, paged_rq.PageSize, paged_rq.Skip)

        payload = utils.to_json(*videos)
        return web.Response(status=200, body=payload)

    async def search(self, request: Request):
        search_rq: SearchRequest = await utils.read_request_content(request, SearchRequest)

        if type(search_rq.SearchType) is str:
            search_rq.SearchType = SearchType[search_rq.SearchType]

        videos = self.video_Repo.search(search_rq)

        videos = limit(videos, 1000, 0)
        payload = utils.to_json(*videos)
        return web.Response(status=200, body=payload)


def limit(videos, page_size, skip) -> [Video]:
    if len(videos) > page_size + skip:
        videos = videos[skip: page_size + skip]
    return videos


def server(is_development: bool):
    video_ctrl = new_video_ctrl(is_development)
    app = web.Application()
    app.add_routes([
        web.get('/videos', video_ctrl.videos),
        web.get('/videos/{video_id}', video_ctrl.get_by_id),
        web.get('/videos/favourite/{video_id}', video_ctrl.favourite),
        web.get('/videos/unfavourite/{video_id}', video_ctrl.unfavourite),
        web.post('/videos/paged', video_ctrl.paged),
        web.post('/videos/search', video_ctrl.search),
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
