class PageChapterModel(object):
    def __init__(self, slug: int, image: str, chapter_id: int):
        self._slug = slug
        self._image = image
        self._chapter_id = chapter_id

    @property
    def slug(self) -> int:
        return self._slug

    @property
    def image(self) -> str:
        return self._image

    @property
    def chapter_id(self):
        return self._chapter_id

    def prepare_for_sql(self):
        return self.slug, self.image, self.chapter_id
