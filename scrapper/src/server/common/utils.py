import json


def to_json(*videos) -> str:
    return json.dumps([i.__dict__ for i in videos])
