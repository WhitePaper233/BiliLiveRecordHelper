# -*- coding: utf-8 -*-
import sys

import requests

from utils import logger


class LiveStream:
    """
    直播流类
    对https://api.live.bilibili.com/room/v1/Room/playUrl这个API的一个封装
    """
    def __init__(self, room_id: int, quality: int = 4):
        """
        :param room_id: 房间号
        :param quality: 画质 (2：流畅 | 3：高清 |4：原画)，缺省值为4
        """
        self.__room_id = room_id
        self.__quality = quality
        self.__logger = logger.HandleLog()

        # 调用接口获取直播流URL
        url = f'https://api.live.bilibili.com/room/v1/Room/playUrl?cid={self.__room_id}&quality={self.__quality}'
        r = requests.get(url)
        live_stream = r.json()
        if live_stream['code'] == 19002003:
            self.__logger.critical('房间信息不存在，请检查配置文件')
            sys.exit(24)
        elif live_stream['code'] == -400:
            self.__logger.critical('画质设置错误，请检查配置文件')
            sys.exit(32)
        elif live_stream['code'] == 0:
            self.__live_stream = live_stream
        else:
            self.__logger.critical(f'请求直播流时发生未知错误，错误代码：{live_stream["code"]}')
            sys.exit(37)

    @property
    def current_quality(self) -> int:
        return self.__live_stream['data']['current_quality']

    @property
    def accept_quality(self) -> tuple:
        return tuple(self.__live_stream['data']['accept_quality'])

    @property
    def current_qn(self) -> int:
        return self.__live_stream['data']['current_qn']

    @property
    def quality_description_desc(self) -> str:
        return self.__live_stream['data']['quality_description']['desc']

    @property
    def durl(self) -> tuple:
        return tuple(self.__live_stream['data']['durl'])

    @property
    def stream_urls(self) -> tuple:
        return tuple(url_array['url'] for url_array in self.__live_stream['data']['durl'])

    def get_stream_url(self) -> str:
        return self.stream_urls[0]
