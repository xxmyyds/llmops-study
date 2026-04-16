# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/15 21:45
# @FileName: prompt.py
from datetime import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

# prompt = PromptTemplate.from_template('请讲一个关于{subject}的笑话')
# print(prompt.format(subject='程序员'))
# prompt_value = prompt.invoke({'subject': '喜剧演员'})
# print(prompt_value.to_string())
# print(prompt_value.to_messages())

# chat_prompt = ChatPromptTemplate.from_template('请讲一个关于{subject}的笑话')
# print(chat_prompt.format(subject='程序员'))
# chat_prompt_value = chat_prompt.invoke({'subject': '喜剧演员'})
# print(chat_prompt_value.to_string())
# print(chat_prompt_value.to_messages())

chat_prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个机器人，请回答用户提出的问题,当前时间为{now}'),
    # 消息占位
    MessagesPlaceholder('chat_history'),
    HumanMessagePromptTemplate.from_template('请讲一个关于{subject}的笑话')
]).partial(now=datetime.now())
chat_prompt_value = chat_prompt.invoke({
    'chat_history': [
        ('human', '我叫xxm'),
        AIMessage('你好，我是deepseek，哈哈哈哈')
    ],
    'subject': '程序员'
})
print(chat_prompt_value)
print(chat_prompt_value.to_string())
