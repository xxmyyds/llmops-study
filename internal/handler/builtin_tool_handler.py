# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/15 21:53
# @FileName: builtin_tool_handler.py
import io
from dataclasses import dataclass

from flask import send_file
from injector import inject

from internal.service import BuiltinToolService
from pkg.response import success_json


@inject
@dataclass
class BuiltinToolHandler:
    """内置工具处理器"""
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self):
        """获取所有内置工具信息"""
        builtin_tools = self.builtin_tool_service.get_builtin_tools()
        return success_json(builtin_tools)

    def get_provider_tools(self, provider_name: str, tool_name: str):
        """根据传递的提供商名字+工具名字获取指定工具信息"""
        builtin_tools = self.builtin_tool_service.get_provider_tool(provider_name, tool_name)
        return success_json(builtin_tools)

    def get_provider_icon(self, provider_name: str):
        """根据传递的提供商获取 icon图标信息"""
        icon, mimetype = self.builtin_tool_service.get_provider_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype=mimetype)

    def get_categories(self):
        """获取所有内置提供商的分类"""
        pass
