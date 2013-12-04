"""trying to make questions

Revision ID: 481cc16e0cb2
Revises: 29eb8237af85
Create Date: 2013-12-04 12:27:34.677747

"""

# revision identifiers, used by Alembic.
revision = '481cc16e0cb2'
down_revision = '29eb8237af85'

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
        {'id' : 'server_default', 'question' : 'Which alternative medicine practice uses dogs and cobras to ease stress and cut anxiety?', 'alt1' : 'Yoga', 'alt2' : 'Meditation', 'alt3' : 'Guided Imagery', 'alt4' : 'Homeopathy', 'answer' : 1 },
        {'id' : 'server_default', 'question' : 'What is the national emblem of Canada?', 'alt1' : 'Maple syrup', 'alt2' : 'Bison', 'alt3' : 'Maple leaf', 'alt4' : 'Bear', 'answer' : 3 },
        {'id' : 'server_default', 'question' : 'What girls name is also the term used to describe a female donkey?', 'alt1' : 'Anna', 'alt2' : 'Johanna', 'alt3' : 'Jenny', 'alt4' : 'Karla', 'answer' : 3 },
        {'id' : 'server_default', 'question' : 'In which sport would you use a chucker?', 'alt1' : 'Lacrosse', 'alt2' : 'Cricket', 'alt3' : 'Rugby', 'alt4' : 'Polo', 'answer' : 4 },
        {'id' : 'server_default', 'question' : 'What line follows \'15 men on a dead mans chest\'?', 'alt1' : 'Yo ho ho and a chest full of booty', 'alt2' : 'Yo ho ho and a bottle of RUM', 'alt3' : 'and a another on \'tis way', 'alt4' : '-Nothing-', 'answer' : 2 },
        {'id' : 'server_default', 'question' : 'What is the gemstone for September?', 'alt1' : 'Sapphire', 'alt2' : 'Ruby', 'alt3' : 'Emerald', 'alt4' : 'Quartz', 'answer' : 1 },
        {'id' : 'server_default', 'question' : 'Which cartoon has a bar called \'Moes\'?', 'alt1' : 'Futurama', 'alt2' : 'The Simpsons', 'alt3' : 'Family Guy', 'alt4' : 'American Dad', 'answer' : 2 },
        {'id' : 'server_default', 'question' : 'Where did Luke Skywalker first meet Han Solo?', 'alt1' : 'The death star', 'alt2' : 'Mos Espa bar', 'alt3' : 'Coruscant Coco Town', 'alt4' : 'Mos Eisley Cantina', 'answer' : 4 },
        {'id' : 'server_default', 'question' : 'In which fantasy story was a kingdom found at the back of the wardrobe?', 'alt1' : 'Winnie-the-Pooh', 'alt2' : 'Narnia', 'alt3' : 'Eragon', 'alt4' : 'Alice in wonderland', 'answer' : 2 },
        {'id' : 'server_default', 'question' : 'How many toes does a dog have?', 'alt1' : '18', 'alt2' : '16', 'alt3' : '20', 'alt4' : '22', 'answer' : 1 }])
    pass




def downgrade():
    op.execute("TRUNCATE TABLE questions")
    pass

