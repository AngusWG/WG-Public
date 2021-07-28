#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2019/6/29 22:11
# @author  : zza
# @Email   : 740713651@qq.com
# @Form https://github.com/MrJStyle/Python-Crawler

import os
import re
import tkinter
import traceback

import requests
from lxml import etree

home_url = "http://wallpaperswide.com"
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
}
# 需要填写的参数！！！
start_page = 15  # 起始页码 如果错误了  根据日志  填写start_page避免重复爬取
end_page = 50  # 结束页码

proxies = {
    "http": "http://127.0.0.1:9999",
    "https": "http://127.0.0.1:9999",
}


class GlobalObj:
    pass


global_obj = GlobalObj()
global_obj.count = 0
max_download_num = 100


def downloads(
    res="/blue_ocean_aesthetic_background-wallpapers.html",
    definition="2560x1440",
    save_dir=None,
):
    print("start :{}".format(res))
    try:
        req1 = requests.get(
            "{}{}".format(home_url, res), headers=header, proxies=proxies
        )
        photo_url = etree.HTML(req1.text).xpath(
            '//div/a[contains(text(),"{}")]/@href'.format(definition)
        )[0]
        rep = requests.get(
            home_url + photo_url, stream=True, headers=header, proxies=proxies
        )
        file_name = re.findall("filename=(.+)", rep.headers["content-disposition"])[0]
        file_path = os.path.join(save_dir, file_name)
    except IndexError as err:
        print(traceback.format_exc())
        print("err   :{}\n{}\n".format(res, err))
        return
    if os.path.exists(file_path) and int(
        rep.headers["Content-Length"]
    ) == os.path.getsize(file_path):
        print("[{}]文件 {} 重复，".format(global_obj.count, file_path))
        # sys.exit(0)
        return
    with open(file_path, "wb") as file:
        for chunk in rep.iter_content(chunk_size=1024 * 10):
            if chunk:
                file.write(chunk)
    global_obj.count += 1
    print("[{}]end   :{}".format(global_obj.count, res))


def service(save_dir=None):
    if save_dir is None:
        save_dir = os.path.join(os.path.expanduser("~"), "Pictures", "wallpaper")
        os.makedirs(save_dir, exist_ok=True)
    root = tkinter.Tk()
    definition = "{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight())
    for page in range(start_page, end_page):
        print("\n{}\npage = {}".format("*" * 20, page))
        req1 = requests.get(
            "{}/city-desktop-wallpapers/page/{}".format(home_url, page),
            headers=header,
            proxies=proxies,
        )
        res_list = etree.HTML(req1.text).xpath('//div[@class="thumb"]/div[1]/a/@href')
        [downloads(res, definition=definition, save_dir=save_dir) for res in res_list]

        if global_obj.count >= max_download_num:
            break


if __name__ == "__main__":
    service()
