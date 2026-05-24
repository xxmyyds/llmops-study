# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/26 21:26
# @FileName: RunnableWithMessageHistory.py

import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(f'./chat_history_{session_id}.txt')
    return store[session_id]


prompt = ChatPromptTemplate.from_messages([
    ('system', '你是一个智能的聊天机器人,需要根据用户的问题和上下文来回答问题'),
    MessagesPlaceholder('history'),
    ('human', '{query}'),
])

llm = ChatOpenAI(model='deepseek-v4-flash')

chain = prompt | llm | StrOutputParser()

with_message_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='query',
    history_messages_key='history',
)

while True:
    query = input("Human: ")

    if query == 'quit' or query == 'q':
        exit(0)

    chain_input = {'query': query}

    print('AI: ')
    response = with_message_chain.stream(
        chain_input,
        config={'configurable': {'session_id': 'xxm'}}
    )
    output = ''
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end='')
    print("")
