# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/17 17:02
# @FileName: jsonOutputParser.py
import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

dotenv.load_dotenv()


class Joke(BaseModel):
    joke: str = Field(description='回答用户的冷笑话')
    punchline: str = Field(description='这个冷笑话的笑点')


parser = JsonOutputParser(pydantic_object=Joke)

# 编排prompt
prompt = ChatPromptTemplate.from_template('请根据用户的提问进行回答: \n{format_instructions}\n{query}').partial(
    format_instructions=parser.get_format_instructions())

# 构建大语言模型
llm = ChatOpenAI(model='deepseek-chat')
joke = parser.invoke(llm.invoke(prompt.invoke({'query': '请讲一个笑话'})))
print(joke)
