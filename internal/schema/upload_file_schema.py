# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/21 21:42
# @FileName: upload_file_schema.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from marshmallow import Schema, fields, pre_dump

from internal.entity.upload_file_entity import ALLOWED_DOCUMENT_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS
from internal.model import UploadFile


class UploadFileReq(FlaskForm):
    """上传文件请求"""
    file = FileField('file', validators=[
        FileRequired('上传文件不能为空'),
        FileSize(max_size=15 * 1024 * 1024, message='上传文件最大不能超过15MB'),
        FileAllowed(ALLOWED_DOCUMENT_EXTENSIONS, message=f"仅上传{'/'.join(ALLOWED_DOCUMENT_EXTENSIONS)}文件")
    ])


class UploadFileResp(Schema):
    """上传文件响应接口"""
    id = fields.UUID()
    account_id = fields.UUID()
    name = fields.String()
    key = fields.String()
    size = fields.Integer()
    extension = fields.String()
    mime_type = fields.String()
    created_at = fields.Integer()

    @pre_dump
    def process_data(self, data: UploadFile, **kwargs):
        return {
            'id': data.id,
            'account_id': data.account_id,
            'name': data.name,
            'key': data.key,
            'size': data.size,
            'extension': data.extension,
            'mime_type': data.mime_type,
            'created_at': int(data.created_at.timestamp()),
        }


class UploadImageReq(FlaskForm):
    """上传图片请求体"""
    file = FileField('file', validators=[
        FileRequired('上传图片不能为空'),
        FileSize(max_size=15 * 1024 * 1024, message='上传图片最大不能超过15MB'),
        FileAllowed(ALLOWED_IMAGE_EXTENSIONS, message=f"仅上传{'/'.join(ALLOWED_IMAGE_EXTENSIONS)}文件")
    ])
