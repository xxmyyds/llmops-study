# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:36
# @FileName: router.py
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler

    def register_router(self, app: Flask):
        # 创建蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 将url与对应的控制器方法做绑定
        bp.add_url_rule('/ping', view_func=self.app_handler.ping)
        bp.add_url_rule('/app/completion', view_func=self.app_handler.completion, methods=['POST'])
        bp.add_url_rule('/app', view_func=self.app_handler.create_app, methods=['POST'])
        bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.get_app)
        bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.update_app, methods=['POST'])
        bp.add_url_rule('/app/<uuid:id>/delete', view_func=self.app_handler.delete_app, methods=['POST'])

        # 在应用上注册蓝图
        app.register_blueprint(bp)
