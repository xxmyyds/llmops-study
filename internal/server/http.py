# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:58
# @FileName: http.py
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.model import App
from internal.router import Router
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    def __init__(self,
                 *args,
                 conf: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs):
        # 调用父类初始化
        super().__init__(*args, **kwargs)

        # 初始化应用配置
        self.config.from_object(conf)

        # 注册绑定异常错误处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 初始化flask扩展
        db.init_app(self)
        migrate.init_app(self, db, directory='internal/migration')
        with self.app_context():
            _ = App()
            db.create_all()
        # 解决跨域问题
        CORS(self, resources={
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
                # "methods": ["POST", "GET"],
                # "allow_headers": ["Content_Type"],
            }
        })
        # 注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        # 判断是否是自定义异常
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))

        # 如果不是自定义错误
        if self.debug or os.getenv('FLASK_DEBUG') == 'development':
            raise error
        else:
            return json(Response(
                code=HttpCode.FAIL,
                message=str(error),
                data={},
            ))
