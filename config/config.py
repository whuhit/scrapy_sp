import os
import configparser


class Config(object):
    def __init__(self, config_file='config/config.ini'):
        self._path = config_file
        if not os.path.exists(self._path):
            raise FileNotFoundError("No such file: config.ini")
        self._config = configparser.ConfigParser()
        self._config.read(self._path, encoding='utf-8-sig')

    def get(self, section, name):
        return self._config.get(section, name)
