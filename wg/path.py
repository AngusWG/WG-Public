#!/usr/bin/env python
# encoding: utf-8
# Created by zza on 2021/6/9 14:23
import re

from prompt_toolkit.clipboard import pyperclip


def convert_path_by_str():
    ...


def convert_path():
    path = pyperclip.pyperclip.paste()  # r'/mnt/d/Programs/ActivityWatch'
    wsl_result = re.match(r"(^[A-Z]:)\\(.*)", path)
    if wsl_result:
        _disk_symbol = wsl_result[1][:-1].lower()
        wsl_path = f"\\mnt\\{_disk_symbol}\\{wsl_result[2]}".replace("\\", "/")
        pyperclip.pyperclip.copy(wsl_path)
        print(wsl_path)
        return wsl_path
    elif re.match(r"^/mnt/([a-z])/(.*)", path):
        win_result = re.match(r"^/mnt/([a-z])/(.*)", path)
        tail = win_result[2].replace("/", "\\")
        win_path = f"{win_result[1].upper()}:\\{tail}"
        pyperclip.pyperclip.copy(win_path)
        print(win_path)
        return win_path
    else:
        print(f"nothing to do with {path}")
        return


def main():
    pyperclip.pyperclip.copy("D:\\Programs\\ActivityWatch")
    convert_path()
    print(pyperclip.pyperclip.paste())


if __name__ == "__main__":
    main()
