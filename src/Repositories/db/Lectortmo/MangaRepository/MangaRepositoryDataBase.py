from src.Utils.Mysql.MysqlConnector import MysqlConnector


class MangaRepositoryDataBase:
    def __init__(self):
        self._my_db = MysqlConnector().connect()

    def check_manga_exists(self, slug: str) -> int:
        my_cursor = self._my_db.cursor()
        query = "SELECT id FROM manga where slug = %s"
        value = (slug,)

        my_cursor.execute(query, value)
        result = my_cursor.fetchone()

        if result is None:
            return -1

        return result[0]

    def insert_manga(self, value) -> int:
        my_cursor = self._my_db.cursor()
        query = "INSERT INTO manga (slug, name, otherNames, summary, cover, type_id, status_id, user_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, 1, 1, %s)"
        my_cursor.execute(query, value)
        self._my_db.commit()

        return my_cursor.lastrowid

    def comic_type(self, label: str):
        my_cursor = self._my_db.cursor()
        query = "SELECT id FROM comictype WHERE label = %s"

        value = (label,)

        my_cursor.execute(query, value)
        result = my_cursor.fetchone()

        if result is None:
            return -1

        return result[0]
