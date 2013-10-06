# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

import datetime
import bcrypt
import sqlalchemy as sa
from sqlalchemy.orm import synonym

from quizzingbricks.common.db import Base

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(128), nullable=False, unique=True)
    _password = sa.Column("password", sa.String(60), nullable=False)

    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)

    def _set_password(self, password):
        self._password = bcrypt.hashpw(password, bcrypt.gensalt())

    def _get_password(self):
        return self._password

    password = synonym("_password", descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        return bcrypt.hashpw(password, self._password) == self._password