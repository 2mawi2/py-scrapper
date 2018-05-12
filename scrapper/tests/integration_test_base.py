import multiprocessing
from unittest import TestCase

from scrapper.src.server.common.static import DB_DEVELOPMENT
from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_repo import VideoRepo
from scrapper.src.server.server import server
from scrapper.tests.http_client import HttpClient


def add_data():
    repo = VideoRepo(DB_DEVELOPMENT)
    repo.insert([
        Video(url="some", isFavourite=False),
        Video(url="some", isFavourite=True)
    ])


def remove_data():
    repo = VideoRepo(DB_DEVELOPMENT)
    repo.delete_all()


class IntegrationTestBase(TestCase):
    def run_server(self):
        self.p = multiprocessing.Process(name="server", target=server, args=(True,))
        self.p.daemon = True
        self.p.start()

    def setUp(self):
        self.run_server()
        self.client = HttpClient("http://localhost:5000/")
        add_data()

    def tearDown(self):
        self.p.terminate()
        remove_data()

    def addCleanup(self, function, *args, **kwargs):
        super().addCleanup(function, *args, **kwargs)





