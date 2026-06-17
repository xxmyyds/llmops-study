# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:37
# @FileName: api_tool_service.py
import json
from dataclasses import dataclass

from injector import inject

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidateException
from internal.model import ApiToolProvider, ApiTool
from internal.schema.api_tool_schema import CreateApiToolReq
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class ApiToolService:
    db: SQLAlchemy

    def create_api_tool(self, req: CreateApiToolReq) -> None:
        """根据传递的请求创建自定义api工具"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            account_id=account_id,
            name=req.name.data
        ).one_or_none()

        if api_tool_provider:
            raise ValidateException(f"该工具提供者名字{req.name.data}已存在")

        with self.db.auto_commit():
            api_tool_provider = ApiToolProvider(
                account_id=account_id,
                name=req.name.data,
                icon=req.icon.data,
                description=openapi_schema.description,
                openapi_schema=req.openapi_schema.data,
                headers=req.headers.data,
            )
            self.db.session.add(api_tool_provider)
            self.db.session.flush()
            for path, path_item in openapi_schema.paths.items():
                for method, method_item in path_item.items():
                    api_tool = ApiTool(
                        account_id=account_id,
                        provider_id=api_tool_provider.id,
                        name=method_item.get('operationId'),
                        description=method_item.get('description'),
                        url=f"{openapi_schema.server}{path}",
                        method=method,
                        parameters=method_item.get('parameters', []),
                    )
                    self.db.session.add(api_tool)

    @classmethod
    def parse_openapi_schema(cls, openai_schema_str: str) -> OpenAPISchema:
        """解析传递的openai_schema字符串"""
        try:
            data = json.loads(openai_schema_str.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidateException('传递数据必须符合OpenAPI规范的字符串')

        return OpenAPISchema(**data)
