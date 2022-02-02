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


class _Flv_Stream:
    """FLV流类"""

    def __init__(self, url: str):
        urllib3.disable_warnings()

        self.__play_url = url

        self.__capture_path = './recordings'

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
                name = f'{datetime.now().strftime("%Y-%m-%d")}'
            else:
                name = f'{datetime.now().strftime("%Y-%m-%d")}-{index}'

            if os.path.exists(os.path.join(self.__capture_path, f'{name}.flv')):
                index += 1
            else:
                break

        try:
            start_time = time.time()
            with open(os.path.join(self.__capture_path, f'{name}.flv'), 'wb') as f:
                self.__logger.info('开始捕获直播')
                for data in cap.iter_content(chunk_size=1024):
                    f.write(data)
                    size += len(data)
                    f.flush()
                    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sys.stdout.write(f'[{now_time}]{colorama.Fore.CYAN}[INFO]{colorama.Fore.WHITE}正在捕获直播:%.2fMB |'
                                     f' {int(time.time() - start_time)}s' % float(size / 1024 / 1024) + '\r')
        except KeyboardInterrupt:
            sys.stdout.write(f'[{now_time}]{colorama.Fore.CYAN}[INFO]{colorama.Fore.WHITE} 正在停止捕获...')
            time.sleep(0.2)
            self.__logger.info(f'[{now_time}]{colorama.Fore.CYAN}[INFO]{colorama.Fore.WHITE}捕获结束，大小:'
                               f'%.2fMB' % float(size / 1024 / 1024))
            print('bye~')
            sys.exit()


class Stream:
    """直播流类"""

    def __init__(self, room_id: str):
        self.__logger = logger.HandleLog()
        self.__room_id = room_id

    def get_flv_stream(self):
        self.__logger.info(f'正在获取直播间{self.__room_id}的直播流信息')
        api_url = f"https://api.live.bilibili.com/room/v1/Room/playUrl?cid={self.__room_id}&qn=0&platform=web"
        api = requests.get(api_url).json()
        play_url = api['data']['durl'][0]['url']
        self.__logger.info(f'成功获取到直播流，地址为：{play_url}')
        return _Flv_Stream(play_url)
