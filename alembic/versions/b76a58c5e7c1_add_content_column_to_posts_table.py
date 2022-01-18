"""add content column to posts table

Revision ID: b76a58c5e7c1
Revises: 6e5e94351f0c
Create Date: 2022-01-18 11:11:48.165321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b76a58c5e7c1'
down_revision = '6e5e94351f0c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
