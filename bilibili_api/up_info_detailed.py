# -*- coding: utf-8 -*-
import sys
import time
from time import struct_time

import requests

from utils import logger


class Up:
    """
    UP主类
    对https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo这个API的一个封装
    """

    def __init__(self, uid: int):
        self.__logger = logger.HandleLog()
        self.__uid = uid

        # 调用接口获取UP主直播间信息
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?uids={uid}&;req_biz=video'
        r = requests.get(url)
        up_data = r.json()
        if up_data['code'] == 0 and bool(up_data['data']['by_uids']):
            # 当接口正常返回结果时
            self.__up_data = up_data
        else:
            self.__logger.critical(f'未找到UID为：{str(self.__uid)}的主播，请检查配置文件后重新启动')
            sys.exit(24)

    @property
    def uid(self) -> int:
        return self.__uid

    @property
    def room_id(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['room_id']

    @property
    def live_status(self) -> bool:
        return True if self.__up_data['data']['by_uids'][str(self.__uid)]['live_status'] == 1 else False

    @property
    def live_url(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['live_url']

    @property
    def parent_area_id(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['parent_area_id']

    @property
    def title(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['title']
    
    @property
    def parent_area_name(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['parent_area_name']

    @property
    def area_name(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['area_name']

    @property
    def live_time(self) -> struct_time:
        return time.strptime(self.__up_data['data']['by_uids'][str(self.__uid)]['live_time'], '%Y-%m-%d %H:%M-%S')

    @property
    def description(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['description']

    @property
    def tags(self) -> tuple:
        return tuple(self.__up_data['data']['by_uids'][str(self.__uid)]['tags'])

    @property
    def attention(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['attention']

    @property
    def online(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['online']

    @property
    def short_id(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['short_id']

    @property
    def uname(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['uname']

    @property
    def cover(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['cover']

    @property
    def background(self) -> str:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['background']

    @property
    def join_slide(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['join_slide']

    @property
    def live_id(self) -> int:
        return self.__up_data['data']['by_uids'][str(self.__uid)]['live_id']


if __name__ == '__main__':
    up = Up(416622817)
    print(up.uname)
