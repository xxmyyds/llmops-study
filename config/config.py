# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 20:59
# @FileName: config.py
import os
from typing import Any

from config.default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    print(key, os.getenv(key, DEFAULT_CONFIG.get(key)))
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str) -> bool:
    value: str = _get_env(key)
    return value.lower() == 'true' if value is not None else False


class Config:
    def __init__(self):
        # 关闭wtf的csrf保护
        self.WTF_CSRF_ENABLED = _get_bool_env('WTF_CSRF_ENABLED')

        # 数据库配置
        self.SQLALCHEMY_DATABASE_URI = _get_env('SQLALCHEMY_DATABASE_URI')
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env('SQLALCHEMY_POOL_SIZE')),
            "pool_recycle": int(_get_env('SQLALCHEMY_POOL_RECYCLE')),
        }
        self.SQLALCHEMY_ECHO = _get_bool_env('SQLALCHEMY_ECHO')

        # 配置redis
        self.REDIS_HOST = _get_env('REDIS_HOST')
        self.REDIS_PORT = _get_env('REDIS_PORT')
        self.REDIS_USERNAME = _get_env('REDIS_USERNAME')
        self.REDIS_PASSWORD = _get_env('REDIS_PASSWORD')
        self.REDIS_DB = _get_env('REDIS_DB')
        self.REDIS_USE_SSL = _get_env('REDIS_USE_SSL')

        # celery配置
        self.CELERY = {
            'broker_url': f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{int(_get_env('CELERY_BROKER_DB'))}",
            'result_backend': f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{int(_get_env('CELERY_RESULT_BACKEND_DB'))}",
            'task_ignore_result': _get_bool_env('CELERY_TASK_IGNORE_RESULT'),
            'result_expires': int(_get_env('CELERY_RESULT_EXPIRES')),
            'broker_connection_retry_on_startup': _get_bool_env('CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP'),
        }
