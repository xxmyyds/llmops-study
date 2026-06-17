# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/6/17 16:07
# @FileName: schema.py
from wtforms import Field


class ListField(Field):
    data: list = None

    def process_formdata(self, valueList):
        if valueList is not None and isinstance(valueList, list):
            self.data = valueList

    def _value(self):
        return self.data if self.data else []
