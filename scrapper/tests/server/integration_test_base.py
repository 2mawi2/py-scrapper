import multiprocessing
from unittest import TestCase

from scrapper.src.server.server import app
from scrapper.tests.server.http_client import HttpClient


class IntegrationTestBase(TestCase):
    @staticmethod
    def start_flask_app():
        app.run(debug=True, use_reloader=False)

    def run_server(self):
        self.p = multiprocessing.Process(name="server_process", target=self.start_flask_app)
        self.p.daemon = True
        self.p.start()

    def setUp(self):
        self.run_server()
        self.client = HttpClient("http://localhost:5000/")

    def tearDown(self):
        self.p.terminate()
