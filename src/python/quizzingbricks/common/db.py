# -*- coding: utf-8 -*-
"""
    Copyright (C) QuizzingBricks
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# we don't need to protect the password in this stage, but move to config file later.
engine = create_engine("postgresql+psycopg2://qb:qb123@127.0.0.1:5432/quizzingbricks_dev",
    convert_unicode=True,
    pool_size=8, # change to what?
    max_overflow=0
)
#engine = create_engine("sqlite:///quizzingbricks.db", echo=True)

metadata = MetaData()
session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine)
)

Base = declarative_base(metadata=metadata)
Base.query = session.query_property()