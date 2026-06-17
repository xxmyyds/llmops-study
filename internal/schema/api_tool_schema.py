# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 14:26
# @FileName: api_tool_schema.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ValidateOpenApiSchemaReq(FlaskForm):
    openapi_schema = StringField('openai_schema', validators=[
        DataRequired(message='openapi_schema字符串不能为空')
    ])
