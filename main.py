import json
import requests
import time
import os
import urllib.request
import argparse
import pandas as pd

from tools.util import get_current_time_format, generate_url_with_xbs, sleep_random
from config import IS_SAVE, SAVE_FOLDER, USER_SEC_UID, IS_WRITE_TO_CSV, LOGIN_COOKIE, CSV_FILE_NAME
import requests

import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 创建日志器
logger = logging.getLogger(__name__)


class DouYinUtil(object):

    def __init__(self, sec_uid: str):
        """
        :param sec_uid: 抖音id
        """
        self.sec_uid = sec_uid
        self.is_save = IS_SAVE
        self.save_folder = SAVE_FOLDER
        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)
        self.is_write_to_csv = IS_WRITE_TO_CSV
        self.csv_name = CSV_FILE_NAME
        self.video_api_url = ''
        self.api_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
            'Cookie': LOGIN_COOKIE
        }
        self.cursor = 0
        self.videos_list = []  # 视频列表id
        self.video_info_list = []
        self.video_info_dict = {}
        self.stop_flag = False  # 默认不停止

    def get_user_video_info(self, url: str):
        res = requests.get(url, headers=self.api_headers)
        res.encoding = 'utf-8'
        res_text = res.text
        return json.loads(res_text)

    def get_all_videos(self):
        """
        获取所有的视频
        :return:
        """
        while not self.stop_flag:
            self.video_api_url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?aid=6383&sec_user_id={self.sec_uid}&count=35&max_cursor={self.cursor}&cookie_enabled=true&platform=PC&downlink=10'
            xbs = generate_url_with_xbs(self.video_api_url, self.api_headers.get('User-Agent'))
            user_video_url = self.video_api_url + '&X-Bogus=' + xbs
            user_info = self.get_user_video_info(user_video_url)
            aweme_list = user_info['aweme_list']
            for aweme_info in aweme_list:
                self.video_info_list.append(aweme_info)
                self.video_info_dict.setdefault(aweme_info['aweme_id'], aweme_info)
                self.videos_list.append(aweme_info['aweme_id'])
            if int(user_info['has_more']) == 0:
                self.stop_flag = True
            else:
                self.cursor = user_info['max_cursor']
                # self.stop_flag = True
            sleep_random()
        return self.videos_list

    def download_video(self, video_url: str, file_name: str = None):
        """
        下载视频
        :param video_url: 视频地址
        :param file_name: 视频保存文件名: 默认为空
        :return:
        """
        if not self.is_save:
            logger.info("当前不需要保存")
            return
        save_folder = f"{self.save_folder}/{self.sec_uid}"
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        real_file_name = f"{save_folder}/{file_name}"
        logger.info(f"下载url:{video_url}\n保存文件名:{real_file_name}")
        if os.path.exists(real_file_name):
            os.remove(real_file_name)

        # 发送GET请求
        headers_ = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Referer': video_url,
        }
        response = requests.get(video_url, stream=True, headers=headers_)

        # 检查请求是否成功
        if response.status_code == 200:
            # 打开一个本地文件用于保存下载的视频
            with open(real_file_name, 'wb') as f:
                # 下载大文件需这样处理
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logger.info("下载完成")
        else:
            logger.info(f"错误{response.status_code}")
        # urllib.request.urlretrieve(video_url, real_file_name)

    def download_images(self, image_list: list, image_dir: str = None):
        """
        下载图片
        :param image_list: 图片地址
        :param file_name: 图片目录: 默认为空
        :return:
        """
        if not self.is_save:
            logger.info("当前不需要保存")
            return

        parent_folder = f"{self.save_folder}/{self.sec_uid}"
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)
        save_folder = f"{self.save_folder}/{self.sec_uid}/{image_dir}"

        logger.info(f"save-dir:{save_folder}")

        num = 1
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        for image_url in image_list:
            num += 1
            logger.info(f"image_url:{image_url} {num}")
            real_file_name = f"{save_folder}/{num}.jpeg"
            logger.info(f"下载url:{image_url}\n保存文件名:{real_file_name}")
            if os.path.exists(real_file_name):
                os.remove(real_file_name)
            urllib.request.urlretrieve(image_url, real_file_name)

    def get_video_detail_info(self, video_id: str):
        """
        获取视频详细信息
        :param video_id: 视频id
        :return:
        """
        default_response = {
            'video_id': video_id,  # 视频id
            'link': 'None',  # 视频链接
            'is_video': True,  # 是否为视频
            'title': 'None',  # 标题
            'thumb_up_num': 0,  # 点赞数
            'comment_num': 0,  # 评论数
            'cover_url': 'http://www.baidu.com',  # 视频封面
            'publish_time': '',  # 发布日期
            'record_time': '记录日期',  # 更新日期
            "preview_title": ""
        }
        res_info = self.video_info_dict.get(video_id, None)
        if res_info is None:
            return default_response
        default_response['title'] = res_info['desc']
        if res_info.get('preview_title') is not None:
            default_response["preview_title"] = res_info["preview_title"]
        create_time = res_info['create_time']
        local_time = time.localtime(create_time)
        local_time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        default_response['publish_time'] = local_time_str
        default_response['record_time'] = get_current_time_format()
        if res_info['images'] is None:
            default_response['link'] = res_info["video"]["play_addr"]["url_list"][0]
            default_response['cover_url'] = res_info["video"]["cover"]["url_list"][0]
            default_response['is_video'] = True
        else:
            default_response['link'] = list(map(lambda x: x["url_list"][-1], res_info["images"]))
            default_response['is_video'] = False
        default_response['thumb_up_num'] = res_info['statistics']['admire_count']
        default_response['comment_num'] = res_info['statistics']['comment_count']
        return default_response


