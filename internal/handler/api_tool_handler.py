# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:21
# @FileName: api_tool_handler.py
from dataclasses import dataclass

from injector import inject

from internal.schema.api_tool_schema import ValidateOpenApiSchemaReq
from internal.service import ApiToolService
from pkg.response import validate_error_json, success_json


@inject
@dataclass
class ApiToolHandler:
    """自定义APi插件处理器"""
    api_tool_service: ApiToolService

    def validate_openapi_schema(self):
        """校验传递的openapi schema是否正确"""
        req = ValidateOpenApiSchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)
        self.api_tool_service.parse_openapi_schema(req.openapi_schema.data)
        return success_json('数据校验成功')
