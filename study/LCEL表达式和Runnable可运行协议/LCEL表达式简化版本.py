# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/17 21:29
# @FileName: LCEL表达式简化版本.py

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 构建组件
prompt = ChatPromptTemplate.from_template('{query}')
llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()

# 创建链
chain = prompt | llm | parser

# 调用链
res = chain.invoke({'query': '你好，你是谁'})
print(res)
