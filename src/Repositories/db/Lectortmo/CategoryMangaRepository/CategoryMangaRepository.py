from src.Utils.Mysql.MysqlConnector import MysqlConnector


class CategoryMangaRepository:
    def __init__(self):
        self._my_db = MysqlConnector().connect()

    def id_category(self, category: str) -> int:
        my_cursor = self._my_db.cursor()
        query = "SELECT id FROM category WHERE name = %s"
        value = (category,)

        my_cursor.execute(query, value)
        result = my_cursor.fetchone()

        if result is None:
            return -1

        return result[0]

    def insert_category_manga(self, categories: list):
        my_cursor = self._my_db.cursor()
        query = "INSERT INTO category_manga (manga_id, category_id) VALUES (%s, %s)"

        my_cursor.executemany(query, categories)
        self._my_db.commit()
