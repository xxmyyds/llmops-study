# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/17 20:40
# @FileName: dataset_handler.py
from dataclasses import dataclass
from uuid import UUID

from injector import inject

from internal.schema.dataset_schema import CreateDatasetReq
from internal.service import DatasetService
from pkg.response import validate_error_json, success_message


@inject
@dataclass
class DatasetHandler:
    """知识库处理器"""
    dataset_service: DatasetService

    def create_dataset(self):
        """创建知识库"""
        req = CreateDatasetReq()
        if not req.validate():
            return validate_error_json(req.errors)

        self.dataset_service.create_dataset(req)

        return success_message('创建知识库成功')

    def get_dataset(self, dataset_id: UUID):
        """根据传递的知识库id获取详情"""
        pass

    def update_dataset(self, dataset_id: UUID):
        """根据传递的知识库id+信息更新知识库"""
        pass

    def get_datasets_with_page(self):
        """获取知识库分页+搜索列表数据"""
        pass
