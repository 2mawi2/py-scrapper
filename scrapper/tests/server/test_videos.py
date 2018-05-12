from scrapper.tests.server.integration_test_base import IntegrationTestBase


class IntegrationTestVideos(IntegrationTestBase):
    def test_videos(self):
        result = self.client.get("videos")
        self.assertEqual("videos", result)
