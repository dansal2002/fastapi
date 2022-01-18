"""add users table

Revision ID: 32f417cb7e86
Revises: b76a58c5e7c1
Create Date: 2022-01-18 11:15:40.002045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32f417cb7e86'
down_revision = 'b76a58c5e7c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), #sets primary key
                    sa.UniqueConstraint('email') #prevents duplicate emails
                    )
    pass

def downgrade():
    op.drop_table('users')
    pass
