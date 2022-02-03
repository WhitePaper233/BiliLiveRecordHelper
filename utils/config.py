# -*- coding: utf-8 -*-
import os
import sys
from shutil import copy

import yaml

from utils import logger


class Config:
    """对配置文件经行操作的库"""

    def __init__(self):
        self.__template = './template/config.yaml'  # 配置文件模板路径
        self.__path = './config.yaml'  # 配置文件路径

        self.__logger = logger.HandleLog()

        self.__logger.info('正在读取配置文件...')
        # 读取配置文件
        if os.path.exists(self.__path):
            with open(self.__path, 'r', encoding='utf8') as f:
                self.__config = yaml.load(f.read(), Loader=yaml.FullLoader)
        # 如果没有就重新生成一份
        else:
            copy(self.__template, self.__path)
            # 因为没有配置文件，所以默认应该为INFO级
            self.__logger.warning('未检测到配置文件，已自动生成，请进行配置后重新启动')
            self.__logger.info('正在退出...')
            sys.exit()

    @property
    def config(self) -> dict:
        return self.__config

    @property
    def room_id(self) -> int:
        return self.__config['room_id']

    @property
    def log_level(self) -> str:
        return self.__config['log_level']


if __name__ == '__main__':
    print(Config().room_id)
