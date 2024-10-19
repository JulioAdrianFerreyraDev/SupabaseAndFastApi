"""add caterogies' table

Revision ID: 32ccb8aa3523
Revises: 09b3dd160023
Create Date: 2024-10-18 19:47:38.564064

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '32ccb8aa3523'
down_revision: Union[str, None] = '09b3dd160023'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("categories", sa.Column(sa.Integer, name="category_id", primary_key=True),
                    sa.Column(sa.String, name="category", nullable=False), if_not_exists=True)


def downgrade() -> None:
    op.drop_table("categories", if_exists=True)
