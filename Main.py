#!/usr/bin/python3
# -*- coding:utf-8 -*-

import click
import Core
import dotenv
import os
import json

@click.group()
def cli():
    pass

# 手动执行-爬取
@click.command()
def update() :
    try:
        Core.Data.get()
    except Exception as identifier:
        # 非重复错误代码则记录
        if identifier.args[1] == 1002 :
            LOGGER.warning(identifier.args[0] + '-' + str(identifier.args[1]))
        else :
            LOGGER.error(identifier.args[0] + '-' + str(identifier.args[1]))
cli.add_command(update)

# 手动执行-发送
@click.command()
def send() :
    try:
        result = Core.Data.send()
        if type(result) != type(True) :
            LOGGER.warning('send_fail_ids:'+json.dumps(result))
    except Exception as identifier:
        # 非重复错误代码则记录
        LOGGER.error(identifier.args[0] + '-' + str(identifier.args[1]))
cli.add_command(send)

# 自动
@click.command()
def auto() :
    try:
        Core.Data.get()
    except Exception as identifier:
        # 非重复错误代码则记录
        if identifier.args[1] == 1002 :
            LOGGER.warning(identifier.args[0] + '-' + str(identifier.args[1]))
        else :
            LOGGER.error(identifier.args[0] + '-' + str(identifier.args[1]))
    else:
        # 发送订阅
        try:
            result = Core.Data.send()
            if type(result) != type(True) :
                LOGGER.warning('send_fail_ids:'+json.dumps(result))
        except Exception as identifier:
            # 非重复错误代码则记录
            LOGGER.error(identifier.args[0] + '-' + str(identifier.args[1]))
cli.add_command(auto)

if __name__ == "__main__":
    LOGGER = Core.Log.Logger().logger
    cli()