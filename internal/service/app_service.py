# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/4/13 21:49
# @FileName: app_service.py
import uuid
from dataclasses import dataclass

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            app = App(name='测试机器人', account_id=uuid.uuid4(), icon='', description='这是一个简单的机器人聊天')
            self.db.session.add(app)

        return app

    def get_app(self, id: uuid.UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id=id)
            app.name = 'xxmyyds'

        return app

    def delete_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id=id)
            self.db.session.delete(app)
        return app
