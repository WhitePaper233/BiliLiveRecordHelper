# -*- coding: utf-8 -*-
import sys

import requests

from utils import logger


class UpInfo:
    """
    Up主信息类
    对https://api.live.bilibili.com/room/v1/Room/room_init这个API的一个封装
    """
    def __init__(self, room_id: int):
        self.__logger = logger.HandleLog()
        self.__room_id = room_id

        # 调用接口获取UP信息
        url = f'https://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}'
        r = requests.get(url)
        up_info = r.json()
        if up_info['code'] == 0:
            # 当接口正常返回结果时
            self.__up_info = up_info
        else:
            self.__logger.critical(f'未找到UID为：{str(self.__room_id)}的主播，请检查配置文件后重新启动')
            sys.exit(24)

    @property
    def room_id(self) -> int:
        return self.__room_id

    @property
    def short_id(self) -> int:
        return self.__up_info['data']['short_id']

    @property
    def uid(self) -> int:
        return self.__up_info['data']['uid']

    @property
    def need_p2p(self) -> bool:
        return False if self.__up_info['data']['need_p2p'] == 0 else True

    @property
    def is_hidden(self) -> bool:
        return self.__up_info['data']['is_hidden']

    @property
    def is_locked(self) -> bool:
        return self.__up_info['data']['is_locked']

    @property
    def is_portrait(self) -> bool:
        return self.__up_info['data']['is_portrait']

    @property
    def live_status(self) -> bool:
        return False if self.__up_info['data']['live_status'] == 0 else True

    @property
    def hidden_till(self) -> int:
        return self.__up_info['data']['hidden_till']

    @property
    def lock_till(self) -> int:
        return self.__up_info['data']['lock_till']

    @property
    def encrypted(self) -> bool:
        return self.__up_info['data']['encrypted']

    @property
    def pwd_verified(self) -> bool:
        return self.__up_info['data']['pwd_verified']

    @property
    def live_time(self) -> int:
        return self.__up_info['data']['live_time']

    @property
    def room_shield(self) -> int:
        return self.__up_info['data']['room_shield']

    @property
    def is_sp(self) -> int:
        return self.__up_info['data']['is_sp']

    @property
    def special_type(self) -> int:
        return self.__up_info['data']['special_type']
