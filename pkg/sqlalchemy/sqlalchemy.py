# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/13 22:23
# @FileName: sqlalchemy.py
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    """实现自动提交回滚"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
