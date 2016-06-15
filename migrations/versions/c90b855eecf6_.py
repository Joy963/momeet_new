"""empty message

Revision ID: c90b855eecf6
Revises: 09686be12a40
Create Date: 2016-06-09 18:11:41.827108

"""

# revision identifiers, used by Alembic.
revision = 'c90b855eecf6'
down_revision = '09686be12a40'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('industry')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('industry',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    ### end Alembic commands ###
