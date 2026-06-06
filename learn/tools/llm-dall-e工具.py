# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/6 19:50
# @FileName: llm-dall-e工具.py

import dotenv
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 提示dall-e-3不存在
dalle = OpenAIDALLEImageGenerationTool(
    api_wrapper=DallEAPIWrapper(model='dall-e-3'),
)

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([dalle], tool_choice='openai_dalle')

chain = llm_with_tools | (lambda msg: msg.tool_calls[0]['args']) | dalle

print(chain.invoke('帮我绘制一张美女照片'))
