"""empty message

Revision ID: 5f4877ff3273
Revises: 2fa3c13e40cb
Create Date: 2016-06-13 11:33:53.928038

"""

# revision identifiers, used by Alembic.
revision = '5f4877ff3273'
down_revision = '2fa3c13e40cb'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('engagement_order', sa.Column('id', sa.String(length=32), nullable=False))
    op.drop_column('engagement_order', 'uuid')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('engagement_order', sa.Column('uuid', mysql.VARCHAR(length=32), nullable=False))
    op.drop_column('engagement_order', 'id')
    ### end Alembic commands ###
