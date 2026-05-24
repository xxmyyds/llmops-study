# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/16 22:33
# @FileName: model批处理.py
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 编排prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', '你是一个机器人，请回答用户提出的问题,当前时间为{now}'),
        ('human', '{query}')
    ]
).partial(now=datetime.now())

# 创建大语言模型
llm = ChatOpenAI(model='deepseek-chat')

ai_messages = llm.batch([
    prompt.invoke({'query': '今天是礼拜几'}),
    prompt.invoke({'query': '现在是几点'})
])
for message in ai_messages:
    print(message.content)
    print('================')
