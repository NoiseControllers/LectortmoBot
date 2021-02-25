from datetime import datetime


class ChapterModel(object):
    def __init__(self, slug: int, name: int, number: int, manga_id: int, user_id: int):
        self._slug = slug
        self._name = name
        self._number = number
        self._manga_id = manga_id
        self._user_id = user_id
        self._created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def slug(self) -> int:
        return self._slug

    @property
    def name(self) -> int:
        return self._name

    @property
    def number(self) -> int:
        return self._number

    @property
    def manga_id(self) -> int:
        return self._manga_id

    @property
    def user_id(self) -> int:
        return self._user_id

    def prepare_for_sql(self):
        return self.slug, self.name, self.number, self.manga_id, self.user_id, self._created_at
