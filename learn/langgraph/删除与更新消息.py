# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/13 17:01
# @FileName: 删除与更新消息.py

import dotenv
from langchain_core.messages import RemoveMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import MessagesState

dotenv.load_dotenv()

llm = ChatOpenAI(model='gpt-4o')


def chatbot(state: MessagesState):
    """聊天机器人节点，使用大语言模型根据传递的消息列表生成内容"""
    ai_message = llm.invoke(state['messages'])
    return {'messages': [ai_message]}


def delete_human_message(state: MessagesState):
    """删除人类消息"""
    human_message = state['messages'][0]
    return {'messages': [RemoveMessage(id=human_message.id)]}


def update_ai_message(state: MessagesState):
    """更新ai_messages"""
    ai_message = state['messages'][-1]
    return {'messages': [AIMessage(id=ai_message.id, content="更新后的ai message：" + ai_message.content)]}


graph_builder = StateGraph(MessagesState)

# 添加节点
graph_builder.add_node('chatbot', chatbot)
graph_builder.add_node('delete_human_message', delete_human_message)
graph_builder.add_node('update_ai_message', update_ai_message)
# 添加边
graph_builder.set_entry_point('chatbot')
graph_builder.add_edge('chatbot', 'delete_human_message')
graph_builder.add_edge('delete_human_message', 'update_ai_message')
graph_builder.set_finish_point('update_ai_message')

# 编译图为Runnable可运行组件
graph = graph_builder.compile()

# 调用
res = graph.invoke(
    {
        "messages": [
            ('human', '你好你是什么大模型')
        ],
        "use_name": "user"
    }
)
print(res)
