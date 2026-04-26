# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:33
# @FileName: app_handler.py

import uuid
from dataclasses import dataclass
from operator import itemgetter
from uuid import UUID

from injector import inject
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
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

    def debug(self, app_id: UUID):
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        prompt = ChatPromptTemplate.from_messages([
            ('system', '你是一个强大的聊天机器人, 请根据用户的问题回答'),
            MessagesPlaceholder('history'),
            ('human', '{query}'),
        ])
        memory = ConversationBufferWindowMemory(
            k=3,
            input_key='query',
            output_key='output',
            return_messages=True,
            chat_memory=FileChatMessageHistory('./storage/memory/chat_history.txt')
        )

        llm = ChatOpenAI(model='deepseek-chat')

        chain = RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter('history'),
        ) | prompt | llm | StrOutputParser()
        # 调用链获得结果
        chain_input = {'query': req.query.data}
        content = chain.invoke(chain_input)
        memory.save_context(chain_input, {'output': content})

        return success_json({"content": content})

    def ping(self):
        raise UnauthorizedException(message='未鉴权的请求')
