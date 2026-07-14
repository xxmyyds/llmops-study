# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/13 20:21
# @FileName: upload_file_service.py
from dataclasses import dataclass

from injector import inject

from internal.model import UploadFile
from internal.service import BaseService
from pkg.sqlpkg import SQLAlchemy


@inject
@dataclass
class UploadFileService(BaseService):
    db: SQLAlchemy

    def create_upload_file(self, **kwargs) -> UploadFile:
        return self.create(UploadFile, **kwargs)
