"""added score to players

Revision ID: 29eb8237af85
Revises: 2d9839e10689
Create Date: 2013-12-02 12:55:08.876505

"""

# revision identifiers, used by Alembic.
revision = '29eb8237af85'
down_revision = '2d9839e10689'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('playersgames', sa.Column('score', sa.Integer, server_default='0'))
    pass


def downgrade():
    op.drop_column('playersgames', 'score')
    pass