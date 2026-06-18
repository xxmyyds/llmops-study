# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:37
# @FileName: api_tool_service.py
import json
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from injector import inject
from sqlalchemy import desc

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import NotFoundException
from internal.exception import ValidateException
from internal.model import ApiToolProvider, ApiTool
from internal.schema.api_tool_schema import CreateApiToolReq, GetApiToolProvidersWithPageReq, UpdateApiToolProvidersResp
from paginator import Paginator
from pkg.sqlpkg import SQLAlchemy
from .base_service import BaseService


@inject
@dataclass
class ApiToolService(BaseService):
    db: SQLAlchemy

    def update_api_tool_provider(self, provider_id: UUID, req: UpdateApiToolProvidersResp):
        """根据传递的provider_id和req更新api工具提供商信息"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise ValidateException("该工具提供者不存在")

        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        # 检测当前账号是否创建了同名的工具提供者，如果是则抛出错误
        check_api_tool_provider = self.db.session.query(ApiToolProvider).filter(
            ApiToolProvider.account_id == account_id,
            ApiToolProvider.name == req.name.data,
            ApiToolProvider.id != api_tool_provider.id,
        ).one_or_none()
        if check_api_tool_provider is not None:
            raise ValidateException(f"该工具提供者{req.name.data}已存在")

        with self.db.auto_commit():
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == api_tool_provider.id,
                ApiTool.account_id == account_id,
            ).delete()

        self.update(
            api_tool_provider,
            name=req.name.data,
            icon=req.icon.data,
            headers=req.headers.data,
            openapi_schema=openapi_schema.data,
        )

        for path, path_item in openapi_schema.paths.items():
            for method, method_item in path_item.items():
                self.create(
                    ApiTool,
                    account_id=account_id,
                    provider_id=api_tool_provider.id,
                    name=method_item.get('operationId'),
                    description=method_item.get('description'),
                    url=f"{openapi_schema.server}{path}",
                    method=method,
                    parameters=method_item.get('parameters', []),
                )

    def create_api_tool_provider(self, req: CreateApiToolReq) -> None:
        """根据传递的请求创建自定义api工具"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        openapi_schema = self.parse_openapi_schema(req.openapi_schema.data)

        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            account_id=account_id,
            name=req.name.data
        ).one_or_none()

        if api_tool_provider:
            raise ValidateException(f"该工具提供者名字{req.name.data}已存在")

        api_tool_provider = self.create(
            ApiToolProvider,
            account_id=account_id,
            name=req.name.data,
            icon=req.icon.data,
            description=openapi_schema.description,
            openapi_schema=req.openapi_schema.data,
            headers=req.headers.data,
        )

        for path, path_item in openapi_schema.paths.items():
            for method, method_item in path_item.items():
                self.create(
                    ApiTool,
                    account_id=account_id,
                    provider_id=api_tool_provider.id,
                    name=method_item.get('operationId'),
                    description=method_item.get('description'),
                    url=f"{openapi_schema.server}{path}",
                    method=method,
                    parameters=method_item.get('parameters', []),
                )

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

    def get_api_tool(self, provider_id: UUID, tool_name: str) -> ApiTool:
        """根据传递的provider_id+tool_name获取对应工具的参数详细信息"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        api_tool = self.db.session.query(ApiTool).filter_by(
            provider_id=provider_id,
            name=tool_name
        ).one_or_none()
        if api_tool is None or str(api_tool.account_id) != account_id:
            raise NotFoundException('该工具不存在')
        return api_tool

    def get_api_tool_provider(self, provider_id: UUID) -> ApiToolProvider:
        """根据传递的provider_id获取api工具提供者信息"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException('该工具提供者不存在')

        return api_tool_provider

    def delete_api_tool_provider(self, provider_id: UUID) -> None:
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        api_tool_provider = self.get(ApiToolProvider, provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException('该工具提供者不存在')

        with self.db.auto_commit():
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == provider_id,
                ApiTool.account_id == account_id
            ).delete()

            self.db.session.delete(api_tool_provider)

    def get_api_tool_providers_with_page(self, req: GetApiToolProvidersWithPageReq) -> tuple[list[Any], Paginator]:
        """获取自定义api工具服务提供者分页列表数据"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        paginator = Paginator(db=self.db, req=req)
        filters = [ApiToolProvider.account_id == account_id]
        if req.search_word.data:
            filters.append(ApiToolProvider.name.ilike(f"%{req.search_word.data}%"))
        api_tool_providers = paginator.paginate(
            self.db.session.query(ApiToolProvider).filter(*filters).order_by(desc('created_at')),
        )

        return api_tool_providers, paginator
