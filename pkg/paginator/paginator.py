# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 21:49
# @FileName: paginator.py
from dataclasses import dataclass
from typing import Any

import math
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import Optional, NumberRange

from pkg.sqlpkg import SQLAlchemy


class PaginatorReq(FlaskForm):
    """分页请求base"""
    current_page: IntegerField = IntegerField('current_page', default=1, validators=[
        Optional(),
        NumberRange(min=1, max=9999, message='当前页数的范围在1-9999'),
    ])
    page_size = IntegerField('page_size', default=20, validators=[
        Optional(),
        NumberRange(min=1, max=50, message='每页数据的范围在1-50'),
    ])


@dataclass
class Paginator:
    """分页器"""
    total_page: int = 0
    total_record: int = 0
    current_page: int = 1
    page_size: int = 20

    def __init__(self, db: SQLAlchemy, req: PaginatorReq = None):
        if req is not None:
            self.current_page = req.current_page.data
            self.page_size = req.page_size.data
        self.db = db

    def paginate(self, select) -> list[Any]:
        """对传入的查询进行分页"""
        p = self.db.paginate(select, per_page=self.page_size, page=self.current_page, error_out=False)
        self.total_page = math.ceil(p.total / self.page_size)
        self.total_record = p.total

        return p.items


@dataclass
class PageModel:
    list: list[Any]
    paginator: Paginator
