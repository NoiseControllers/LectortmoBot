class CategoryModel(object):
    def __init__(self, manga_id: int, category_id: int):
        self._manga_id = manga_id
        self._category_id = category_id

    @property
    def manga_id(self) -> int:
        return self._manga_id

    @property
    def category_id(self) -> int:
        return self._category_id

    def prepare_for_sql(self) -> tuple:
        return self.manga_id, self.category_id
