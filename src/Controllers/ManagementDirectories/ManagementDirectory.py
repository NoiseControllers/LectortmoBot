import os


class ManagementDirectory:
    def __init__(self):
        self._path = os.getcwd()
        self._parent_folder = "uploads\\manga"

    def make_directory(self, name_folder: str, chapter: str) -> str:
        name_folder = self.__clean_name_folder(name_folder=name_folder)
        path = f"{self._path}\\{self._parent_folder}\\{name_folder}\\chapters\\{chapter}"
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def base_directory(self, name_folder: str):
        name_folder = self.__clean_name_folder(name_folder=name_folder)
        path = f"{self._path}\\{self._parent_folder}\\{name_folder}\\cover"

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    @staticmethod
    def __clean_name_folder(name_folder):
        words = [":"]

        for word in words:
            name_folder = name_folder.replace(word, "")

        return name_folder.strip().lower()
