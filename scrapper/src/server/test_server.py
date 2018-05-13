import json
from scrapper.src.server.common.static import DB_DEVELOPMENT
from scrapper.src.server.model.search_request import PagedRequest, SearchRequest, SearchType
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_repo import VideoRepo
from scrapper.tests.integration_test_base import IntegrationTestBase


class IntegrationTestVideos(IntegrationTestBase):
    def add_data(self):
        repo = VideoRepo(DB_DEVELOPMENT)
        repo.insert([
            Video(url="some", isFavourite=False),
            Video(url="some", keywords="keyword", isFavourite=True),
            Video(url="some", isFavourite=False),
        ])

    def remove_data(self):
        repo = VideoRepo(DB_DEVELOPMENT)
        repo.delete_all()

    def test_videos(self):
        result = self.client.get("videos")
        videos = json.loads(result, object_hook=Video)
        self.assertTrue(videos)

    def test_paged(self):
        result = self.client.post("videos/paged", PagedRequest(Skip=0, PageSize=2))
        videos = json.loads(result, object_hook=Video)
        self.assertEqual(len(videos), 2)

    def test_get_by_id(self):
        result = self.client.get("videos/2")
        video = json.loads(result, object_hook=Video)
        self.assertIsNotNone(video)

    def test_favourite(self):
        self.client.get("videos/favourite/2")

    def test_unfavourite(self):
        self.client.get("videos/unfavourite/2")

    def test_search(self):
        result = self.client.post("videos/search", SearchRequest(SearchType=SearchType.all, SearchField="keywords"))
        video = json.loads(result, object_hook=Video)
        self.assertIsNotNone(video)
