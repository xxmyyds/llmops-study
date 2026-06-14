# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/14 14:54
# @FileName: 断点人在环路.py
import json
import os
from typing import Any, Type, Literal, TypedDict, Annotated

import dotenv
import requests
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class GaodeWeatherArgsSchema(BaseModel):
    city: str = Field(description='需要查询天气预报的目标城市，如广州，上海')


class GaodeWeatherTool(BaseTool):
    """根据传入的城市名查询天气"""
    name: str = 'gaode_weather'
    description: str = '当你想查询天气或与天气相关的问题时可以用的工具'
    args_schema: Type[BaseModel] = GaodeWeatherArgsSchema

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        try:
            gaode_api_key = os.getenv('GAODE_API_KEY')
            if gaode_api_key is None:
                return 'no gaode api key'
            city = kwargs.get('city')
            api_domain = 'https://restapi.amap.com/v3'

            session = requests.session()

            city_response = session.request(
                method='GET',
                url=f"{api_domain}/config/district?key={gaode_api_key}&keywords={city}&subdistrict=0",
                headers={"Content-Type": "application/json; charset=utf-8"},
            )
            city_response.raise_for_status()
            city_data = city_response.json()
            if city_data.get('info') == 'OK':
                ad_code = city_data['districts'][0]['adcode']

                weather_response = session.request(
                    method='GET',
                    url=f"{api_domain}/weather/weatherInfo?key={gaode_api_key}&city={ad_code}&extensions=all&output=json",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                if weather_data.get('info') == 'OK':
                    return json.dumps(weather_data)
            return 'get weather error'
        except Exception as e:
            return 'something error'


gaodeWeatherTool = GaodeWeatherTool()

tools = [gaodeWeatherTool]

llm = ChatOpenAI(model='gpt-4o')

llm_with_tool = llm.bind_tools(tools=tools)


# 创建状态图
class State(TypedDict):
    """图结构的状态数据"""
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    """聊天机器人节点，使用大语言模型根据传递的消息列表生成内容"""
    ai_message = llm_with_tool.invoke(state['messages'])
    return {'messages': [ai_message]}


def route(state: State) -> Literal['tools', '__end__']:
    """通过路由检测后续返回的节点是什么，工具执行或结束节点"""
    ai_message = state['messages'][-1]
    if hasattr(ai_message, 'tool_calls') and len(ai_message.tool_calls) > 0:
        return 'tools'
    return END


graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node('llm', chatbot)
graph_builder.add_node('tools', ToolNode(tools=tools))
# 添加边
graph_builder.set_entry_point('llm')
graph_builder.add_edge('llm', 'tools')
graph_builder.add_conditional_edges('llm', route)

checkpointer = MemorySaver()
config = {'configurable': {'thread_id': 1}}
# 编译图为Runnable可运行组件
graph = graph_builder.compile(checkpointer=checkpointer, interrupt_before=['tools'])

state = graph.invoke({'messages': [('human', '今天浙江宁波天气怎么样')]}, config=config)
print(state)

if hasattr(state['messages'][-1], 'tool_calls') and len(state['messages'][-1].tool_calls) > 0:
    print('现在准备调用工具：', state['messages'][-1].tool_calls)
    human_input = input('如果需要执行工具请输入yes或no：')
    if human_input.lower() == 'yes':
        print(graph.invoke(None, config=config))
    else:
        print('执行完毕')
