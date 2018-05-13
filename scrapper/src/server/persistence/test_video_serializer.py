from unittest import TestCase

from scrapper.src.server.model.video import Video
from scrapper.src.server.persistence.video_serializer import serialize, deserialize


class TestSerializer(TestCase):

    def test_serialize(self):
        result = serialize([Video(isFavourite=False, description="description")])
        self.assertEqual(result[0], {'actor': '',
                                     'date': '',
                                     'description': 'description',
                                     'isFavourite': False,
                                     'keywords': '',
                                     'preview': '',
                                     'title': '',
                                     'url': ''})

    def test_deserialize(self):
        video = ElementMock({'actor': '',
                             'date': '',
                             'description': 'description',
                             'isFavourite': True,
                             'keywords': '',
                             'preview': '',
                             'title': '',
                             'url': ''})
        video.doc_id = 1

        result = deserialize([video])
        self.assertEqual(result[0], Video(video_id=1, isFavourite=True, description="description"))


class ElementMock(dict):
    doc_id: int
