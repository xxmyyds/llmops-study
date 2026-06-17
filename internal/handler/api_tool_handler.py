# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:21
# @FileName: api_tool_handler.py
from dataclasses import dataclass
from uuid import UUID

from injector import inject

from internal.schema.api_tool_schema import GetApiToolProviderResp, GetApiToolResp
from internal.schema.api_tool_schema import ValidateOpenApiSchemaReq, CreateApiToolReq
from internal.service import ApiToolService
from pkg.response import validate_error_json, success_json, success_message


@inject
@dataclass
class ApiToolHandler:
    """自定义APi插件处理器"""
    api_tool_service: ApiToolService

    def create_api_tool(self):
        """创建自定义api工具"""
        req = CreateApiToolReq()
        if not req.validate():
            return validate_error_json(req.errors)
        self.api_tool_service.create_api_tool(req)

        return success_message('创建自定义API插件成功')

    def get_api_tool(self, provider_id: UUID, tool_name: str):
        api_tool = self.api_tool_service.get_api_tool(provider_id, tool_name)
        resp = GetApiToolResp()
        return success_json(resp.dump(api_tool))

    def get_api_tool_provider(self, provider_id: UUID):
        """根据传递的provider_id获取工具提供者的原始信息"""
        api_tool_provider = self.api_tool_service.get_api_tool_provider(provider_id)
        resp = GetApiToolProviderResp()
        return success_json(resp.dump(api_tool_provider))

    def validate_openapi_schema(self):
        """校验传递的openapi schema是否正确"""
        req = ValidateOpenApiSchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)
        self.api_tool_service.parse_openapi_schema(req.openapi_schema.data)
        return success_json('数据校验成功')
