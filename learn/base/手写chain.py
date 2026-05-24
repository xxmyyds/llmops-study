# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/17 21:18
# @FileName: 手写chain.py
from typing import Any

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 构建组件
prompt = ChatPromptTemplate.from_template('{query}')
llm = ChatOpenAI(model='deepseek-chat')
parser = StrOutputParser()


class Chain:
    steps: list = []

    def __init__(self, steps):
        self.steps = steps

    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print('步骤:', step)
            print('输出:', input)
            print('==========')
        return input


chain = Chain([prompt, llm, parser])
print(chain.invoke({'query': '你好,你是谁'}))
