"""add last few columns to posts table

Revision ID: 85d794559b56
Revises: 9b92ea0c312d
Create Date: 2022-01-18 11:27:26.037807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d794559b56'
down_revision = '9b92ea0c312d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
