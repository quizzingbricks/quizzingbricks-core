# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from quizzingbricks.common.db import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)