"""empty message

Revision ID: fb85f1227e84
Revises: 2601ca087b59
Create Date: 2016-06-07 12:35:58.538019

"""

# revision identifiers, used by Alembic.
revision = 'fb85f1227e84'
down_revision = '2601ca087b59'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('theme')
    op.add_column('engagement', sa.Column('theme', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('engagement', 'theme')
    op.create_table('theme',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('engagement_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('name', mysql.VARCHAR(length=200), nullable=True),
    sa.ForeignKeyConstraint(['engagement_id'], [u'engagement.id'], name=u'theme_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
