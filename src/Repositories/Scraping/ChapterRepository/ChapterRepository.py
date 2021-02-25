import mimetypes
import re
import time

import requests
from bs4 import BeautifulSoup

from src.Controllers.BrowserController.BrowserController import init_browser
from src.Controllers.FtpController.FtpController import FtpController
from src.Controllers.ManagementDirectories.ManagementDirectory import ManagementDirectory
from src.Controllers.SessionController.SessionController import SessionController
from src.Models.Lectortmo.ChapterModel.ChapterModel import ChapterModel
from src.Models.Lectortmo.PageChapterModel.PageChapterModel import PageChapterModel
from src.Repositories.Scraping.MangaRepository.DataSheetMangaRepository import DataSheetMangaRepository
from src.Repositories.db.Lectortmo.ChapterMangaRepository.ChapterMangaRepository import ChapterMangaRepository
from src.Repositories.db.Lectortmo.PageChapterRepository.PageChapterRepository import PageChapterRepository


class ChapterRepository:
    def __init__(self, sess: SessionController, ftp: FtpController):
        self._header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        self._sess = sess
        self._directory = ManagementDirectory()
        self._path = None
        self._browser = init_browser()
        self._chapter_repository = ChapterMangaRepository()
        self._page_repository = PageChapterRepository()
        self._data_sheet = DataSheetMangaRepository()
        self._ftp = ftp

    def get_episode(self, link: str, manga_id: int):
        self._browser.get(link)
        if "lectortmo.com" not in self._browser.current_url:
            print("[-] Redireccion detectada, volviendo a intentar.")
            self.get_episode(link=link, manga_id=manga_id)
            time.sleep(5)

        bs4 = BeautifulSoup(self._browser.page_source, "lxml")

        try:
            link_resolve = bs4.find("meta", {"property": "og:url"})["content"]
            link_resolve = link_resolve.replace("paginated", "cascade")
        except TypeError:
            time.sleep(10)
            print(link, manga_id, self._browser.current_url)
            self.get_episode(link=link, manga_id=manga_id)

        title = str(bs4.find("h1").get_text())

        link_parent_manga = str(bs4.find("a", {"title": "Volver"})["href"])
        slug = link_parent_manga.split("/")[6]

        episode_number = self.__episode_number_format(string=str(bs4.find("h2").get_text()))
        folder = f"{str(episode_number)}"

        if manga_id == -2:
            self._browser.get(link_parent_manga)
            bs4 = BeautifulSoup(self._browser.page_source, "lxml")
            manga_id = self._data_sheet.data_sheet(bs4=bs4, ftp=self._ftp)

        chapter_id = self._chapter_repository.check_episode_exists(chapter_episode=episode_number, manga_id=manga_id)

        if chapter_id == -1:
            chapter_obj = ChapterModel(
                slug=episode_number,
                name=episode_number,
                number=episode_number,
                manga_id=manga_id,
                user_id=1
            )
            chapter_id = self._chapter_repository.insert_chapter(value=chapter_obj.prepare_for_sql())
            self._path = self._directory.make_directory(name_folder=slug, chapter=folder)
            folders_ftp = [slug, "chapters", folder]

            self._ftp.prepare_directories_for_upload(folders=folders_ftp)
            self.__get_images(link=link_resolve, chapter_id=chapter_id)
        else:
            print(f"[*] El episodio {episode_number} de {title} ya existe en DB.")

    def get_a_chapter(self, link: str, episode):
        self._browser.get(link)

        if "lectortmo.com" not in self._browser.current_url:
            print("[-] Redireccion detectada, volviendo a intentar.")
            self.get_a_chapter(link=link, episode=episode)
            time.sleep(5)

        bs4 = BeautifulSoup(self._browser.page_source, "lxml")

        manga_id = self._data_sheet.data_sheet(bs4=bs4, ftp=self._ftp)

        try:
            list_episodes_parent = bs4.find("div", id="chapters").find("ul")
        except AttributeError:
            list_episodes_parent = None

        episode_search = f"Capítulo {episode}"

        if list_episodes_parent is not None:
            for episode in list_episodes_parent.find_all("li"):
                try:
                    episode_number = str(episode.find("h4").get_text()).strip()
                except AttributeError:
                    continue
                if episode_search in episode_number:
                    link = episode.find("a", {"href": re.compile("view_uploads")})["href"]
                    self.get_episode(link=link, manga_id=manga_id)
                    break

    def __get_images(self, link: str, chapter_id: int):
        bs4 = BeautifulSoup(self._sess.get(link).content, "lxml")
        cascade_images = bs4.find("div", id="main-container").findAll("img")

        values = []

        for x, image in enumerate(cascade_images):
            try:
                resp = requests.get(image["data-src"], headers=self._header)
            except Exception:
                print("[-] No se ha podido bajar la imagen.")
                resp = None

            if resp is None:
                continue

            if resp.status_code == 200:
                content_type = resp.headers['content-type']
                extension = mimetypes.guess_extension(content_type)
                episode = x + 1
                temp_name = f"{episode}{extension}"
                print(f"[+] Downloading: {temp_name}")
                with open(f'{self._path}\\{temp_name}', 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                post_obj = PageChapterModel(slug=episode, image=temp_name, chapter_id=chapter_id)
                values.append(post_obj.prepare_for_sql())

        self._ftp.upload_files(local_path=self._path)
        self._page_repository.insert_page(value=values)

    def get_browser(self):
        return self._browser

    @staticmethod
    def __episode_number_format(string: str) -> int:
        string = string.split(" ")
        # Limpia los vacios
        string = [x for x in string if x != '']
        string = string[1].split(":")[0]
        number = round(float(string.strip()))

        return int(number)
