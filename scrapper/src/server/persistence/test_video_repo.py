from unittest import TestCase
from tinydb import TinyDB

from scrapper.src.server.common.static import ROOT_DIR, DB_DEVELOPMENT
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_repo import VideoRepo


class TestVideoRepo(TestCase):
    def setUp(self):
        self.repo = VideoRepo(DB_DEVELOPMENT)

    def tearDown(self):
        self.repo.delete_all()

    def test_insert(self):
        video = Video()
        self.repo.insert([video])

        res = self.repo.all()

        video.video_id = 1

        self.assertEqual(video, res[0])

    def test_all(self):
        videos = [Video(), Video()]
        self.repo.insert(videos)

        res = self.repo.all()

        self.assertTrue(res)

    def test_delete_all(self):
        self.repo.insert([Video()])
        self.repo.delete_all()

        res = self.repo.all()

        self.assertFalse(res)

    def test_favourite(self):
        ids = self.repo.insert([Video(isFavourite=False)])

        self.repo.favourite(ids[0])

        video = self.repo.get_by_id(ids[0])

        self.assertTrue(video.isFavourite)

    def test_unfavourite(self):
        ids = self.repo.insert([Video(isFavourite=True)])

        self.repo.unfavourite(ids[0])

        video = self.repo.get_by_id(ids[0])

        self.assertFalse(video.isFavourite)
