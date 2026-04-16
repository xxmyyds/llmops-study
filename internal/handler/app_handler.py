# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:33
# @FileName: app_handler.py

import os
import uuid
from dataclasses import dataclass

from injector import inject
from openai import OpenAI

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

        client = OpenAI(base_url=os.getenv("OPENAI_BASE_URL"))
        com = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {'role': "system", 'content': "你是一个人民教师"},
                {"role": "user", "content": req.query.data},
            ]
        )

        content = com.choices[0].message.content

        return success_json({"content": content})

    def ping(self):
        raise UnauthorizedException(message='未鉴权的请求')
