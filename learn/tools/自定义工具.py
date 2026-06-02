# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/1 21:24
# @FileName: 自定义工具.py
from typing import Type

from langchain_core.tools import StructuredTool, BaseTool
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MultiplyInput(BaseModel):
    x: int = Field(description='第一个数')
    y: int = Field(description='第二个数')


@tool('multiply function', return_direct=True, args_schema=MultiplyInput)
def multiply(x: int, y: int) -> int:
    """实现乘法"""
    return x * y


print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.invoke({'x': 2, 'y': 3}))


def multiply1(x: int, y: int) -> int:
    """实现乘法"""
    return x * y


async def amultiply1(x: int, y: int) -> int:
    """实现乘法"""
    return x * y


calculator = StructuredTool.from_function(
    func=multiply1,
    coroutine=amultiply1,
    name='multiply',
    description='simple multiply function',
    args_schema=MultiplyInput,
    return_direct=True,
)

print(calculator.name)
print(calculator.description)
print(calculator.args)
print(calculator.return_direct)
print(calculator.invoke({'x': 2, 'y': 3}))


class MultiplyTool(BaseTool):
    """simple multiply tool"""

    name: str = 'multiply1'
    description: str = '1simple multiply function'
    args_schema: Type[BaseModel] = MultiplyInput

    def _run(self, x: int, y: int) -> int:
        return x * y


calculator1 = MultiplyTool()
print(calculator1.name)
print(calculator1.description)
print(calculator1.args)
print(calculator1.return_direct)
print(calculator1.invoke({'x': 22, 'y': 3}))
