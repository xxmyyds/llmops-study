# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/7/19 14:48
# @FileName: dataset_service.py
from dataclasses import dataclass
from uuid import UUID

from injector import inject

from internal.entity.dataset_entity import DEFAULT_DATASET_DESCRIPTION_FORMATTER
from internal.exception import ValidateException, NotFoundException
from internal.model import Dataset
from internal.schema.dataset_schema import CreateDatasetReq
from internal.service import BaseService
from pkg.sqlpkg import SQLAlchemy


@inject
@dataclass
class DatasetService(BaseService):
    """知识库服务"""
    db: SQLAlchemy

    def create_dataset(self, req: CreateDatasetReq) -> Dataset:
        """根据传递的请求信息创建知识库"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"

        dataset = self.db.session.query(Dataset).filter_by(
            account_id=account_id,
            name=req.name.data
        ).one_or_none()
        if dataset:
            raise ValidateException(f"该知识库{req.name.data}已存在")
        if req.description.data is None or req.description.data.strip() == "":
            req.description.data = DEFAULT_DATASET_DESCRIPTION_FORMATTER.format(name=req.name.data)
        return self.create(
            Dataset,
            account_id=account_id,
            name=req.name.data,
            icon=req.icon.data,
            description=req.description.data,
        )

    def get_dataset(self, dataset_id: UUID) -> Dataset:
        """根据传递的知识库id获取知识库记录"""
        account_id = "46db30d1-3199-4e79-a0cd-abf12fa6858f"
        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise NotFoundException('该知识库不存在')
        return dataset
