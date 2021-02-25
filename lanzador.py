import re
import time

import pyperclip as pyperclip

from src.Controllers.FtpController.FtpController import FtpController
from src.Controllers.SessionController.SessionController import SessionController
from src.Repositories.Scraping.ChapterRepository.ChapterRepository import ChapterRepository
from src.Repositories.Scraping.LatestEpisodesRepository.LatestEpisodesRepository import LatestEpisodesRepository
from src.Repositories.Scraping.MangaRepository.MangaRepository import MangaRepository
import sys

session = SessionController()
ftp = FtpController()

CHAPTER = ChapterRepository(sess=session, ftp=ftp)
MANGA = MangaRepository(chapter_repository=CHAPTER, ftp=ftp)

PATTERN = "^.*(library|viewer).*$"
PATTERN_MANGA = "^.*(library).*$"
PATTERN_EPISODE = "^.*(viewer).*$"
HISTORY_LIST = []


def manual_search():
    print("Tan solo copia el link y automaticamente el bot lo procesara.")
    while True:
        link = __get_link_valid()
        print(f"[+] {link}")
        if re.match(PATTERN_MANGA, link):
            MANGA.get_episodes_by_manga(link=link)
        elif re.match(PATTERN_EPISODE, link):
            CHAPTER.get_episode(link=link, manga_id=-2)
        else:
            print("[-] Enlace no valido.")
        print("[*] Esperando nuevo enlace.")


def automatic_search():
    latest = LatestEpisodesRepository(chapter_repo=CHAPTER)
    latest.last_chapters_uploaded()


def main():
    print("1. Modo Manual.")
    print("2. Modo Automatico (Ultimos subidos)")
    print("3. Salir")

    opt = int(input("Opcion: "))

    if opt == 1:
        print("[*] Opcion Manual.")
        manual_search()
    elif opt == 2:
        print("[*] Opcion Automatica.")
        automatic_search()
    elif opt == 3:
        sys.exit(0)
    elif opt < 1 or opt > 3:
        print("[-] Opcion no valida.")
        main()


def __get_link_valid():
    while True:
        time.sleep(0.5)
        if re.search(PATTERN, pyperclip.paste()) and pyperclip.paste() not in HISTORY_LIST:
            HISTORY_LIST.append(pyperclip.paste())
            return pyperclip.paste()


if __name__ == '__main__':
    print("Lectortmo V.1.0.0 | Decibel150 | esdecibel150@gmail.com \n")
    try:
        main()
    except KeyboardInterrupt:
        print("[*] Programa detenido por el usuario.")

