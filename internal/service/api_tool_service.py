# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:37
# @FileName: api_tool_service.py
import json

from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.exception import ValidateException


class ApiToolService:
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