if __name__ == '__main__':
    import sys
    logger.info("有问题请联系微信：ytouching （备注来意！！！！！！！！！！！！！！！！！！！！！）")
    params_list_size = len(sys.argv)
    if params_list_size == 2:
        USER_SEC_UID = sys.argv[1]
    elif params_list_size == 3:
        USER_SEC_UID = sys.argv[1]
        SAVE_FOLDER = sys.argv[2]

    print(f"当前传入的参数：SEC_ID：{USER_SEC_UID}\n SAVE_FOLDER:{SAVE_FOLDER}")
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)

    dy_util = DouYinUtil(sec_uid=USER_SEC_UID)
    all_video_list = dy_util.get_all_videos()
    print(f"当前需要下载的视频列表数量为:{len(all_video_list)}")
    csvVideos = []
    for video_id in all_video_list:
        video_info = dy_util.get_video_detail_info(video_id)
        if video_info['is_video'] is True:
            logger.info(f"video_link:{video_info['link']}")
            dy_util.download_video(video_info['link'], f"{video_id}.mp4")
        if video_info["is_video"] is False:
            dy_util.download_images(video_info["link"], f"{video_id}")
        title = video_info["title"]
        preview_title = video_info["preview_title"]
        logger.info(f"file:{video_id}.mp4,title:{title} , preview_title:{preview_title}")
        video_info["link"] = video_id
        video_info["video_id"] = f"id:{video_id}"
        csvVideos.append(video_info)
    try:
        data = pd.DataFrame(csvVideos)
        csvHeaders = ["视频id", "视频链接", "是否为视频", "标题", "点赞数", "评论数", "视频封面", "发布日期",
                      "更新日期",
                      "预览标题"]
        data.to_csv(CSV_FILE_NAME, header=csvHeaders, index=False, mode='a+', encoding='utf-8')
        try:
            data.to_csv(CSV_FILE_NAME, header=False, index=False, mode='a+', encoding='utf-8')
        except UnicodeEncodeError:
            logger.info("编码错误, 该数据无法写到文件中, 直接忽略该数据")
    except Exception as e:
        logger.info(e)
