# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:33
# @FileName: app_handler.py

import uuid
from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from internal.exception import UnauthorizedException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def create_app(self):
        app = self.app_service.create_app()
        return success_message(f"应用已经创建完毕, id: {app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_json(data={'app_name': app.name})

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_json(data={'app_name': app.name})

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已被删除, id: {app.id}")

    def completion(self):
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # 构建组件
        prompt = ChatPromptTemplate.from_template('{query}')
        llm = ChatOpenAI(model='deepseek-chat')
        parser = StrOutputParser()

        # 构建链
        chain = prompt | llm | parser

        # 调用链获得结果
        content = chain.invoke({'query': req.query.data})

        return success_json({"content": content})

    def ping(self):
        raise UnauthorizedException(message='未鉴权的请求')
