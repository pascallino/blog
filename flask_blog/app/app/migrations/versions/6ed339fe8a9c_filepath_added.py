"""filepath_added

Revision ID: 6ed339fe8a9c
Revises: 87fbd0263d7a
Create Date: 2023-11-06 12:14:01.612777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ed339fe8a9c'
down_revision = '87fbd0263d7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filepath', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('filepath')

    # ### end Alembic commands ###
