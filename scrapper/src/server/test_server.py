import json

from scrapper.src.server.model.video import Video
from scrapper.tests.integration_test_base import IntegrationTestBase


class IntegrationTestVideos(IntegrationTestBase):

    def test_videos(self):
        result = self.client.get("videos")
        videos = json.loads(result, object_hook=Video)
        self.assertTrue(videos)

    def test_get_by_id(self):
        result = self.client.get("videos/2")
        video = json.loads(result, object_hook=Video)
        self.assertIsNotNone(video)

    def test_favourite(self):
        self.client.get("videos/favourite/2")

    def test_unfavourite(self):
        self.client.get("videos/unfavourite/2")

