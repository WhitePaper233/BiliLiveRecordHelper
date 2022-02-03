# -*- coding: utf-8 -*-
import os
import sys

import requests
import colorama
import datetime
import time
import urllib3

from datetime import datetime

from utils import logger
from bilibili_api import up_info_basic
from bilibili_api import live_stream
from bilibili_api import up_info_detailed


class _Flv_Stream:
    """FLV流类"""

    def __init__(self, url: str, up_info: up_info_detailed.Up):
        urllib3.disable_warnings()

        self.__play_url = url

        self.up_info = up_info

        self.__capture_path = os.path.join('./recordings', self.up_info.uname)

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'}

        if not os.path.exists(self.__capture_path):
            os.mkdir(self.__capture_path)

        self.__logger = logger.HandleLog()

    def capture(self):
        size = 0
        cap = requests.get(self.__play_url, headers=self.headers, stream=True, verify=False)
        index = 1

        while True:
            if index == 1:
                name = f'{datetime.now().strftime("%Y-%m-%d")}-{self.up_info.title}'
            else:
                name = f'{datetime.now().strftime("%Y-%m-%d")}-{self.up_info.title}-{index}'

            if os.path.exists(os.path.join(self.__capture_path, f'{name}.flv')):
                index += 1
            else:
                break

        try:
            start_time = time.time()
            with open(os.path.join(self.__capture_path, f'{name}.flv'), 'wb') as f:
                self.__logger.info('开始捕获直播，使用 Ctrl+C 停止捕获')
                for data in cap.iter_content(chunk_size=1024):
                    f.write(data)
                    size += len(data)
                    f.flush()
                    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sys.stdout.write(f'[{now_time}]{colorama.Fore.CYAN}[INFO]{colorama.Fore.WHITE} 正在捕获直播:%.2f MB |'
                                     f' {int(time.time() - start_time)}s' % float(size / 1024 / 1024) + '\r')
        except KeyboardInterrupt:
            sys.stdout.write(f'[{now_time}]{colorama.Fore.CYAN}[INFO]{colorama.Fore.WHITE} 正在停止捕获:\n')
            time.sleep(0.2)
            self.__logger.info(f'捕获结束，大小: %.2fMB' % float(size / 1024 / 1024))
            self.__logger.info('bye~')
            sys.exit()


class Stream:
    """直播流类"""

    def __init__(self, room_id: int):
        self.__logger = logger.HandleLog()
        self.__room_id = room_id

    def get_flv_stream(self):
        self.__logger.info(f'正在获取直播间{self.__room_id}的直播流信息')
        up_info = up_info_basic.UpInfo(self.__room_id)
        up_info_detail = up_info_detailed.Up(up_info.uid)
        if up_info.live_status:
            play_url = live_stream.LiveStream(self.__room_id).get_stream_url()
            self.__logger.info(f'成功获取到直播流')
            self.__logger.info(f'正在开始捕获直播：{up_info_detail.title}，主播：{up_info_detail.uname}')
            return _Flv_Stream(play_url, up_info_detail)
        else:
            self.__logger.info('主播暂未开启直播')
