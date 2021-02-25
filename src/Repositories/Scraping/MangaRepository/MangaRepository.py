import re

from bs4 import BeautifulSoup

from src.Controllers.FtpController.FtpController import FtpController
from src.Repositories.Scraping.ChapterRepository.ChapterRepository import ChapterRepository
from src.Repositories.Scraping.MangaRepository.DataSheetMangaRepository import DataSheetMangaRepository


class MangaRepository:
    def __init__(self, chapter_repository: ChapterRepository, ftp: FtpController):
        self._links = []
        self._chapter_repository = chapter_repository
        self._data_sheet = DataSheetMangaRepository()
        self._ftp = ftp

    def get_episodes_by_manga(self, link: str):
        browser = self._chapter_repository.get_browser()
        browser.get(link)
        bs4 = BeautifulSoup(browser.page_source, "lxml")

        manga_id = self._data_sheet.data_sheet(bs4=bs4, ftp=self._ftp)

        list_episodes_parent = bs4.find("div", id="chapters").find("ul")

        for li in list_episodes_parent.findAll("li"):
            link = li.find("a", {"href": re.compile("view_uploads")})["href"]
            if link not in self._links:
                self._links.append(link)
                print(f"[+] GET {link}")
                self._chapter_repository.get_episode(link=link, manga_id=manga_id)

        self._links.clear()
