# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/16 22:37
# @FileName: model流式输出.py
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

ai_message = llm.stream(prompt.invoke({'query': '简单介绍下langchain这个库'}))
for message in ai_message:
    print(message.content, flush=True, end='')
