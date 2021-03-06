"""empty message

Revision ID: 3fc9033213b6
Revises: 57302998d431
Create Date: 2016-06-14 13:45:55.504869

"""

# revision identifiers, used by Alembic.
revision = '3fc9033213b6'
down_revision = '57302998d431'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personal_label',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('job_label',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('tag')
    op.drop_column(u'user', 'personal_label')
    op.drop_column(u'user', 'job_label')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'user', sa.Column('job_label', mysql.VARCHAR(length=2000), nullable=True))
    op.add_column(u'user', sa.Column('personal_label', mysql.VARCHAR(length=2000), nullable=True))
    op.create_table('tag',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('job_label')
    op.drop_table('personal_label')
    ### end Alembic commands ###
