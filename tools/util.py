import random
import execjs
import time
import urllib.parse
import datetime


def sleep_random(sleep_time: int = None):
    """
    睡眠时间
    :param sleep_time:
    :return:
    """
    if sleep_time is None:
        time.sleep(random.randint(1, 5))
    else:
        time.sleep(sleep_time)


def get_current_time_format(format_info: str = None):
    """
    获取当前的时间的格式化 [ex: 2023-02-25 11:22:11]
    :param format_info:
    :return:
    """
    if format_info is None:
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.now().strftime(format_info)


def generate_url_with_xbs(url, user_agent):
    """
    生成x_bogus
    :param url:
    :param user_agent:
    :return:
    """
    query = urllib.parse.urlparse(url).query
    x_bogus = execjs.compile(open('tools/X-Bogus.js').read()).call('sign', query, user_agent)
    return x_bogus
