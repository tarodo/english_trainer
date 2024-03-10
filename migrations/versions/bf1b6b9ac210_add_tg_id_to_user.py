"""add tg_id to user

Revision ID: bf1b6b9ac210
Revises: 12cdfab35e2b
Create Date: 2024-03-10 08:55:36.310683

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'bf1b6b9ac210'
down_revision = '12cdfab35e2b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('et_user', sa.Column('tg_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('et_user', 'tg_id')
    # ### end Alembic commands ###