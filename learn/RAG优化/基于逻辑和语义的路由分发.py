# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/18 22:30
# @FileName: 基于逻辑和语义的路由分发.py
from typing import Literal

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

dotenv.load_dotenv()


class RouteQuery(BaseModel):
    """将用户的查询映射到对应的数据源上"""
    datasource: Literal['python_docs', 'js_docs', 'golang_docs'] = Field(
        description='根据用户的问题,选择哪个数据源最相关来回答用户问题'
    )


def choose_route(result: RouteQuery) -> str:
    if 'python_docs' in result.datasource:
        return 'chain in python_docs'
    elif 'js_docs' in result.datasource:
        return 'chain in js_docs'
    else:
        return 'chain in golang_docs'


llm = ChatOpenAI(model='deepseek-chat', temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)
prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个擅长将用户问题路由到适当的数据源专家，\n请根据问题涉及的编程语言，将其路由到相关数据源'),
    ('human', '{question}')
])
router = {'question': RunnablePassthrough()} | prompt | structured_llm | choose_route

question = """
为什么下面这段代码不执行了

var a=123
"""

r = router.invoke(question)
print(r)
