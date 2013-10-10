"""create initial user table

Revision ID: 3899a0e148d3
Revises: None
Create Date: 2013-10-06 16:06:08.686807

"""

# revision identifiers, used by Alembic.
revision = '3899a0e148d3'
down_revision = None

import datetime
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(64), unique=True),
        sa.Column("email", sa.String(128), unique=True),
        sa.Column("password", sa.String(60)),
        sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow, nullable=False),
        sa.Column("updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    )


def downgrade():
    op.drop_table("users")
