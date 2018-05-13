from unittest import TestCase

from aiohttp.web_exceptions import HTTPBadRequest

from scrapper.src.server.common.static import DB_DEVELOPMENT
from scrapper.src.server.model.search_request import SearchRequest, SearchType
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

    def test_search_should_validate_searchField(self):
        for st in [SearchType.all, SearchType.keywords, SearchType.description, SearchType.title, SearchType.date,
                   SearchType.actor]:
            with self.assertRaises(HTTPBadRequest):
                self.repo.search(SearchRequest(SearchField="", SearchType=st))

    def test_search_should_validate_searchType_id(self):
        with self.assertRaises(HTTPBadRequest):
            self.repo.search(SearchRequest(SearchField="l", SearchType=SearchType.id))

    def test_search_favourite(self):
        self.repo.insert(
            [Video(url="1", keywords="item", isFavourite=True), Video(isFavourite=False)],
        )

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="",
            SearchType=SearchType.isFavourite))

        self.assertEqual(1, len(result))
        self.assertEqual("item", result[0].keywords)

    def test_search_description(self):
        self.assert_search_attribute("description")

    def test_search_keywords(self):
        self.assert_search_attribute("keywords")

    def test_search_date(self):
        self.assert_search_attribute("date")

    def test_search_title(self):
        self.assert_search_attribute("title")

    def test_search_actor(self):
        self.assert_search_attribute("actor")

    def assert_search_attribute(self, attr: str):
        valid = Video()
        setattr(valid, attr, "item")
        invalid = Video()
        setattr(invalid, attr, "wrong")

        self.repo.insert([valid, invalid])

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="item",
            SearchType=getattr(SearchType, attr)))

        self.assertEqual(1, len(result))
        self.assertEqual("item", getattr(result[0], attr))

    def test_search_gets_distinct(self):
        self.repo.insert(
            [Video(url="url1", description="special", keywords="special"),
             Video(url="url2", title="special")],
        )

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="special",
            SearchType=SearchType.all))

        self.assertEqual(2, len(result))

    def test_search_all(self):
        self.repo.insert(
            [Video(url="1", description="special"),
             Video(url="2", keywords="special"),
             Video(url="3", actor="special"),
             Video(url="4", date="special"),
             Video(url="5", title="special")],
        )

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="special",
            SearchType=SearchType.all))

        self.assertEqual(5, len(result))

    def test_search_multiple_words_recognized(self):
        self.repo.insert(
            [Video(url="1", description="special"),
             Video(url="2", keywords="actor"),
             Video(url="3", actor="actor"),
             Video(url="4", date="special", actor="actor"),
             Video(url="5", title="special")],
        )

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="special actor",
            SearchType=SearchType.all))

        self.assertEqual(5, len(result))

    def test_search_should_apply_ranking(self):
        self.repo.insert(
            [Video(url="1", title="special title"),
             Video(url="2", description="special description", actor="special", title="special"),
             Video(url="3", actor="special actor", title="special"),
             Video(url="4", description="special description", actor="special", title="special", keywords="special")]
        )

        result: [Video] = self.repo.search(SearchRequest(
            SearchField="special",
            SearchType=SearchType.all))

        self.assertEqual("4", result[0].url)
        self.assertEqual("2", result[1].url)
        self.assertEqual("3", result[2].url)
        self.assertEqual("1", result[3].url)
