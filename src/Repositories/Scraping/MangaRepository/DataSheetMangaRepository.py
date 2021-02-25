import mimetypes

from bs4 import BeautifulSoup

from src.Controllers.FtpController.FtpController import FtpController
from src.Controllers.ManagementDirectories.ManagementDirectory import ManagementDirectory
from src.Models.Lectortmo.MangaModel.CategoriesModel.CategoryModel import CategoryModel
from src.Models.Lectortmo.MangaModel.MangaModel import MangaModel
from src.Repositories.db.Lectortmo.CategoryMangaRepository.CategoryMangaRepository import CategoryMangaRepository
from src.Repositories.db.Lectortmo.MangaRepository.MangaRepositoryDataBase import MangaRepositoryDataBase
import requests
import os


class DataSheetMangaRepository:
    def __init__(self):
        self._bs4 = None or BeautifulSoup
        self._manga_repository = MangaRepositoryDataBase()
        self._category_repository = CategoryMangaRepository()
        self._management_directory = ManagementDirectory()

    def data_sheet(self, bs4: BeautifulSoup, ftp: FtpController) -> int:
        self._bs4 = bs4
        type_manga = str(bs4.find("h1", class_="book-type").get_text()).strip()
        type_manga = type_manga.lower().capitalize()
        type_id = self._manga_repository.comic_type(label=type_manga)

        if type_id == -1:
            type_id = None

        manga_obj = MangaModel(
            slug=self.__slug(),
            name=self.__title(),
            other_names=self.__title(),
            description=self.__description(),
            type_id=type_id
        )

        # Return the id of the sleeve in db | -1 no exists
        exists_manga_in_db = self._manga_repository.check_manga_exists(slug=manga_obj.slug)

        if exists_manga_in_db == -1:
            manga_id = self._manga_repository.insert_manga(value=tuple(manga_obj))
            categories = self.__categories(manga_id=manga_id)
            self._category_repository.insert_category_manga(categories=categories)
            self.__thumbnail(ftp=ftp)
            return manga_id

        return exists_manga_in_db

    def __slug(self) -> str:
        bs4 = self._bs4

        link = str(bs4.find("meta", {"property": "og:url"})["content"])
        link = link.split("/")

        return link[6].lower()

    def __categories(self, manga_id: int) -> list:
        bs4 = self._bs4
        genres = []
        categories = []

        category = str(bs4.find("div", class_="demography").get_text())
        genres.append(category.strip())
        temp_genres = bs4.find_all("h6")

        for genre in temp_genres:
            genre = genre.get_text()
            genres.append(genre)

        for genre in genres:
            category_id = self._category_repository.id_category(category=genre)
            if category_id == -1:
                continue
            categories.append(CategoryModel(manga_id=manga_id, category_id=category_id).prepare_for_sql())

        return categories

    def __title(self) -> str:
        bs4 = self._bs4

        title = str(bs4.find("h2").get_text())

        return title

    def __description(self) -> str:
        bs4 = self._bs4

        description = str(bs4.find("p", class_="element-description").get_text())

        return description

    def __thumbnail(self, ftp: FtpController) -> None:
        bs4 = self._bs4

        thumbnail = str(bs4.find("img", class_="book-thumbnail")["src"])

        resp = requests.get(thumbnail, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
        self._management_directory.base_directory(name_folder=self.__slug())
        if resp.status_code == 200:
            content_type = resp.headers['content-type']
            extension = mimetypes.guess_extension(content_type)
            temp_name = f"cover_thumb{extension}"
            temp_name_2 = f"cover_250x350{extension}"
            files_save = [temp_name, temp_name_2]
            path = f"{os.getcwd()}\\uploads\\manga\\{self.__slug()}\\cover\\"
            for temp_name in files_save:
                with open(f"{path}{temp_name}", 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)

                ftp.upload_thumbnail(folder_name=self.__slug(), thumbnail=temp_name, local_path=path)
