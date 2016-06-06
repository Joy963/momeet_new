"""empty message

Revision ID: 3afd23e3a1a8
Revises: cd7e1fec8b8d
Create Date: 2016-06-06 11:07:54.811402

"""

# revision identifiers, used by Alembic.
revision = '3afd23e3a1a8'
down_revision = 'cd7e1fec8b8d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('edu_experience', sa.Column('major', sa.String(length=100), nullable=True))
    op.drop_column('edu_experience', 'specialty')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('edu_experience', sa.Column('specialty', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('edu_experience', 'major')
    ### end Alembic commands ###
