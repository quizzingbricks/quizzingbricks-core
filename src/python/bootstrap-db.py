# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.common.db import Base, engine

from quizzingbricks.users.models import User

if __name__ == "__main__":
    Base.metadata.create_all(engine)