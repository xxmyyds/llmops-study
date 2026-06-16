# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/15 22:00
# @FileName: builtin_tool_service.py
import mimetypes
import os
from dataclasses import dataclass
from typing import get_origin, get_args, Union

from flask import current_app
from injector import inject
from pydantic import BaseModel

from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.exception import NotFoundException


def _get_simple_type_name(annotation) -> str:
    """获取简单类型名称"""
    # 基本类型映射
    type_map = {
        'str': 'string',
        'int': 'integer',
        'float': 'number',
        'bool': 'boolean',
    }

    # 处理 List
    origin = get_origin(annotation)
    if origin is list:
        return 'array'

    # 处理普通类型
    if hasattr(annotation, '__name__'):
        return type_map.get(annotation.__name__, annotation.__name__)

    return str(annotation)


@inject
@dataclass
class BuiltinToolService:
    builtin_provider_manager: BuiltinProviderManager

    def get_builtin_tools(self):
        """获取所有内置工具信息"""
        providers = self.builtin_provider_manager.get_providers()
        # 遍历所有的提供商并提取工具信息
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=['icon']),
                'tools': []
            }
            # 循环遍历提取提供者的实体
            # 获取工具

            for tool_entity in provider.get_tool_entities():
                tool = provider.get_tool(tool_entity.name)
                tool_dict = {
                    **tool_entity.model_dump(),
                    'inputs': self.get_tool_inputs(tool)
                }

                builtin_tool['tools'].append(tool_dict)
            builtin_tools.append(builtin_tool)
        return builtin_tools

    def get_provider_tool(self, provider_name: str, tool_name: str):
        """根据传递的提供商名字+工具名字获取指定工具信息"""
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该提供商{provider}不存在")
        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"该工具{tool_name}不存在")

        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_name)

        builtin_tool = {
            'provider': {**provider_entity.model_dump(exclude=['icon', 'created_at'])},
            **tool_entity.model_dump(),
            'created_at': provider_entity.created_at,
            'inputs': self.get_tool_inputs(tool)
        }

        return builtin_tool

    def get_provider_icon(self, provider_name: str) -> tuple[bytes, str]:
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该提供商{provider}不存在")

        root_path = os.path.dirname(os.path.dirname(current_app.root_path))
        provider_path = os.path.join(
            root_path,
            "internal",
            "core",
            "tools",
            "builtin_tools",
            "providers",
            provider_name
        )
        icon_path = os.path.join(provider_path, "_asset", provider.provider_entity.icon)
        if not os.path.exists(icon_path):
            raise NotFoundException(f"该提供商{provider}不存在图标")
        mimetype, _ = mimetypes.guess_type(icon_path)
        mimetype = mimetype or 'application/octet-stream'
        with open(icon_path, 'rb') as f:
            byte_data = f.read()
            return byte_data, mimetype

    def get_categories(self):
        pass

    @classmethod
    def get_tool_inputs(cls, tool: str):
        inputs = []
        if hasattr(tool, 'args_schema') and issubclass(tool.args_schema, BaseModel):
            for field_name, model_field in tool.args_schema.model_fields.items():
                annotation = model_field.annotation

                # 提取类型
                if get_origin(annotation) is Union:
                    # 处理 Optional
                    args = get_args(annotation)
                    non_none = [arg for arg in args if arg is not type(None)]
                    if len(non_none) == 1:
                        type_name = _get_simple_type_name(non_none[0])
                    else:
                        type_name = 'union'
                else:
                    type_name = _get_simple_type_name(annotation)
                inputs.append({
                    'name': field_name,
                    'description': model_field.description or '',
                    'required': model_field.is_required(),
                    'type': type_name
                })
        return inputs
