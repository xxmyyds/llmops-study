# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/17 16:54
# @FileName: strOutputParser.py
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 编排prompt
prompt = ChatPromptTemplate.from_template('{query}')

# 创建大语言模型
llm = ChatOpenAI(model='deepseek-chat')

# 解析
parser = StrOutputParser()
content = parser.invoke(llm.invoke(prompt.invoke({'query': '你好,你是谁?'})))
print(content)
