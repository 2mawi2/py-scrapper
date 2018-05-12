import os

video_table = "videos"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PRODUCTION = f"{ROOT_DIR}\\..\\..\\..\\..\\resources\\db.json"
DB_DEVELOPMENT = f"{ROOT_DIR}\\..\\..\\..\\..\\resources\\test_db.json"
