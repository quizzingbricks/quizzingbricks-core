"""lobby_memberships

Revision ID: 4837dab62493
Revises: af8b0541219
Create Date: 2013-11-14 09:57:02.596624

"""

# revision identifiers, used by Alembic.
revision = '4837dab62493'
down_revision = 'af8b0541219'

from alembic import op
import sqlalchemy as sa
import datetime


def upgrade():
    op.create_table(
        "lobbymemberships",
        sa.Column("lobby_id", sa.Integer, sa.ForeignKey("lobbies.lobby_id"), primary_key=True),
        sa.Column("user_id",sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String, nullable=False, index=True),
        
        sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow, nullable=False),
        sa.Column("updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow,
                           nullable=False)
    )

                           
def downgrade():
    op.drop_table("lobbymemberships")
