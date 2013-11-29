"""lobbies

Revision ID: af8b0541219
Revises: 22ece6d73f9d
Create Date: 2013-11-14 07:46:18.681898

"""

# revision identifiers, used by Alembic.
revision = 'af8b0541219'
down_revision = '22ece6d73f9d'

from alembic import op
import sqlalchemy as sa
import datetime


def upgrade():
    op.create_table(
        "lobbies",
        sa.Column("lobby_id", sa.Integer, primary_key=True),
        sa.Column("game_type", sa.Integer, nullable=False),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),       
        sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow, nullable=False),
        sa.Column("updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    )

def downgrade():
    op.drop_table("lobbies")
