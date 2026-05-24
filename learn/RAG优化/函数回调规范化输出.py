# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/18 22:14
# @FileName: 函数回调规范化输出.py
from typing import Literal

import dotenv
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

dotenv.load_dotenv()


class RouteQuery(BaseModel):
    """将用户的查询映射到对应的数据源上"""
    datasource: Literal['python_docs', 'js_docs', 'golang_docs'] = Field(
        description='根据用户的问题,选择哪个数据源最相关来回答用户问题'
    )


llm = ChatOpenAI(model='deepseek-chat', temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

question = """
为什么下面代码不工作了：
var a=123;
"""
res: RouteQuery = structured_llm.invoke(question)
print(res)
print(res.datasource)
