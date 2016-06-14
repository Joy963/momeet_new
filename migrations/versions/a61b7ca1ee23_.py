"""empty message

Revision ID: a61b7ca1ee23
Revises: 951b0cbf24a4
Create Date: 2016-06-13 11:32:06.013482

"""

# revision identifiers, used by Alembic.
revision = 'a61b7ca1ee23'
down_revision = '951b0cbf24a4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'engagement_order', 'user', ['guest'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'engagement_order', type_='foreignkey')
    ### end Alembic commands ###