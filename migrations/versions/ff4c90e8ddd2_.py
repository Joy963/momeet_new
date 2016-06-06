"""empty message

Revision ID: ff4c90e8ddd2
Revises: 4d0374215543
Create Date: 2016-06-06 19:05:31.627951

"""

# revision identifiers, used by Alembic.
revision = 'ff4c90e8ddd2'
down_revision = '4d0374215543'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_photo', sa.Column('is_active', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_photo', 'is_active')
    ### end Alembic commands ###