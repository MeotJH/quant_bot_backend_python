"""Change pasword column string length

Revision ID: 76cfe2c48770
Revises: 6b06704421b7
Create Date: 2024-09-07 23:30:23.764414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76cfe2c48770'
down_revision = '6b06704421b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=512),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###
