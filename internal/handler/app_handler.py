# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 16:33
# @FileName: app_handler.py

import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, Any
from uuid import UUID

from injector import inject
from langchain_classic.base_memory import BaseMemory
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI

from internal.core.tools.builtin_tools.providers import ProviderFactory
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from internal.service import VectorDatabaseService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    app_service: AppService
    vector_database_service: VectorDatabaseService
    provider_factory: ProviderFactory

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

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """加载记忆变量信息"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {'history': []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存储对应的上下文信息到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID):
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        prompt = ChatPromptTemplate.from_messages([
            ('system',
             '你是一个强大的聊天机器人, 请根据对应的上下文和历史对话回复用户的问题. \n\n<context>{context}</context>'),
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

        retriever = self.vector_database_service.get_retriever() | self.vector_database_service.combine_documents

        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter('history'),
            context=itemgetter('query') | retriever
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)
        # 调用链获得结果
        chain_input = {'query': req.query.data}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})

        return success_json({"content": content})

    @classmethod
    def _combine_documents(cls, documents: list[Document]) -> str:
        """将传入的文档列表合并成字符串"""
        return "\n\n".join([document.page_content for document in documents])

    def ping(self):
        google_serper = self.provider_factory.get_tool('google', 'google_serper')()
        print(google_serper)
        print(google_serper.invoke('什么是 llmops'))
        return success_json()
