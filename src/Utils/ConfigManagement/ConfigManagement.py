import configparser
import os


class ConfigManagement:
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config = None
        self.__init()

    def __init(self):
        self._config_parser.read(f'{os.getcwd()}\\config.ini')
        self._config = self._config_parser

    def max_threads(self) -> int:
        return int(self._config['DEFAULT']['MAX_THREADS'])

    def pause_time(self) -> int:
        return int(self._config['DEFAULT']['DEFAULT_TIME_PAUSE'])

    def user_agent(self) -> str:
        return self._config['DEFAULT']['USER-AGENT']

    def data_site_key(self) -> str:
        return str(self._config['RECAPTCHA']['DATA-SITE-KEY'])

    def api_key(self) -> str:
        return str(self._config['2CAPTCHA']['API-KEY'])

    def config(self) -> configparser.ConfigParser:
        return self._config
