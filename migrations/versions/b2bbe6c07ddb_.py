"""empty message

Revision ID: b2bbe6c07ddb
Revises: ddc5239023b3
Create Date: 2016-06-10 13:22:22.514671

"""

# revision identifiers, used by Alembic.
revision = 'b2bbe6c07ddb'
down_revision = 'ddc5239023b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('engagement_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host', sa.Integer(), nullable=False),
    sa.Column('guest', sa.Integer(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['guest'], ['user.id'], ),
    sa.ForeignKeyConstraint(['host'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8',
    mysql_engine='InnoDB'
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('engagement_order')
    ### end Alembic commands ###
