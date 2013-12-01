"""game service tables

Revision ID: 445f69111f49
Revises: 4837dab62493
Create Date: 2013-11-30 21:07:44.258829

"""

# revision identifiers, used by Alembic.
revision = '445f69111f49'
down_revision = '4837dab62493'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        "games",
        sa.Column("gameid", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("board", sa.Text)
    )
    op.create_table(
        "playersgames",
        sa.Column("playerid", sa.Integer),
        sa.Column("gameid", sa.Integer),
        sa.Column("state", sa.Integer),
        sa.Column("x", sa.Integer),
        sa.Column("y", sa.Integer),
        sa.Column("question", sa.Text),
        sa.Column("alt1", sa.Text), 
        sa.Column("alt2", sa.Text),
        sa.Column("alt3", sa.Text),
        sa.Column("alt4", sa.Text),
        sa.Column("correctanswer", sa.Integer),
        sa.Column("answer", sa.Integer)
    )


    op.create_primary_key(
         "pk_games", "playersgames",
        ["playerid", "gameid"]
    )
    op.create_index('playeridx', 'playersgames', ['playerid', 'gameid'])
    op.create_index('gameidx', 'playersgames', ['gameid', 'playerid'])
    
    op.create_table(
        "questions",
        sa.Column("questionid", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("question", sa.Text),
        sa.Column("alt1", sa.Text),
        sa.Column("alt2", sa.Text),
        sa.Column("alt3", sa.Text),
        sa.Column("alt4", sa.Text),
        sa.Column("answer", sa.Integer)
    )

def downgrade():
    op.drop_table("games")
    op.drop_table("playersgames")
    op.drop_table("questions")





