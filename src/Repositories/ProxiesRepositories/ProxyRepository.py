import os
import random


class ProxiesRepository:
    def __init__(self):
        self._file_name = 'proxies.txt'
        self._proxies = []
        self.__load_proxies()

    def __load_proxies(self):
        try:
            with open(f'{os.getcwd()}\\proxies.txt', 'r') as f:
                for proxy in f.read().splitlines():
                    self._proxies.append(proxy)
        except (TypeError, FileNotFoundError):
            print(f"[Error] No se ha podido abrir el archivo {self._file_name}")

    def random_proxy(self):
        if len(self._proxies) > 0:
            proxy = random.choice(self._proxies)
            proxies = {
                "http": 'http://' + proxy,
                "https": 'https://' + proxy
            }

            return proxies

        return None

    def remove_proxy(self, proxy):
        try:
            proxy = proxy['http'].replace('http://', '')
            self._proxies.remove(proxy)
        except UnboundLocalError:
            pass
        except ValueError:
            pass
