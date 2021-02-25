import logging
import cloudscraper
from lxml.html import fromstring
from src.Repositories.ProxiesRepositories.ProxyRepository import ProxiesRepository

logger = logging.getLogger(__name__)


class SessionController(object):
    def __init__(self):
        self._scraper = cloudscraper.create_scraper()
        # self._proxies_repo = ProxiesRepository()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }

    def get(self, url: str, referer=None):
        # proxies = self._proxies_repo.random_proxy()
        headers = self._headers

        if referer is not None:
            headers["referer"] = referer

        while True:
            try:
                res = self._scraper.get(url, headers=headers, timeout=10)
            except Exception:
                res = None
                # self._proxies_repo.remove_proxy(proxy=proxies)

            if res is None:
                continue

            tree = fromstring(res.content)
            title = tree.findtext('.//title')

            if "Access denied" in title:
                print("[*] Proxy baneado, intentando con otro.")
                continue
            elif res.status_code == 200:
                return res
            elif res.status_code != 200:
                logger.info("HTTP status code: {0}".format(res.status_code))
