# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/18 22:20
# @FileName: callback使用技巧.py
import time
from typing import Any
from uuid import UUID

import dotenv
from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    # 自定义llm回调处理器
    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            metadata: dict[str, Any] | None = None,
            **kwargs: Any,
    ) -> Any:
        print('聊天模型开始执行')
        print(serialized)
        print(messages)
        self.start_at = time.time()

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: GenerationChunk | ChatGenerationChunk | None = None,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            **kwargs: Any,
    ) -> Any:
        print('token生成了')
        print(token)

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print(response)
        print('程序消耗:', end_at - self.start_at)


prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()
chain = {'query': RunnablePassthrough()} | prompt | llm | parser

content = chain.invoke('你好, 你是谁', config={'callbacks': [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})
print(content)

# res = chain.stream('你好, 你是谁', config={'callbacks': [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})
# for r in res:
#     pass
