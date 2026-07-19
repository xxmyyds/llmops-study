# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:36
# @FileName: router.py
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler, BuiltinToolHandler, ApiToolHandler, UploadFileHandler
from internal.handler.dataset_handler import DatasetHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler
    build_tool_handler: BuiltinToolHandler
    api_tool_handler: ApiToolHandler
    upload_file_handler: UploadFileHandler
    dataset_handler: DatasetHandler

    def register_router(self, app: Flask):
        # 创建蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 将url与对应的控制器方法做绑定
        bp.add_url_rule('/ping', view_func=self.app_handler.ping)
        bp.add_url_rule('/apps/<uuid:app_id>/debug', view_func=self.app_handler.debug, methods=['POST'])
        bp.add_url_rule('/app', view_func=self.app_handler.create_app, methods=['POST'])
        bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.get_app)
        bp.add_url_rule('/app/<uuid:id>', view_func=self.app_handler.update_app, methods=['POST'])
        bp.add_url_rule('/app/<uuid:id>/delete', view_func=self.app_handler.delete_app, methods=['POST'])

        # 内置插件模块
        bp.add_url_rule('/builtin-tools', view_func=self.build_tool_handler.get_builtin_tools)
        bp.add_url_rule('/builtin-tools/<string:provider_name>/tools/<string:tool_name>',
                        view_func=self.build_tool_handler.get_provider_tools)
        bp.add_url_rule('/builtin-tools/<string:provider_name>/icon',
                        view_func=self.build_tool_handler.get_provider_icon)
        bp.add_url_rule('/builtin-tools/categories', view_func=self.build_tool_handler.get_categories)

        # 自定义插件模块
        bp.add_url_rule('/api-tools/validate-openapi-schema', view_func=self.api_tool_handler.validate_openapi_schema,
                        methods=['POST'])

        bp.add_url_rule('/api-tools', view_func=self.api_tool_handler.get_api_tool_providers_with_page)
        bp.add_url_rule('/api-tools', view_func=self.api_tool_handler.create_api_tool_provider, methods=['POST'])
        bp.add_url_rule('/api-tools/<uuid:provider_id>', methods=['POST'],
                        view_func=self.api_tool_handler.update_api_tool_provider)

        bp.add_url_rule('/api-tools/<uuid:provider_id>', view_func=self.api_tool_handler.get_api_tool_provider)
        bp.add_url_rule('/api-tools/<uuid:provider_id>/tools/<string:tool_name>',
                        view_func=self.api_tool_handler.get_api_tool)

        bp.add_url_rule('/api-tools/<uuid:provider_id>/delete', methods=['POST'],
                        view_func=self.api_tool_handler.delete_api_tool_provider)

        bp.add_url_rule('/upload-files/file', methods=['POST'], view_func=self.upload_file_handler.upload_file)
        bp.add_url_rule('/upload-files/image', methods=['POST'], view_func=self.upload_file_handler.upload_image)

        # 知识库模块
        bp.add_url_rule('/datasets', view_func=self.dataset_handler.get_datasets_with_page)
        bp.add_url_rule('/datasets', methods=['POST'], view_func=self.dataset_handler.create_dataset)
        bp.add_url_rule('/datasets/<uuid:dataset_id>', view_func=self.dataset_handler.get_dataset)
        bp.add_url_rule('/datasets/<uuid:dataset_id>', methods=['POST'], view_func=self.dataset_handler.update_dataset)

        # 在应用上注册蓝图
        app.register_blueprint(bp)
