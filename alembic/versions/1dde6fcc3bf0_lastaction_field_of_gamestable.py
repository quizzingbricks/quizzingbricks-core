"""lastAction field of gamestable

Revision ID: 1dde6fcc3bf0
Revises: 481cc16e0cb2
Create Date: 2013-12-06 16:47:23.513761

"""

# revision identifiers, used by Alembic.
revision = '1dde6fcc3bf0'
down_revision = '481cc16e0cb2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('games', sa.Column('lastaction', postgresql.BIGINT))
    op.add_column('games', sa.Column('finished', sa.Boolean, default=False))
    pass


def downgrade():
    op.drop_column('games', 'lastaction')
    op.drop_column('games', 'finished')
    pass
