# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/18 11:14
# @FileName: RunnableParallel_usage.py

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

joke_prompt = ChatPromptTemplate.from_template('请讲一个关于{subject}的笑话,尽可能短一点')
poem_prompt = ChatPromptTemplate.from_template('请写一篇关于{subject}的诗,尽可能短一点')
llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()

joke_chain = joke_prompt | llm | parser
poem_chain = poem_prompt | llm | parser

# 创建并行链
# map_chain = RunnableParallel({
#     'joke': joke_chain,
#     'poem': poem_chain
# })
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

res = map_chain.invoke({'subject': '程序员'})
print(res)
