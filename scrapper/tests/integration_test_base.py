import abc
import multiprocessing
from multiprocessing import Process
from unittest import TestCase
from scrapper.src.server.server import server
from scrapper.tests.http_client import HttpClient

server_process: Process


class IntegrationTestBase(TestCase):
    @abc.abstractmethod
    def add_data(self):
        pass

    @abc.abstractmethod
    def remove_data(self):
        pass

    @classmethod
    def setUpClass(cls):
        global server_process
        server_process = multiprocessing.Process(name="server", target=server, args=(True,))
        server_process.daemon = True
        server_process.start()

    @classmethod
    def tearDownClass(cls):
        global server_process
        server_process.terminate()

    def setUp(self):
        self.client = HttpClient("http://localhost:5000/")
        self.add_data()

    def tearDown(self):
        self.remove_data()
