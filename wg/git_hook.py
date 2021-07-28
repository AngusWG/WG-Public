#!/usr/bin/env python
# encoding: utf-8
# Created by zza on 2021/5/31 18:44
import os


def git_hooks():
    hooks = os.path.join(os.path.expanduser("~"), r".git\hooks")
    hooks_bak = os.path.join(os.path.expanduser("~"), r".git\hooks_bak")
    if os.path.exists(hooks):
        os.rename(hooks, hooks_bak)
        print("git hooks close")
    else:
        os.rename(hooks_bak, hooks)
        print("git hooks open")


def set_config_2():

    ...


if __name__ == "__main__":
    git_hooks()
