# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/15 14:28
# @FileName: helper.py
import importlib
from typing import Any


def dynamic_import(module_name: str, symbol_name: str) -> Any:
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)
