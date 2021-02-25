import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

from src.Controllers.BrowserController.BrowserController import init_browser
from src.Repositories.Scraping.ChapterRepository.ChapterRepository import ChapterRepository


class LatestEpisodesRepository:
    def __init__(self, chapter_repo: ChapterRepository):
        self._header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        self._link = "https://lectortmo.com/latest_uploads"
        self._chapter_repository = chapter_repo

    def last_chapters_uploaded(self):
        browser = init_browser()
        browser.get(self._link)
        time.sleep(5)
        current_window = browser.current_window_handle
        table = browser.find_elements_by_xpath('//*[@id="latest-uploads"]/div/table/tbody/tr')

        for tr in table:
            try:
                tr.find_element_by_tag_name("a").send_keys(Keys.CONTROL + Keys.RETURN)
                episode_number = tr.find_elements_by_tag_name("td")[2].text
            except ElementNotInteractableException:
                continue

            browser.switch_to.window(browser.window_handles[-1])
            link = browser.current_url
            browser.close()
            browser.switch_to.window(current_window)
            if link is None or link == "":
                continue
            print(f"[+] GET {link} Episode: {episode_number}")
            self._chapter_repository.get_a_chapter(link=link, episode=episode_number)
