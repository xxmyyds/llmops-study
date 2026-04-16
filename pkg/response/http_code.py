# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 21:16
# @FileName: http_code.py
from enum import Enum


class HttpCode(str, Enum):
    SUCCESS = "success"  # 成功
    FAIL = "fail"  # 失败
    NOT_FOUND = "not_found"  # 未找到
    UNAUTHORIZED = "unauthorized"  # 未授权
    FORBIDDEN = "forbidden"  # 无权限
    VALIDATE_ERROR = "validate_error"  # 数据验证错误
