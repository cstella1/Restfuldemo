"""empty message

Revision ID: 733b451fddb7
Revises: 10bb38c8796a
Create Date: 2022-08-05 09:03:54.109875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733b451fddb7'
down_revision = '10bb38c8796a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isdelete', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'email')
    op.drop_column('user', 'isdelete')
    # ### end Alembic commands ###
