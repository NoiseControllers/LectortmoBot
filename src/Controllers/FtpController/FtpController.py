import os
from ftplib import FTP

from src.Utils.ConfigManagement.ConfigManagement import ConfigManagement


class FtpController:
    def __init__(self):
        self._config = ConfigManagement().config()
        self._base_directory = self._config.get("FTP", "base_directory")
        self._ftp = self.__connect()

    def __connect(self):
        ftp = FTP()
        ftp.connect(host=self._config.get("FTP", "server"), port=self._config.getint("FTP", "port"))
        ftp.login(user=self._config.get("FTP", "user"), passwd=self._config.get("FTP", "password"))

        return ftp

    def prepare_directories_for_upload(self, folders: list):
        self._ftp.cwd(self._base_directory)
        for folder in folders:
            folder = str(folder).lower()
            if folder not in self._ftp.nlst():
                self._ftp.mkd(folder)
            self._ftp.cwd(folder)

    def upload_files(self, local_path: str):
        print("[*] Starting the FTP upload.")
        for root, dirs, files in os.walk(local_path):
            for f_name in files:
                full_filename = os.path.join(root, f_name)
                fh = open(full_filename, 'rb')
                try:
                    self._ftp.storbinary("STOR " + f_name, fh)
                except ConnectionResetError:
                    self._ftp = self.__connect()
                    self.upload_files(local_path=local_path)
                finally:
                    fh.close()
        print("[✓] Uploaded sucesfully!")

    def upload_thumbnail(self, folder_name: str, thumbnail: str, local_path: str):
        print("[*] Starting uploade of thumbnail")
        self._ftp.cwd(self._base_directory)
        if folder_name not in self._ftp.nlst():
            self._ftp.mkd(folder_name)
        self._ftp.cwd(folder_name)
        if "cover" not in self._ftp.nlst():
            self._ftp.mkd("cover")
        self._ftp.cwd("cover")

        full_filename = os.path.join(local_path, thumbnail)
        fh = open(full_filename, 'rb')
        self._ftp.storbinary("STOR " + thumbnail, fh)
        fh.close()
        print("[✓] Uploaded sucesfully!")
