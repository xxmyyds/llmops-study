# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/11 20:52
# @FileName: app_schema.py
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天接口请求验证"""
    query = StringField('query', validators=[
        DataRequired(message='用户的提问是必须填的'),
        Length(max=2000, message='用户的提问最大长度是2000')
    ])
