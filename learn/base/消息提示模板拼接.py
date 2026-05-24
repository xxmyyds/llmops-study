# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/15 22:17
# @FileName: 消息提示模板拼接.py
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个机器人，请回答用户提出的问题,当前时间为{now}'),
])

human_chat_prompt = ChatPromptTemplate.from_messages([
    ('human', '{query}'),
])
prompt = system_chat_prompt + human_chat_prompt
print(prompt.invoke({
    'now': datetime.now(),
    'query': 'xxxx'
}))
