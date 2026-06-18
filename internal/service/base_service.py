# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/18 16:17
# @FileName: base_service.py
from typing import Any, Optional

from exception import FailException
from sqlpkg import SQLAlchemy


class BaseService:
    """基础service"""
    db: SQLAlchemy

    def create(self, model: Any, **kwargs) -> Any:
        with self.db.auto_commit():
            model_instance = model(**kwargs)
            self.db.session.add(model_instance)
        return model_instance

    def delete(self, model_instance: Any, **kwargs) -> Any:
        with self.db.auto_commit():
            self.db.session.delete(model_instance)
        return model_instance

    def update(self, model_instance: Any, **kwargs) -> Any:
        with self.db.auto_commit():
            for field, value in kwargs.items():
                if hasattr(model_instance, field):
                    setattr(model_instance, field, value)
                else:
                    raise FailException('更新失败')
        return model_instance

    def get(self, model: Any, primary_key) -> Optional[Any]:
        return self.db.session.query(model).get(primary_key)
