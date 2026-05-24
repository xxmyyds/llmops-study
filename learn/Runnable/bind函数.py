# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/28 21:39
# @FileName: bind函数.py
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    print('正在检索:', query)
    return '我是Bob'


prompt = ChatPromptTemplate.from_messages([
    ('system', '你正在执行一项测试，请重复用户输入的内容，不要带其他内容'),
    ('human', '{query}')
])

llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()
chain = prompt | llm.bind(stop='谁') | parser

content = chain.invoke({'query': '你好, 我是谁'})

print(content)
