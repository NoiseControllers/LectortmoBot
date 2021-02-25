from src.Utils.Mysql.MysqlConnector import MysqlConnector


class ChapterMangaRepository:
    def __init__(self):
        self._my_db = MysqlConnector().connect()

    def check_episode_exists(self, chapter_episode: int, manga_id: int):
        my_cursor = self._my_db.cursor()
        query = "SELECT id FROM chapter WHERE number = %s AND manga_id = %s"

        value = (chapter_episode, manga_id, )
        my_cursor.execute(query, value)
        result = my_cursor.fetchone()

        if result is None:
            return -1

        return result[0]

    def insert_chapter(self, value: tuple) -> int:
        my_cursor = self._my_db.cursor()
        query = "INSERT INTO chapter (slug, name, number, manga_id, user_id, created_at) VALUES (%s, %s, %s, %s, %s, %s)"

        my_cursor.execute(query, value)
        self._my_db.commit()

        return my_cursor.lastrowid
