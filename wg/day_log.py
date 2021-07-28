#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2020/12/28 18:53
# @author  : zza
# @Email   : 740713651@qq.com
# @File    : 日报处理.py
import datetime
import re

from prompt_toolkit.clipboard import pyperclip


def service(change_file=False):
    txt_data = pyperclip.pyperclip.paste()
    print("read file pyperclip")
    txt_data = (
        txt_data.replace("✅", "- [x]")
        .replace("⬜", "- [ ]")
        .replace("\r\n", "\n")
        .replace("已完成", "已完成\n")
    )
    txt_data = (
        txt_data.replace(
            "我的一天\n\n", "\n{}:\n\n".format(datetime.date.today().isoformat())
        )
        .replace("发送自 Windows 10 版邮件应用", "")
        .strip()
    )
    txt_data = re.sub(" {2,}", "  ", txt_data) + "\n\n"
    print(txt_data)
    if change_file:
        pyperclip.pyperclip.copy(txt_data)


if __name__ == "__main__":
    service()
