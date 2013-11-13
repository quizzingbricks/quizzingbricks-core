"""Friends

Revision ID: 22ece6d73f9d
Revises: 3899a0e148d3
Create Date: 2013-11-11 13:00:57.351847

"""

# revision identifiers, used by Alembic.
revision = '22ece6d73f9d'
down_revision = '3899a0e148d3'

from alembic import op
import datetime
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "friendships",
        sa.Column("friend_id" ,sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False, primary_key=True),
        sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow, nullable=False),
        sa.Column("updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    )


def downgrade():
    op.drop_table("friendships")
