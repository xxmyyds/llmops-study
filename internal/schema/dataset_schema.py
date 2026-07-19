# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/19 14:40
# @FileName: dataset_schema.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL, Optional


class CreateDatasetReq(FlaskForm):
    """创建知识库请求"""
    name = StringField('name', validators=[
        DataRequired('知识库名称不能为空'),
        Length(max=100, message='知识库长度不能超过100字符'),
    ])
    icon = StringField('icon', validators=[
        DataRequired('知识库图标不能为空'),
        URL(message='知识库图标必须是图片URL地址')
    ])
    description = StringField('description', default='', validators=[
        Optional(),
        Length(max=2000, message='知识库描述长度不能超过2000字符')
    ])
