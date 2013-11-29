# -*- coding: utf-8 -*-
"""
    Copyright (C) Quizzingbricks
"""

import datetime
import bcrypt
import sqlalchemy as sa
from sqlalchemy.orm import synonym, relationship

from quizzingbricks.common.db import Base
from quizzingbricks.services.users.models import User

class Lobby(Base):
    __tablename__ = "lobbies"

    lobby_id = sa.Column(sa.Integer, primary_key=True)
    game_type = sa.Column(sa.Integer, nullable=False)
    owner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    
    user = relationship(User, backref="lobbies",foreign_keys=[owner_id])
    
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)

                           
                           
class LobbyMembership(Base):
    __tablename__ = "lobbymemberships"
    
    lobby_id = sa.Column(sa.Integer, sa.ForeignKey("lobbies.lobby_id"), primary_key=True)
    status = sa.Column(sa.String, nullable=False, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    
    user = relationship(User, backref="lobbymemberships", foreign_keys=[user_id])
    lobby = relationship(Lobby, backref="lobbymemberships", foreign_keys=[lobby_id] )
    
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    
    # def _set_password(self, password):
    #     password = password.encode("utf-8")
    #     self._password = bcrypt.hashpw(password, bcrypt.gensalt())

    # def _get_password(self):
    #     return self._password

    # password = synonym("_password", descriptor=property(_get_password, _set_password))

    # def check_password(self, password):
    #     password = password.encode("utf-8")
    #     return bcrypt.hashpw(password, self.password.encode("utf-8")) == self.password.encode("utf-8")