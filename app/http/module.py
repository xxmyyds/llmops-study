# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/12 22:09
# @FileName: module.py
from flask_migrate import Migrate
from injector import Module, Binder

from internal.extension.database_extension import db
from internal.extension.migrate_extension import migrate
from pkg.sqlalchemy import SQLAlchemy


class ExtensionModule(Module):
    def configure(self, binder: Binder):
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
