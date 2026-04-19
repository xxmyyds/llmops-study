# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 21:20
# @FileName: response.py
from dataclasses import field, dataclass
from typing import Any

from flask import jsonify

from .http_code import HttpCode


@dataclass
class Response:
    """基础http响应"""
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)


def json(data: Response = None):
    response = jsonify(data)
    return response, 200


def success_json(data: Any = None):
    return json(Response(code=HttpCode.SUCCESS, message='', data=data))


def fail_json(data: Any = None):
    return json(Response(code=HttpCode.FAIL, message='', data=data))


def validate_error_json(errors: dict):
    """数据验证错误响应"""
    first_key = next(iter(errors))
    if first_key is not None:
        msg = errors.get(first_key)[0]
    else:
        msg = ''
    return json(Response(code=HttpCode.VALIDATE_ERROR, message=msg, data=errors))


def message(code: HttpCode, msg: str = ''):
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ''):
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ''):
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ''):
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ''):
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ''):
    return message(code=HttpCode.FORBIDDEN, msg=msg)
