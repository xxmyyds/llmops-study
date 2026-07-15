# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/15 19:59
# @FileName: redis_extension.py
import redis
from flask import Flask
from redis.connection import Connection, SSLConnection

redis_client = redis.Redis()


def init_app(app: Flask):
    """初始化客户端"""
    connection_class = Connection
    if app.config.get('REDIS_USE_SSL', False):
        connection_class = SSLConnection

    redis_client.connection_pool = redis.ConnectionPool(**{
        'host': app.config.get('REDIS_HOST', 'localhost'),
        'port': app.config.get('REDIS_PORT', 6379),
        'db': app.config.get('REDIS_DB', 0),
        'password': app.config.get('REDIS_PASSWORD', None),
        'username': app.config.get('REDIS_USERNAME', None),
        'encoding': 'utf-8',
        'encoding_errors': 'strict',
        'decode_responses': False,
    }, connection_class=connection_class)
    app.extensions['redis'] = redis_client
