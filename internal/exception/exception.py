# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 21:48
# @FileName: exception.py
from dataclasses import field
from typing import Any

from pkg.response import HttpCode


class CustomException(Exception):
    """基础异常信息"""
    code: HttpCode = HttpCode.FAIL
    message: str = ''
    data: Any = field(default_factory=dict)

    def __init__(self, message: str = '', data: Any = None):
        super().__init__()
        self.message = message
        self.data = data


class FailException(CustomException):
    pass


class NotFoundException(CustomException):
    code: HttpCode = HttpCode.NOT_FOUND


class UnauthorizedException(CustomException):
    code: HttpCode = HttpCode.UNAUTHORIZED


class ForbiddenException(CustomException):
    code: HttpCode = HttpCode.FORBIDDEN


class ValidateException(CustomException):
    code: HttpCode = HttpCode.VALIDATE_ERROR
