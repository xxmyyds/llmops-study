# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/15 22:00
# @FileName: builtin_tool_service.py
from dataclasses import dataclass
from typing import get_origin, get_args, Union

from injector import inject
from pydantic import BaseModel

from internal.core.tools.builtin_tools.providers import BuiltinProviderManager


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
            for tool_entity in provider.get_tool_entities():
                tool_dict = {
                    **tool_entity.model_dump(),
                    'inputs': []
                }
                # 获取工具
                tool = provider.get_tool(tool_entity.name)
                if hasattr(tool, 'args_schema') and issubclass(tool.args_schema, BaseModel):
                    inputs = []
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
                    tool_dict['inputs'] = inputs
                builtin_tool['tools'].append(tool_dict)
            builtin_tools.append(builtin_tool)
        return builtin_tools

    def get_provider_tools(self, provider_name: str, tool_name: str):
        """根据传递的提供商名字+工具名字获取指定工具信息"""
        pass
