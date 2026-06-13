# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/13 10:23
# @FileName: 条件边与循环流程控制.py
import json
import os
from typing import TypedDict, Annotated, Type, Any, Literal

import dotenv
import requests
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

dotenv.load_dotenv()

llm = ChatOpenAI(model='gpt-4o')


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

llm_with_tool = llm.bind_tools(tools=tools)


# 创建状态图
class State(TypedDict):
    """图结构的状态数据"""
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    """聊天机器人节点，使用大语言模型根据传递的消息列表生成内容"""
    ai_message = llm_with_tool.invoke(state['messages'])
    return {'messages': [ai_message]}


def tool_executor(state: State) -> Any:
    """工具执行节点"""
    tool_calls = state['messages'][-1].tool_calls
    tools_by_name = {tool.name: tool for tool in tools}

    messages = []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call['name']]
        messages.append(ToolMessage(
            tool_call_id=tool_call['id'],
            name=tool_call['name'],
            content=tool.invoke(tool_call['args'])
        ))
    return {'messages': messages}


def route(state: State) -> Literal['tool_executor', '__end__']:
    """通过路由检测后续返回的节点是什么，工具执行或结束节点"""
    ai_message = state['messages'][-1]
    if hasattr(ai_message, 'tool_calls') and len(ai_message.tool_calls) > 0:
        return 'tool_executor'
    return END


graph_builder = StateGraph(State)

# 添加节点
graph_builder.add_node('llm', chatbot)
graph_builder.add_node('tool_executor', tool_executor)
# 添加边
graph_builder.set_entry_point('llm')
graph_builder.add_conditional_edges('llm', route)
graph_builder.add_edge('tool_executor', 'llm')

# graph_builder.add_edge(START, 'llm')
# graph_builder.add_edge('llm', END)

# 编译图为Runnable可运行组件
graph = graph_builder.compile()

state = graph.invoke({'messages': [('human', '今天浙江宁波天气怎么样')]})

for message in state['messages']:
    print('消息类型：', message.type)
    if hasattr(message, 'tool_calls') and len(message.tool_calls) > 0:
        print('工具调用参数:', message.tool_calls)
    print('消息内容：', message.content)
    print('=============================')
