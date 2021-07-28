#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2019/12/19 9:36
# @author  : zza
# @Email   : 740713651@qq.com
# @File    : 将网易云的私信音乐整理.py
"""
该脚本会保存每天新私信里最后几首歌曲到tmp_save_dir
1.在Chrome上登录自己的网易云帐号t
2.创建tmp_save_dir
然后运行脚本
"""
import os

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from tqdm import tqdm

song_dir = "tmp_save_dir"
# 屏蔽关键词
shielding_words = ["伴奏"]

_path = os.path.abspath(__file__)
_dir_name = os.path.dirname(_path)  # 单个文件 下载驱动


def init_driver():
    executable_name = "chromedriver.exe"

    _file_path = _path.replace(os.path.basename(__file__), executable_name)
    if not os.path.exists(_file_path):  # 无驱则需要下载
        # 本地项目 复制驱动

        url = "https://raw.githubusercontent.com/AngusWG/crawler_set/tree/master/driver/chromedriver.exe"
        proxies = {
            "http": "socks5://127.0.0.1:9999",
            "https": "socks5://127.0.0.1:9999",
        }
        r = requests.get(url, proxies=proxies)

        with open(_file_path, "wb") as code:
            content_size = int(r.headers["content-length"])  # 内容体总大小
            for data in tqdm(
                iterable=r.iter_content(1024), total=content_size, unit="k", desc="下载驱动"
            ):
                code.write(data)
    # auto add "default"
    user_cookies = os.path.join(
        os.path.expanduser("~"), r"AppData\Local\Google\Chrome\User Data"
    )
    option = webdriver.ChromeOptions()
    option.add_argument("--user-data-dir={}".format(user_cookies))  # 设置成用户自己的数据目录

    try:
        driver = webdriver.Chrome(_file_path, options=option)
        driver.implicitly_wait(5)
        return driver
    except WebDriverException as err:
        print("请先关掉所有的Chrome")
        print(err)
        exit(-2)


def get_private_detail(index=1):
    # 点击私信后
    driver.get("https://music.163.com/#/msg/m/private?index={}".format(index))
    driver.switch_to.frame("contentFrame")
    new_msg_items = driver.find_elements_by_xpath(
        '//i[@class="u-bub"]/b[@class="f-alpha"]/..//parent::*//a'
    )
    private_detail_url_dict = dict()
    for i in new_msg_items:
        _, singer_id = i.get_attribute("href").split("?")
        uri = "https://music.163.com/#/msg/m/private_detail?" + singer_id
        msg_num = int(i.find_element_by_xpath("../i/em").text)
        private_detail_url_dict[uri] = msg_num
    if private_detail_url_dict:
        private_detail_url_dict.update(get_private_detail(index + 1))

    return private_detail_url_dict


def get_song_url_from_album_set(url):
    song_set = set()
    # 歌曲页面保存
    driver.get(url)
    driver.switch_to.frame("contentFrame")
    url_list = driver.find_elements_by_xpath('//a[contains(@href, "/song?id")]')
    for item in url_list:
        if "伴奏" in item.text:
            break
        _, song_id = item.get_attribute("href").split("?id=")
        song_set.add("https://music.163.com/#/song?id=" + song_id)
        song_name = item.find_element_by_xpath("./b").get_attribute("title")
        print(song_name, end=" ")
    return song_set


def get_song_url_from_private_detail(url, msg_num):
    album_set = set()
    song_set = set()
    # 歌曲页面保存
    driver.get(url)
    driver.switch_to.frame("contentFrame")
    url_list = driver.find_elements_by_xpath('//div[contains(@class,"itemleft")]')[
        -msg_num:
    ]
    for item in url_list:
        try:
            i = item.find_element_by_xpath(
                './/a[contains(@href,"album?id") or contains(@href, "song?id")]'
            ).get_attribute("href")
            _, _id = i.split("?id=")
            if "song?id" in i:
                song_set.add("https://music.163.com/#/song?id=" + _id)
            else:  # "album?id"
                album_set.add("https://music.163.com/#/album?id=" + _id)
        except NoSuchElementException:
            pass

    for album_url in album_set:
        song_set.update(get_song_url_from_album_set(album_url))
    return song_set


def save_song(url):
    print("[{}] start".format(url), end=" ")
    driver.get(url)
    driver.switch_to.frame("contentFrame")
    title = driver.find_element_by_xpath('//div[contains(@class, "tit")]').text.strip()
    for word in shielding_words:
        if word in title:
            print("{} 因 {} 已忽略".format(title, word))
            return
    driver.find_element_by_xpath('//*[contains(text(), "收藏")]').click()

    item = driver.find_elements_by_xpath('//*[contains(text(), "{}")]'.format(song_dir))
    if item:
        item[0].click()
        print(title)
    else:
        print(title, "收藏失败", url)


driver = init_driver()


def server():
    tmp_save_data = os.path.join(_dir_name, "tmp.txt")
    if not os.path.exists(tmp_save_data):
        # 获取私信用户列表
        private_detail_url_dict = get_private_detail()
        print("private_detail_url_set len={}".format(len(private_detail_url_dict)))
        # 获取歌曲id
        song_url_set = set()
        for private_detail_url, msg_num in private_detail_url_dict.items():
            song_url_set.update(
                get_song_url_from_private_detail(private_detail_url, msg_num)
            )
            print("song_url_set len={}".format(len(song_url_set)))
        with open(tmp_save_data, "w", encoding="utf8") as f:
            f.write("\n".join(song_url_set))
    else:
        with open(tmp_save_data, "r", encoding="utf8") as f:
            data = f.read()
        song_url_set = data.split("\n") if data else []
    # 保存歌曲
    for song_url in song_url_set:
        save_song(song_url)
    os.remove(tmp_save_data)
    driver.close()


if __name__ == "__main__":
    server()
