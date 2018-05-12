from unittest import TestCase
from tinydb import TinyDB

from scrapper.server.common.static import ROOT_DIR
from scrapper.server.model.Video import Video
from scrapper.server.persistence.video_repo import VideoRepo


class TestVideoRepo(TestCase):
    def setUp(self):
        self.db = TinyDB(f"{ROOT_DIR}\\..\\..\\..\\resources\\db.json")
        self.repo = VideoRepo(self.db)

    def tearDown(self):
        self.repo.close()
        self.repo.delete_all()

    def test_insert(self):
        video = Video()
        self.repo.insert([video])

        res = self.repo.all()

        self.assertEqual(video, res[0])

    def test_all(self):
        videos = [Video(), Video()]
        self.repo.insert(videos)

        res = self.repo.all()

        self.assertEqual(videos, res)

    def test_delete_all(self):
        self.repo.insert([Video()])
        self.repo.delete_all()

        res = self.repo.all()

        self.assertFalse(res)

    def test_favourite(self):
        ids = self.repo.insert([Video(IsFavourite=False)])

        self.repo.favourite(ids[0])

        video = self.repo.get_by_id(ids[0])

        self.assertTrue(video.IsFavourite)
