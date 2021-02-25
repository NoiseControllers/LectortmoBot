from src.Utils.Mysql.MysqlConnector import MysqlConnector


class PageChapterRepository:
    def __init__(self):
        self._my_db = MysqlConnector().connect()

    def insert_page(self, value: list):
        my_cursor = self._my_db.cursor()
        query = "INSERT INTO page (slug, image, chapter_id) VALUES (%s, %s, %s)"

        my_cursor.executemany(query, value)
        self._my_db.commit()
