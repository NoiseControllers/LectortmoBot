from datetime import datetime
from typing import Tuple


class MangaModel(object):
    def __init__(
            self,
            slug: str,
            name: str,
            other_names: str,
            description: str,
            type_id: int
    ):
        self._slug = slug
        self._name = name
        self._other_names = other_names
        self._summary = description
        self._cover = 1
        self._type_id = type_id
        self._created_at = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def slug(self) -> str:
        return self._slug

    @property
    def name(self) -> str:
        return self._name

    @property
    def other_names(self) -> str:
        return self._other_names

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def cover(self) -> int:
        return self._cover
    
    @property
    def type_id(self) -> int:
        return self._type_id

    @property
    def created_at(self):
        return str(self._created_at)

    def __iter__(self):
        return iter([
            self.slug,
            self.name,
            self.other_names,
            self.summary,
            self.cover,
            self.type_id,
            self.created_at
        ])
