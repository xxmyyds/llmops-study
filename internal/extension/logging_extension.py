# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/14 20:23
# @FileName: logging_extension.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from flask import Flask


def init_app(app: Flask):
    """日志记录器初始化"""
    # 设置日志存储的文件夹
    project_root = Path(__file__).parent.parent.parent
    print(project_root)
    log_folder = os.path.join(project_root, 'storage', 'log')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    # 定义日志的文件名
    log_file = os.path.join(log_folder, 'app.log')
    # 设置日志的格式，并且让日志每天更新一次
    handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8',
    )
    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s]: %(message)s"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    # 在开发环境下，将日志同时输出到控制台
    if app.debug or os.getenv("FLASK_ENV") == "development":
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
