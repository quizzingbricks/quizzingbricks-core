"""sample questions

Revision ID: 2d9839e10689
Revises: 445f69111f49
Create Date: 2013-11-30 22:00:44.407065

"""

# revision identifiers, used by Alembic.
revision = '2d9839e10689'
down_revision = '445f69111f49'

from alembic import op
from sqlalchemy.sql import table
import sqlalchemy as sa


def upgrade():
    questions = table(
    "questions",
    sa.Column("questionid", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("question", sa.Text),
    sa.Column("alt1", sa.Text),
    sa.Column("alt2", sa.Text),
    sa.Column("alt3", sa.Text),
    sa.Column("alt4", sa.Text),
    sa.Column("answer", sa.Integer))

    op.bulk_insert(questions, [
        {'id' : 'server_default', 'question' : 'This is a question with correct answer 1', 'alt1' : 'Correct answer', 'alt2' : 'Incorrect answer', 'alt3' : 'Incorrect answer', 'alt4' : 'Incorrect answer', 'answer' : 1 },
        {'id' : 'server_default', 'question' : 'This is a question with correct answer 2', 'alt1' : 'Incorrect answer', 'alt2' : 'Correct answer', 'alt3' : 'Incorrect answer', 'alt4' : 'Incorrect answer', 'answer' : 2 },
        {'id' : 'server_default', 'question' : 'This is a question with correct answer 3', 'alt1' : 'Incorrect answer', 'alt2' : 'Incorrect answer', 'alt3' : 'Correct answer', 'alt4' : 'Incorrect answer', 'answer' : 3 },
        {'id' : 'server_default', 'question' : 'This is a question with correct answer 4', 'alt1' : 'Incorrect answer', 'alt2' : 'Incorrect answer', 'alt3' : 'Incorrect answer', 'alt4' : 'Correct answer', 'answer' : 4 }]) 
    pass


def downgrade():
    op.execute("TRUNCATE TABLE questions")
    pass
