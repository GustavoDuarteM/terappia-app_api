"""empty message

Revision ID: 0959356eeee5
Revises: c8cb2014b21b
Create Date: 2021-06-03 20:03:04.444802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0959356eeee5'
down_revision = 'c8cb2014b21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patients')
    # ### end Alembic commands ###
