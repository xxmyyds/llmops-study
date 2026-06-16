# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/15 14:28
# @FileName: helper.py
import importlib
from typing import Any


def dynamic_import(module_name: str, symbol_name: str) -> Any:
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)


def add_attribute(attr_name: str, attr_value: Any):
    """为特定函数添加属性"""

    def decorator(func: Any):
        setattr(func, attr_name, attr_value)
        return func

    return decorator
