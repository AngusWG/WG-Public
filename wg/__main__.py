#!/usr/bin/python3
# encoding: utf-8
# @Time    : 2020/6/24 10:05
# @author  : zza
# @Email   : 740713651@qq.com
# @File    : __main__.py

import fire

from wg.cli_helper import CliHelper


def main():
    """默认启动程序"""
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    cli_helper = CliHelper()
    fire.Fire(cli_helper)


if __name__ == "__main__":
    main()
