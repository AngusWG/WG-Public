#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2020/6/24 10:04
# @author  : zza
# @Email   : 740713651@qq.com
# @File    : cli_helper.py
import os


class CliHelper(object):
    @staticmethod
    def rm_file(path="."):
        """
        remove_pyd_c_file
        删除当前或指定目录的pyd文件和c文件
        """
        ignore_list = ["setup"]
        for root, dirs, files in os.walk(path):
            for file in files:
                if "." in file and not file.endswith("py") and not file.endswith("pyi"):
                    name = file[: file.index(".")]
                    if name in ignore_list:
                        continue
                    if name + ".py" in files:
                        path = os.path.join(".", root, file)
                        print("remove : {}".format(path))
                        os.remove(path)
        return True

    @staticmethod
    def 网易():
        """
        网易云音乐 自动收藏
        """
        from wg.将网易云的私信音乐整理 import server

        server()

    @staticmethod
    def 壁纸():
        """爬取壁纸"""
        from wg.壁纸爬虫 import service

        service()

    @staticmethod
    def day_log(change_file=True):
        """将剪贴板日志转换成markdown格式"""
        from wg.day_log import service

        service(change_file)

    @staticmethod
    def set_git_hook():
        """设置 git pre-commit"""
        from wg.git_set_hook import service

        service()

    @staticmethod
    def git_hooks():
        """开/关 git hooks"""
        from wg.git_hook import git_hooks

        git_hooks()

    @staticmethod
    def path():
        """wsl windows 路径转换"""
        from wg.path import convert_path

        convert_path()

    @staticmethod
    def date():
        """显示倒计时"""
        from wg.work_hours import main

        main()
