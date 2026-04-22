# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/22 22:00
# @FileName: 文件对话信息历史组件.py

import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(base_url='https://api.deepseek.com')
chat_history = FileChatMessageHistory('./memory.txt')

while True:
    # 获取人类输入
    query = input('Human:')

    # 输入是否为q,如果是则直接退出
    if query == 'quit' or query == 'q':
        exit(0)

    system_prompt = (
            '你是openai大模型,请根据用户的提问回答问题\n\n' +
            f"<context>{chat_history}</context>\n\n"
    )
    # 调用openai大模型
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'content': query, 'role': 'user'}
        ],
        stream=True
    )

    print('AI: ', flush=True, end='')
    ai_content = ''
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        ai_content += content

        print(content, flush=True, end='')
    chat_history.add_user_message(query)
    chat_history.add_ai_message(ai_content)
    print('')
