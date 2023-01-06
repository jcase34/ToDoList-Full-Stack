"""create post table

Revision ID: 99792f644e38
Revises: 
Create Date: 2022-12-30 12:13:10.785058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99792f644e38'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
